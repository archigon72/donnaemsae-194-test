"""돈냄새연구소 원클릭 격리 갱신 (GrokBot). 수집→원천보존(비공개 경로)→정규화→승인 CORE(runtime_source.zip) 실행→자동 QA→PASS 시 격리 release 승격.
쓰기 대상: <site>/auto-test/releases/<release_id>/ 와 <site>/auto-test/latest.json 만. 기존 사이트 파일/inputs/data 불변.
누락값은 0으로 대체하지 않음(행 자체 미추가 + 사유 기록). 원천 raw 는 --raw-dir(비공개/임시)에만 저장, 공개 트리에는 해시만.
사용: python3 oneclick.py --site <pages_root> --raw-dir <private_dir> [--mode live|replay] [--replay-dir D] [--asof YYYYMMDD]
      [--inject-error KIND] [--interrupt-after-build] [--codes a,b]"""
import argparse,json,os,sys,hashlib,time,datetime,urllib.request,zipfile,tempfile,shutil,copy,re,traceback
ap=argparse.ArgumentParser();ap.add_argument('--site',required=True);ap.add_argument('--raw-dir',required=True)
ap.add_argument('--mode',default='live');ap.add_argument('--replay-dir');ap.add_argument('--asof')
ap.add_argument('--inject-error');ap.add_argument('--interrupt-after-build',action='store_true');ap.add_argument('--codes')
ap.add_argument('--publish-raw',action='store_true',help='대표 승인(공개 허용): 원천 raw 를 auto-test/raw/<release_id>/ 에 보존(덮어쓰기 금지)')
ap.add_argument('--base-release',help='use this release dir (inputs snapshot) as previous state instead of site inputs')
A=ap.parse_args();SITE=os.path.abspath(A.site);AT=f'{SITE}/auto-test'
KST=datetime.timezone(datetime.timedelta(hours=9));NOW=datetime.datetime.now(KST)
ASOF=A.asof or NOW.strftime('%Y%m%d')
RID=f"auto-{ASOF}-{NOW.strftime('%H%M%S')}-{A.mode}"+(f"-inj-{A.inject_error}" if A.inject_error else '')
RAW=os.path.join(os.path.abspath(A.raw_dir),RID);os.makedirs(RAW,exist_ok=False)
LOG={'release_id':RID,'mode':A.mode,'asof':ASOF,'started_kst':NOW.isoformat(),'steps':[],'collect':{},'qa':[],'result':None}
def step(n,**k): LOG['steps'].append({'step':n,'t':datetime.datetime.now(KST).isoformat(),**k});print('STEP',n,json.dumps(k,ensure_ascii=False)[:300],flush=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def wjson(p,o): os.makedirs(os.path.dirname(p),exist_ok=True);open(p,'w').write(json.dumps(o,ensure_ascii=False,separators=(',',':')))
codes=sorted(f[:-5] for f in os.listdir(f'{SITE}/inputs') if f.endswith('.json'))
if A.codes: codes=[c for c in codes if c in A.codes.split(',')]
PREV_IN=A.base_release and f'{A.base_release}/inputs' or f'{SITE}/inputs'
def prev_bundle(c):
    p=f'{PREV_IN}/{c}.json'
    if not os.path.exists(p): p=f'{SITE}/inputs/{c}.json'
    return json.load(open(p))
UA={'User-Agent':'Mozilla/5.0 (donnaemsae-194-test oneclick)'}
def fetch(u,tries=3,to=30):
    err=None
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=to) as r: return r.status,r.read()
        except Exception as e: err=str(e)[:120];time.sleep(1.5*(i+1))
    return None,err
# ---------- 1 collect ----------
def collect(c,b):
    isin=b['manifest']['isin'];last=b['meta']['data_cutoff'].replace('-','')
    st=(datetime.date.fromisoformat(b['meta']['data_cutoff'])-datetime.timedelta(days=10)).strftime('%Y%m%d')
    out={'isin':isin,'prev_cutoff':b['meta']['data_cutoff']}
    if A.mode=='replay':
        d=f'{A.replay_dir}/{c}'
        if not os.path.isdir(d): return {**out,'status':'fail','reason':'replay source missing'},None,None,None
        nav=open(f'{d}/nav.json','rb').read();div=open(f'{d}/div.json','rb').read();zq=open(f'{d}/zeroin.json','rb').read() if os.path.exists(f'{d}/zeroin.json') else None
    else:
        s1,nav=fetch(f'https://www.funetf.co.kr/api/public/product/view/etfnav?gijunYmd={ASOF}&fundCd={isin}&itemId={isin}&schNavStDt={st}&schNavEdDt={ASOF}')
        s2,div=fetch(f'https://www.funetf.co.kr/api/public/product/view/etfdividend?gijunYmd={ASOF}&fundCd={isin}&itemId={isin}')
        s3,zq=fetch(f'https://etf.zeroin.co.kr/api/quote/{c}',tries=2,to=12)
        if s1!=200 or s2!=200: return {**out,'status':'fail','reason':f'funetf nav={s1 or nav} div={s2 or div}'},None,None,None
        if s3!=200: out['zeroin']=f'fail {zq}';zq=None
    os.makedirs(f'{RAW}/{c}',exist_ok=True)
    for n,v in (('nav.json',nav),('div.json',div),('zeroin.json',zq)):
        if v is not None: open(f'{RAW}/{c}/{n}','wb').write(v);out.setdefault('sha256',{})[n]=sha(v)
    try: N=json.loads(nav,parse_float=str);D=json.loads(div,parse_float=str);Z=json.loads(zq) if zq else None
    except Exception as e: return {**out,'status':'fail','reason':'parse '+str(e)[:80]},None,None,None
    if not isinstance(N,list) or not isinstance(D,list): return {**out,'status':'fail','reason':'unexpected payload'},None,None,None
    if not N: return {**out,'status':'fail','reason':'nav empty (source returned 0 rows)'},None,None,None
    if Z is not None: out['zeroin']='ok as_of %s'%Z.get('as_of')
    return {**out,'status':'ok'},N,D,Z
# ---------- 2 normalize ----------
def norm_row(r,tmpl):
    o={k:(None if r.get(k) is None else (r[k] if isinstance(r[k],int) else str(r[k]))) for k in tmpl}
    if tmpl.get('clsp') is None: o['clsp']=o['clspDiff']=o['clspDiffRt']=None
    return o
def merge(c,b,N,D,info):
    nb=copy.deepcopy(b);old={r['gijunYmd']:r for r in b['nav_rows']};tmpl=b['nav_rows'][0]
    add=[];mism=[];skipped=[]
    for r in N:
        d=r.get('gijunYmd')
        if not d or not re.fullmatch(r'\d{8}',d): skipped.append(str(d));continue
        if r.get('fp') in (None,''): skipped.append(d+':fp missing');continue   # never 0
        if d in old:
            if old[d].get('fp') is not None and float(old[d]['fp'])!=float(r['fp']): mism.append({'date':d,'old':old[d]['fp'],'new':r['fp']})
        elif d>b['nav_rows'][0]['gijunYmd']: add.append(norm_row(r,tmpl))
    add.sort(key=lambda r:r['gijunYmd'],reverse=True);nb['nav_rows']=add+b['nav_rows']
    dkeys={(r['gijunYmd'],str(r.get('divAmt'))) for r in b['distribution_rows']};dold={r['gijunYmd'] for r in b.get('distribution_rows_raw',b['distribution_rows'])};dadd=[];dchg=[]
    dt=b['distribution_rows'][0] if b['distribution_rows'] else (D[0] if D else {})
    for r in D:
        d=r.get('gijunYmd')
        if d in dold:
            # same ex-date: payDt may have been filled since (estimated->actual); record, do not rewrite approved rows here
            o=[x for x in b.get('distribution_rows_raw',b['distribution_rows']) if x['gijunYmd']==d][0]
            if str(r.get('payDt'))!=str(o.get('payDt')) or (r.get('divAmt') is not None and o.get('divAmt') is not None and float(r['divAmt'])!=float(o['divAmt'])): dchg.append({'date':d,'old_payDt':o.get('payDt'),'new_payDt':r.get('payDt'),'old_amt':o.get('divAmt'),'new_amt':r.get('divAmt')})
        else:
            if r.get('divAmt') in (None,''): skipped.append(d+':divAmt missing');continue
            dadd.append({k:(None if r.get(k) is None else (r[k] if isinstance(r[k],int) else str(r[k]))) for k in (dt or r)})
    if 'distribution_rows_raw' in nb: nb['distribution_rows_raw']=dadd+nb['distribution_rows_raw']
    nb['distribution_rows']=sorted(dadd,key=lambda r:r['gijunYmd'],reverse=True)+b['distribution_rows']
    newcut=max(r['gijunYmd'] for r in nb['nav_rows']);newcut=f'{newcut[:4]}-{newcut[4:6]}-{newcut[6:]}'
    nb['meta']['data_cutoff']=newcut;nb['meta']['snapshot_id']=RID;nb['manifest']['data_cutoff']=newcut;nb['manifest']['last_date']=newcut
    nb['manifest']['observations']=len(nb['nav_rows']);nb['manifest']['oneclick']={'release_id':RID,'raw_sha256':info.get('sha256'),'source_mode':A.mode}
    info.update(nav_added=len(add),div_added=len(dadd),div_changed=dchg,overlap_mismatch=mism,skipped=skipped,new_cutoff=newcut,
                state=('updated' if add or dadd else 'no_change_normal'))
    return nb
# ---------- run ----------
try:
    step('start',codes=len(codes),site_tree_untouched_paths=['inputs/','data/','*.html','*.js'])
    WORK=tempfile.mkdtemp(prefix='oneclick-');os.makedirs(f'{WORK}/inputs');os.makedirs(f'{WORK}/data')
    for f in ('runtime_source.zip','presentation.py','facts_projection.py','market_projection.py'):
        if os.path.exists(f'{SITE}/{f}'): shutil.copy(f'{SITE}/{f}',WORK)
    ok=0;fail=0
    from concurrent.futures import ThreadPoolExecutor
    PB_={c:prev_bundle(c) for c in codes}
    with ThreadPoolExecutor(6) as ex: RES=dict(zip(codes,ex.map(lambda c:collect(c,PB_[c]),codes)))
    for c in codes:
        b=PB_[c];info,N,D,Z=RES[c];LOG['collect'][c]=info
        if info['status']=='ok': nb=merge(c,b,N,D,info);ok+=1
        else: nb=b;fail+=1
        wjson(f'{WORK}/inputs/{c}.json',nb)
    st={}
    for v in LOG['collect'].values(): st[v.get('state',v['status'])]=st.get(v.get('state',v['status']),0)+1
    step('collect',ok=ok,fail=fail,states=st)
    if A.inject_error=='collect_fail_all': fail=len(codes)
    # ---------- 3 CORE ----------
    RT=tempfile.mkdtemp(prefix='rt-');zipfile.ZipFile(f'{WORK}/runtime_source.zip').extractall(RT);sys.path[:0]=[RT,WORK];sys.dont_write_bytecode=True
    import period_bridge,presentation
    cat=json.load(open(f'{SITE}/data/catalog.json'));cat['snapshot']['snapshot_id']=RID
    built={};errs=[]
    for c in codes:
        b=json.load(open(f'{WORK}/inputs/{c}.json'))
        if A.inject_error=='bad_input' and c==codes[0]: b['distribution_rows'].insert(0,dict(b['distribution_rows'][0] if b['distribution_rows'] else {},gijunYmd='20261013',divAmt='-5.0'))
        b['meta']['snapshot_id']=RID
        out={'snapshot':b['meta'],'ticker':c,'periods':{},'presentations':{}}
        for k in ['1개월','6개월','1년','전체']:
            bb=copy.deepcopy(b);bb['period']=k;v=period_bridge.run_period(bb,None,None);out['periods'][k]=v;out['presentations'][k]=presentation.detail_presentation(v,bb)
        s=json.dumps(out,ensure_ascii=False,separators=(',',':'));built[c]=s
        for it in cat['items']:
            if it['ticker']==c: it['available_period']['end']=b['meta']['data_cutoff']
    step('core_build',built=len(built),engine_hash=cat['snapshot']['engine_hash'])
    if A.interrupt_after_build: step('interrupted');LOG['result']='INTERRUPTED';raise SystemExit(3)
    # ---------- 4 QA ----------
    def qa(n,okk,d=None): LOG['qa'].append({'check':n,'pass':bool(okk),'detail':d});print(('PASS ' if okk else 'FAIL ')+n,json.dumps(d,ensure_ascii=False)[:300] if d is not None else '',flush=True)
    qa('194/194 tickers built',len(built)==194 or (A.codes and len(built)==len(codes)),len(built))
    qa('collection: 0 failed tickers',fail==0,{c:v['reason'] for c,v in LOG['collect'].items() if v['status']!='ok'})
    prev_err=[];new_err=[];LEGIT=[]
    for c in codes:
        o=json.loads(open(f'{SITE}/data/{c}.json').read()) if os.path.exists(f'{SITE}/data/{c}.json') else {'periods':{}}
        n=json.loads(built[c])
        for k in ['1개월','6개월','1년','전체']:
            if (o['periods'].get(k) or {}).get('status')=='ERROR': prev_err.append(c+k)
            if n['periods'][k].get('status')=='ERROR':
                pre={i.get('code') for i in (o['periods'].get(k) or {}).get('issues',[])}
                codes_=sorted({i.get('code') for i in n['periods'][k].get('issues',[])}-pre)
                if codes_==['insufficient_period']: LEGIT.append(c+k)   # CORE 정상 판정(관측 20개 미만, 예: 연휴) — 오류 아님
                else: new_err.append(c+k)
    qa('no new ERROR periods vs deployed',set(new_err)<=set(prev_err),sorted(set(new_err)-set(prev_err))[:10])
    qa('info: CORE insufficient_period (legit, not failure) count',True,{'n':len(LEGIT),'sample':LEGIT[:6]});LOG['legit_insufficient']=LEGIT
    iso=re.compile(r'^\d{4}-\d{2}-\d{2}$');badiso=[c for c in codes if not iso.match(json.loads(built[c])['snapshot']['data_cutoff'])]
    qa('data_cutoff ISO',not badiso,badiso[:5])
    reg=[c for c,v in LOG['collect'].items() if v.get('new_cutoff') and v['new_cutoff']<v['prev_cutoff']]
    qa('per-ticker cutoff non-decreasing',not reg,reg)
    mm={c:v['overlap_mismatch'] for c,v in LOG['collect'].items() if v.get('overlap_mismatch')}
    qa('overlap NAV identical to preserved source (no silent rewrite)',not mm,mm)
    rawok=all(re.fullmatch(r'\d{8}',r['gijunYmd']) for c in codes for r in json.load(open(f'{WORK}/inputs/{c}.json'))['nav_rows'][:5])
    qa('raw gijunYmd kept YYYYMMDD',rawok)
    if '329200' in built:
        b=json.load(open(f'{WORK}/inputs/329200.json'));d=json.loads(built['329200'])
        ov=[o for o in b.get('normalization_overrides',[]) if o.get('rule_id')=='329200-20240628-same-round-v1']
        qa('329200 override kept; 전체 not ERROR; raw rows >= 60',bool(ov) and d['periods']['전체'].get('status')!='ERROR' and len(b.get('distribution_rows_raw',[]))>=60,{'raw':len(b.get('distribution_rows_raw',[])),'calc':len(b['distribution_rows'])})
    zero=[(c,r['gijunYmd']) for c,v in LOG['collect'].items() for r in json.load(open(f'{WORK}/inputs/{c}.json'))['distribution_rows'][:v.get('div_added',0)] if float(r.get('divAmt') or 0)<=0]
    qa('new distribution rows: no 0/negative amounts introduced',not zero,zero[:5])
    # existing approved validator (pipeline/validate_json.py) on the candidate release tree
    for c,sv in built.items(): open(f'{WORK}/data/{c}.json','w').write(sv)
    open(f'{WORK}/data/catalog.json','w').write(json.dumps(cat,ensure_ascii=False))
    import subprocess
    vp=subprocess.run([sys.executable,f'{SITE}/pipeline/validate_json.py',WORK],capture_output=True,text=True,timeout=1800)
    tail=(vp.stdout+vp.stderr)[-600:];LOG['validator_tail']=tail
    try: vj=json.loads(vp.stdout);vf=vj['counts'].get('FAIL',0);vd={'counts':vj['counts'],'fail_by_check':vj['fail_by_check']}
    except Exception: vf=None;vd=tail[-300:]
    LOG['validator']=vd;qa('pipeline/validate_json.py on release tree: 0 FAIL',vf==0,vd)
    if A.inject_error=='qa_fail': qa('forced QA failure (inject)',False)
    passed=all(q['pass'] for q in LOG['qa']);step('qa',passed=passed,nq=len(LOG['qa']),fails=[q['check'] for q in LOG['qa'] if not q['pass']])
    if not passed: LOG['result']='FAIL_NOT_PROMOTED';raise SystemExit(2)
    # ---------- 5 promote (immutable dir then pointer) ----------
    R=f'{AT}/releases/{RID}';assert not os.path.exists(R);TMP=R+'.partial';os.makedirs(f'{TMP}/data')
    files={}
    for c,s in built.items(): open(f'{TMP}/data/{c}.json','w').write(s);files[f'data/{c}.json']=sha(s.encode())
    cs=json.dumps(cat,ensure_ascii=False,separators=(',',':'));open(f'{TMP}/data/catalog.json','w').write(cs);files['data/catalog.json']=sha(cs.encode())
    man={'release_id':RID,'created_kst':datetime.datetime.now(KST).isoformat(),'mode':A.mode,'asof':ASOF,'engine_hash':cat['snapshot']['engine_hash'],
         'cutoffs':{c:json.loads(built[c])['snapshot']['data_cutoff'] for c in codes},'collect_summary':st,'files':files,
         'raw_sha256':{c:v.get('sha256') for c,v in LOG['collect'].items()},'note':'raw sources are NOT published; hashes only'}
    wjson(f'{TMP}/manifest.json',man)
    # verify before exposing
    bad=[p for p,h in files.items() if sha(open(f'{TMP}/{p}','rb').read())!=h];assert not bad,bad
    os.rename(TMP,R)
    prevlatest=json.load(open(f'{AT}/latest.json')) if os.path.exists(f'{AT}/latest.json') else None
    lt={'release_id':RID,'path':f'releases/{RID}/','manifest_sha256':sha(open(f'{R}/manifest.json','rb').read()),'promoted_kst':datetime.datetime.now(KST).isoformat(),
        'mode':A.mode,'previous':prevlatest and prevlatest['release_id'],'max_cutoff':max(man['cutoffs'].values()),'qa':'PASS'}
    wjson(f'{AT}/latest.json.tmp',lt);os.replace(f'{AT}/latest.json.tmp',f'{AT}/latest.json')
    LOG['result']='PASS_PROMOTED';step('promoted',release=RID)
except SystemExit as e:
    pass
except Exception as e:
    LOG['result']='ERROR_NOT_PROMOTED';LOG['error']=traceback.format_exc()[-1500:];print(LOG['error'])
finally:
    os.makedirs(f'{AT}/runs',exist_ok=True)
    pub={k:v for k,v in LOG.items() if k!='collect'};pub['collect']={c:{k:v[k] for k in v if k in('status','reason','state','nav_added','div_added','new_cutoff','prev_cutoff','zeroin','overlap_mismatch','div_changed','skipped')} for c,v in LOG['collect'].items()}
    wjson(f'{AT}/runs/{RID}.json',pub)
    ix=json.load(open(f'{AT}/runs/index.json')) if os.path.exists(f'{AT}/runs/index.json') else []
    ix.insert(0,{'release_id':RID,'result':LOG['result'],'mode':A.mode,'inject':A.inject_error,'started_kst':LOG['started_kst'],
      'collect':{k:sum(1 for v in LOG['collect'].values() if v.get('state',v['status'])==k) for k in ('updated','no_change_normal','fail')},
      'qa_fail':[q['check'] for q in LOG['qa'] if not q['pass']]})
    wjson(f'{AT}/runs/index.json',ix[:200]);json.dump(LOG,open(f'{RAW}/run_log.json','w'),ensure_ascii=False,indent=1)
    if A.publish_raw and LOG['collect']:
        dst=f'{AT}/raw/{RID}';assert not os.path.exists(dst);shutil.copytree(RAW,dst)
    print('RESULT',LOG['result'],RID)
    sys.exit(0 if LOG['result']=='PASS_PROMOTED' else 1)
