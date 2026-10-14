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
# ---------- ZeroIn 시험 제어 (yml 변경 없이; 시험 후 반드시 none) ----------
CTLP=os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_control.json')
CTL=json.load(open(CTLP)) if os.path.exists(CTLP) else {}
ZSIM=CTL.get('zeroin_scenario','none')
assert ZSIM in ('none','all_fail','partial','all_success','block_no_prev'),ZSIM
ZFIX=CTL.get('fixture_release','auto-20261014-143346-live')   # GrokBot box 실수집 132/194 (2026-10-14 KST)
KST=datetime.timezone(datetime.timedelta(hours=9));NOW=datetime.datetime.now(KST)
ASOF=A.asof or NOW.strftime('%Y%m%d')
RID=f"auto-{ASOF}-{NOW.strftime('%H%M%S')}-{A.mode}"+(f"-inj-{A.inject_error}" if A.inject_error else '')+(f"-zsim-{ZSIM}" if ZSIM!='none' else '')
RAW=os.path.join(os.path.abspath(A.raw_dir),RID);os.makedirs(RAW,exist_ok=False)
LOG={'release_id':RID,'zeroin_scenario':ZSIM,'mode':A.mode,'asof':ASOF,'started_kst':NOW.isoformat(),'steps':[],'collect':{},'qa':[],'result':None}
def step(n,**k): LOG['steps'].append({'step':n,'t':datetime.datetime.now(KST).isoformat(),**k});print('STEP',n,json.dumps(k,ensure_ascii=False)[:300],flush=True)
def sha(b): return hashlib.sha256(b).hexdigest()
def wjson(p,o): os.makedirs(os.path.dirname(p),exist_ok=True);open(p,'w').write(json.dumps(o,ensure_ascii=False,separators=(',',':')))
codes=sorted(f[:-5] for f in os.listdir(f'{SITE}/inputs') if f.endswith('.json'))
if A.codes: codes=[c for c in codes if c in A.codes.split(',')]
def fixture_quote(c):
    p=f'{AT}/raw/{ZFIX}/{c}/zeroin.json'
    return open(p,'rb').read() if os.path.exists(p) else None
if ZSIM=='all_success': codes=[c for c in codes if fixture_quote(c) is not None];A.codes=','.join(codes)  # 기존 --codes 부분집합 규칙 재사용   # 모의: fixture 보유 종목만 (없는 값을 만들지 않음)
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
        out['zeroin_origin']='replay'
        if ZSIM in ('all_fail','block_no_prev'): zq=None;out['zeroin_origin']='simulated'
        elif ZSIM in ('partial','all_success'): zq=fixture_quote(c);out['zeroin_origin']='simulated_fixture'
        if zq is None: out['zeroin']='fail (replay/simulated: none)'
    else:
        s1,nav=fetch(f'https://www.funetf.co.kr/api/public/product/view/etfnav?gijunYmd={ASOF}&fundCd={isin}&itemId={isin}&schNavStDt={st}&schNavEdDt={ASOF}')
        s2,div=fetch(f'https://www.funetf.co.kr/api/public/product/view/etfdividend?gijunYmd={ASOF}&fundCd={isin}&itemId={isin}')
        if ZSIM=='none': s3,zq=fetch(f'https://etf.zeroin.co.kr/api/quote/{c}',tries=2,to=12);out['zeroin_origin']='network'
        elif ZSIM in ('all_fail','block_no_prev'): s3,zq=None,'simulated failure (test_control)';out['zeroin_origin']='simulated'
        else:
            fq=fixture_quote(c);s3,zq=(200,fq) if fq else (None,'simulated failure: no fixture');out['zeroin_origin']='simulated_fixture'
        if s1!=200 or s2!=200: return {**out,'status':'fail','reason':f'funetf nav={s1 or nav} div={s2 or div}'},None,None,None
        if s3!=200: out['zeroin']=f'fail {zq}';zq=None
    os.makedirs(f'{RAW}/{c}',exist_ok=True)
    for n,v in (('nav.json',nav),('div.json',div),('zeroin.json',zq if out.get('zeroin_origin')=='network' else None)):
        if v is not None: open(f'{RAW}/{c}/{n}','wb').write(v);out.setdefault('sha256',{})[n]=sha(v)
    try: N=json.loads(nav,parse_float=str);D=json.loads(div,parse_float=str);Z=json.loads(zq) if zq else None
    except Exception as e: return {**out,'status':'fail','reason':'parse '+str(e)[:80]},None,None,None
    if not isinstance(N,list) or not isinstance(D,list): return {**out,'status':'fail','reason':'unexpected payload'},None,None,None
    if not N: return {**out,'status':'fail','reason':'nav empty (source returned 0 rows)'},None,None,None
    if Z is not None: out['zeroin']='ok as_of %s'%Z.get('as_of');out['zeroin_as_of']=str(Z.get('as_of'));out['zeroin_sha256']=sha(zq)
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
    # ---------- 1b ZeroIn 판정 준비 ----------
    # CORE가 실제 요구하는 ZeroIn 관련 값 = adapter.metadata()의 issuer·benchmark·fee·strategy (instrument master 또는 bundle.zeroin_metadata).
    #   비면 CORE가 issue 'zeroin_failed' 를 냄 → 이것을 '필수값 누락' 판정 기준으로 사용.
    # quote API(close·nav·net_asset·as_of)는 원천 보존용이며 CORE 입력이 아님.
    # 기준본: 직전 '검증' 승격본 raw zeroin.json(sha 일치) → 없으면 배포 사이트 data/<code>.json (대표 승인본).
    #   (run #2 auto-20261014-152635-live 는 zeroin.json 0개 → 자연히 그 이전 auto-20261014-143346-live(132) 로 거슬러 올라감)
    def prev_quotes():
        ix=json.load(open(f'{AT}/runs/index.json')) if os.path.exists(f'{AT}/runs/index.json') else []
        got={}
        for r in ix:
            rid=r['release_id']
            if not str(r.get('result','')).startswith('PASS_PROMOTED') or not os.path.exists(f'{AT}/releases/{rid}/manifest.json'): continue
            m=json.load(open(f'{AT}/releases/{rid}/manifest.json'))
            for c,h in (m.get('raw_sha256') or {}).items():
                if c in got or not h or 'zeroin.json' not in h: continue
                p=f'{AT}/raw/{rid}/{c}/zeroin.json'
                if os.path.exists(p) and sha(open(p,'rb').read())==h['zeroin.json']:
                    q=json.load(open(p));got[c]={'source_release':rid,'as_of':str(q.get('as_of')),'sha256':h['zeroin.json'],'path':f'raw/{rid}/{c}/zeroin.json'}
        return got
    PQ={} if ZSIM=='block_no_prev' else prev_quotes()
    BLANKED=None
    if ZSIM=='block_no_prev':   # 모의: 사이트 기준본에서 필수 메타가 사라진 종목 1개 (작업 사본에서만, 승격 불가)
        for c in codes:
            p_=f'{WORK}/inputs/{c}.json';b_=json.load(open(p_));z_=b_.get('zeroin_metadata') or {}
            if all(z_.get(k) for k in ('issuer','index_name','fee','strategy')): b_['zeroin_metadata']={};wjson(p_,b_);BLANKED=c;break
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
    # ---------- 3b ZeroIn 판정: fresh / reused(직전 검증 quote) / site_baseline(사이트 기준본) / missing(차단) ----------
    def zf(o): return any('zeroin_failed' in [x.get('code') for x in (v or {}).get('issues',[])] for v in (o.get('periods') or {}).values())
    ZS={};blocked=[];gap=0
    for c in codes:
        v=LOG['collect'][c]
        if v['status']!='ok' or c not in built: continue
        so=json.load(open(f'{SITE}/data/{c}.json')) if os.path.exists(f'{SITE}/data/{c}.json') else {}
        base_gap=zf(so);now_fail=zf(json.loads(built[c]));new_missing=now_fail and not base_gap
        if v.get('zeroin_as_of'): ZS[c]={'state':'fresh','as_of':v['zeroin_as_of'],'origin':v.get('zeroin_origin')}
        elif c in PQ and not new_missing: ZS[c]={'state':'reused',**PQ[c]}
        elif not new_missing: ZS[c]={'state':'site_baseline'}
        else: ZS[c]={'state':'missing','reason':'CORE 필수 메타(issuer·benchmark·fee·strategy) 누락이 사이트 기준본 대비 새로 발생'};blocked.append(c)
        ZS[c]['baseline_gap']=base_gap;gap+=base_gap;v['zeroin_state']=ZS[c]['state']
    def cnt(k): return sum(1 for z in ZS.values() if z['state']==k)
    ra=sorted({z['as_of'] for z in ZS.values() if z['state']=='reused'})
    ZSUM={'total':len(codes),'fresh':cnt('fresh'),'reused':cnt('reused'),'reused_as_of':(ra[0]+'~'+ra[-1] if len(ra)>1 else (ra[0] if ra else None)),
          'reused_from':sorted({z['source_release'] for z in ZS.values() if z['state']=='reused'}),'site_baseline':cnt('site_baseline'),'missing':cnt('missing'),
          'baseline_gap_preexisting':gap,'blocked_codes':blocked[:20],'simulated':ZSIM!='none','scenario':ZSIM,'sim_blanked':BLANKED,
          'fresh_origin':sorted({z.get('origin') for z in ZS.values() if z['state']=='fresh'}),
          'note':'quote 미취득 시 CORE 입력은 사이트 기준본 그대로; 0·추정값 대체 없음. baseline_gap_preexisting=배포본에도 이미 zeroin_failed(기존 미제공)'}
    LOG['zeroin']=ZSUM;LOG['zeroin_detail']=ZS
    step('zeroin',**{k:ZSUM[k] for k in ('total','fresh','reused','reused_as_of','site_baseline','missing','baseline_gap_preexisting','scenario')})
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
    if ZSUM['missing']: LOG['result']='BLOCKED_ZEROIN_MISSING';step('blocked',reason='ZeroIn 신규·직전 검증본 없음 + CORE 필수값이 사이트 기준본 대비 누락',codes=blocked[:20]);raise SystemExit(4)
    # ---------- 5 promote (immutable dir then pointer) ----------
    R=f'{AT}/releases/{RID}';assert not os.path.exists(R);TMP=R+'.partial';os.makedirs(f'{TMP}/data')
    files={}
    for c,s in built.items(): open(f'{TMP}/data/{c}.json','w').write(s);files[f'data/{c}.json']=sha(s.encode())
    cs=json.dumps(cat,ensure_ascii=False,separators=(',',':'));open(f'{TMP}/data/catalog.json','w').write(cs);files['data/catalog.json']=sha(cs.encode())
    man={'release_id':RID,'created_kst':datetime.datetime.now(KST).isoformat(),'mode':A.mode,'asof':ASOF,'engine_hash':cat['snapshot']['engine_hash'],
         'cutoffs':{c:json.loads(built[c])['snapshot']['data_cutoff'] for c in codes},'collect_summary':st,'files':files,
         'raw_sha256':{c:v.get('sha256') for c,v in LOG['collect'].items()},'zeroin':ZSUM,'zeroin_detail':ZS,'note':'raw sources are NOT published; hashes only'}
    wjson(f'{TMP}/manifest.json',man)
    # verify before exposing
    bad=[p for p,h in files.items() if sha(open(f'{TMP}/{p}','rb').read())!=h];assert not bad,bad
    os.rename(TMP,R)
    prevlatest=json.load(open(f'{AT}/latest.json')) if os.path.exists(f'{AT}/latest.json') else None
    lt={'release_id':RID,'path':f'releases/{RID}/','manifest_sha256':sha(open(f'{R}/manifest.json','rb').read()),'promoted_kst':datetime.datetime.now(KST).isoformat(),
        'mode':A.mode,'previous':prevlatest and prevlatest['release_id'],'max_cutoff':max(man['cutoffs'].values()),'qa':'PASS',
        'zeroin':{k:ZSUM[k] for k in ('total','fresh','reused','reused_as_of','site_baseline','missing','simulated','scenario')}}
    RES_=('PASS_PROMOTED' if ZSUM['fresh']==ZSUM['total'] else 'PASS_PROMOTED_WITH_REUSE')+('_SIM' if ZSIM!='none' else '');lt['status']=RES_
    wjson(f'{AT}/latest.json.tmp',lt);os.replace(f'{AT}/latest.json.tmp',f'{AT}/latest.json')
    LOG['result']=RES_;step('promoted',release=RID,result=RES_)
except SystemExit as e:
    pass
except Exception as e:
    LOG['result']='ERROR_NOT_PROMOTED';LOG['error']=traceback.format_exc()[-1500:];print(LOG['error'])
finally:
    os.makedirs(f'{AT}/runs',exist_ok=True)
    pub={k:v for k,v in LOG.items() if k!='collect'};pub['collect']={c:{k:v[k] for k in v if k in('status','reason','state','nav_added','div_added','new_cutoff','prev_cutoff','zeroin','zeroin_state','zeroin_origin','zeroin_as_of','overlap_mismatch','div_changed','skipped')} for c,v in LOG['collect'].items()}
    wjson(f'{AT}/runs/{RID}.json',pub)
    ix=json.load(open(f'{AT}/runs/index.json')) if os.path.exists(f'{AT}/runs/index.json') else []
    ix.insert(0,{'release_id':RID,'result':LOG['result'],'mode':A.mode,'inject':A.inject_error,'started_kst':LOG['started_kst'],
      'collect':{k:sum(1 for v in LOG['collect'].values() if v.get('state',v['status'])==k) for k in ('updated','no_change_normal','fail')},
      'qa_fail':[q['check'] for q in LOG['qa'] if not q['pass']],'zeroin':{k:v for k,v in (LOG.get('zeroin') or {}).items() if k not in('blocked_codes','note')}})
    wjson(f'{AT}/runs/index.json',ix[:200]);json.dump(LOG,open(f'{RAW}/run_log.json','w'),ensure_ascii=False,indent=1)
    if A.publish_raw and LOG['collect']:
        dst=f'{AT}/raw/{RID}';assert not os.path.exists(dst);shutil.copytree(RAW,dst)
    Z_=LOG.get('zeroin') or {}
    zl=(f"zeroin={Z_.get('fresh')}/{Z_.get('total')} reused={Z_.get('reused')}(기준일 {Z_.get('reused_as_of') or '-'}) site_baseline={Z_.get('site_baseline')} missing={Z_.get('missing')}"
        +(f" [ZeroIn 모의:{ZSIM}]" if ZSIM!='none' else (' [ZeroIn 재생(replay)]' if A.mode=='replay' else ' [ZeroIn 실네트워크]'))) if Z_ else 'zeroin=NOT_EVALUATED'
    print('RESULT',LOG['result'],RID,zl)
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        warn='' if LOG['result']=='PASS_PROMOTED' else ('> ⚠️ **정상 완료 아님** — ' + {'PASS_PROMOTED_WITH_REUSE':'ZeroIn 일부/전부 미수집, 직전 검증본·사이트 기준본 재사용','BLOCKED_ZEROIN_MISSING':'ZeroIn 필수값 누락으로 승격 차단'}.get(LOG['result'].replace('_SIM',''),LOG['result']))+'\n'
        open(os.environ['GITHUB_STEP_SUMMARY'],'a').write(f"## oneclick: {LOG['result']}\n{warn}\n- release: `{RID}`\n- ZeroIn 신규 **{Z_.get('fresh')}/{Z_.get('total')}**, 재사용 {Z_.get('reused')} (기준일 {Z_.get('reused_as_of') or '-'}, 출처 {', '.join(Z_.get('reused_from') or []) or '-'}), 사이트 기준본 {Z_.get('site_baseline')}, 누락 {Z_.get('missing')}\n- ZeroIn 출처: {'모의(test_control: '+ZSIM+')' if ZSIM!='none' else ('재생(replay)' if A.mode=='replay' else '실네트워크')}\n\n")
    sys.exit(0 if LOG['result']=='PASS_PROMOTED' else 1)
