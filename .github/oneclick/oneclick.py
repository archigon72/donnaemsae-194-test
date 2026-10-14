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
# 시험 제어(yml 변경 없이). 정상값 none. meta_loss = 승인 메타 1종 유실 주입(작업 사본만, 승격 차단 확인용)
CTLP=os.path.join(os.path.dirname(os.path.abspath(__file__)),'test_control.json')
CTL=json.load(open(CTLP)) if os.path.exists(CTLP) else {}
SCN=CTL.get('scenario','none');assert SCN in ('none','meta_loss'),SCN
# 1회성 범위 제한: only_run_number 지정 시 그 Actions 실행 번호에서만 유효, expires_kst 이후 무효 → 그 외 실행은 none
if SCN!='none' and CTL.get('only_run_number') is not None and str(os.environ.get('GITHUB_RUN_NUMBER'))!=str(CTL['only_run_number']): SCN='none'
if SCN!='none' and CTL.get('expires_kst') and datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat()>CTL['expires_kst']: SCN='none'
STORE_P=f'{AT}/meta/product_meta_store.json'
KST=datetime.timezone(datetime.timedelta(hours=9));NOW=datetime.datetime.now(KST)
ASOF=A.asof or NOW.strftime('%Y%m%d')
RID=f"auto-{ASOF}-{NOW.strftime('%H%M%S')}-{A.mode}"+(f"-inj-{A.inject_error}" if A.inject_error else '')+(f"-scn-{SCN}" if SCN!='none' else '')
RAW=os.path.join(os.path.abspath(A.raw_dir),RID);os.makedirs(RAW,exist_ok=False)
LOG={'release_id':RID,'scenario':SCN,'mode':A.mode,'asof':ASOF,'started_kst':NOW.isoformat(),'steps':[],'collect':{},'qa':[],'result':None}
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
        nav=open(f'{d}/nav.json','rb').read();div=open(f'{d}/div.json','rb').read();zq=None
    else:
        s1,nav=fetch(f'https://www.funetf.co.kr/api/public/product/view/etfnav?gijunYmd={ASOF}&fundCd={isin}&itemId={isin}&schNavStDt={st}&schNavEdDt={ASOF}')
        s2,div=fetch(f'https://www.funetf.co.kr/api/public/product/view/etfdividend?gijunYmd={ASOF}&fundCd={isin}&itemId={isin}')
        zq=None   # ZeroIn 일일 호출 제거(2026-10-14 대표 결정). 메타는 저장된 승인본 사용
        if s1!=200 or s2!=200: return {**out,'status':'fail','reason':f'funetf nav={s1 or nav} div={s2 or div}'},None,None,None
    os.makedirs(f'{RAW}/{c}',exist_ok=True)
    for n,v in (('nav.json',nav),('div.json',div),('zeroin.json',zq)):
        if v is not None: open(f'{RAW}/{c}/{n}','wb').write(v);out.setdefault('sha256',{})[n]=sha(v)
    try: N=json.loads(nav,parse_float=str);D=json.loads(div,parse_float=str);Z=json.loads(zq) if zq else None
    except Exception as e: return {**out,'status':'fail','reason':'parse '+str(e)[:80]},None,None,None
    if not isinstance(N,list) or not isinstance(D,list): return {**out,'status':'fail','reason':'unexpected payload'},None,None,None
    if not N: return {**out,'status':'fail','reason':'nav empty (source returned 0 rows)'},None,None,None
    out['zeroin']='not_called'
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
    SRC_STATE='collection_error' if fail else ('unchanged_all' if st.get('no_change_normal',0)==len(codes) else ('partly_unchanged' if st.get('no_change_normal') else 'updated'))
    LOG['source_state']=SRC_STATE   # unchanged_all = 휴장·원천 미변경(정상), collection_error = 수집 오류(QA 차단)
    step('collect',ok=ok,fail=fail,states=st,source_state=SRC_STATE)
    # ---------- 1b 메타: 저장된 승인 메타 결합(일일 재수집 없음) ----------
    cj=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
    STORE=json.load(open(STORE_P)) if os.path.exists(STORE_P) else None
    store_ok=bool(STORE) and sha(cj(STORE['items']).encode())==STORE.get('items_sha256')
    INJ=None
    if SCN=='meta_loss':
        for c in codes:
            p_=f'{WORK}/inputs/{c}.json';b_=json.load(open(p_));z_=b_.get('zeroin_metadata') or {}
            if all(z_.get(k) for k in ('issuer','index_name','fee','strategy')): b_['zeroin_metadata']={**z_,'issuer':'','fee':''};wjson(p_,b_);INJ=c;break
    MS={};loss=[]
    for c in codes:
        wm=json.load(open(f'{WORK}/inputs/{c}.json')).get('zeroin_metadata') or {}
        it=(STORE or {}).get('items',{}).get(c) if store_ok else None
        if it:
            am=it['approved']['zeroin_metadata'];lost=[k for k,v in am.items() if v not in (None,'',{},[]) and wm.get(k) in (None,'',{},[])]
            chg=sha(cj(wm).encode())!=it['approved']['sha256']
            st_='stored' if not chg else ('lost' if lost else 'changed')
            fu=it.get('funetf') or {}
            MS[c]={'state':st_,'lost_fields':lost,'approved_sha256':it['approved']['sha256'],'funetf':fu.get('status'),'funetf_retrieved':fu.get('retrieved_kst')}
        else: MS[c]={'state':'site_baseline_only','lost_fields':[]}
        if MS[c]['state'] in ('lost','changed'): loss.append(c)
    fr=sorted({(v.get('funetf_retrieved') or '')[:10] for v in MS.values() if v.get('funetf')=='ok'})
    MSUM={'metadata':'stored' if store_ok else 'site_baseline_only','metadata_refresh':'skipped','zeroin_daily':'removed','store_built_kst':(STORE or {}).get('built_kst'),
          'store_integrity':'ok' if store_ok else ('missing' if not STORE else 'BAD'),'total':len(codes),'stored':sum(v['state']=='stored' for v in MS.values()),
          'site_baseline_only':sum(v['state']=='site_baseline_only' for v in MS.values()),'lost_or_changed':len(loss),'loss_codes':loss[:20],
          'funetf_meta_verified':sum(v.get('funetf')=='ok' for v in MS.values()),'funetf_meta_unconfirmed':sum(v.get('funetf') not in (None,'ok') for v in MS.values()),
          'funetf_meta_as_of':(fr[0]+('~'+fr[-1] if len(fr)>1 else '')) if fr else None,'injected':INJ}
    LOG['metadata']=MSUM;LOG['metadata_detail']=MS
    step('metadata',**{k:v for k,v in MSUM.items() if k!='loss_codes'})
    if A.inject_error=='collect_fail_all': fail=len(codes)
    # ---------- 3 CORE ----------
    RT=tempfile.mkdtemp(prefix='rt-');zipfile.ZipFile(f'{WORK}/runtime_source.zip').extractall(RT);sys.path[:0]=[RT,WORK];sys.dont_write_bytecode=True
    import period_bridge,presentation
    cat=json.load(open(f'{SITE}/data/catalog.json'));cat['snapshot']['snapshot_id']=RID
    built={};errs=[];INPUT_BAD=[]
    for c in codes:
        b=json.load(open(f'{WORK}/inputs/{c}.json'))
        if A.inject_error=='bad_input' and c==codes[0]: b['distribution_rows'].insert(0,dict(b['distribution_rows'][0] if b['distribution_rows'] else {},gijunYmd='20261013',divAmt='-5.0'))
        b['meta']['snapshot_id']=RID
        # 입력 오염 검사(CORE 직전 실제 투입 객체): 계산 대상 분배금 숫자·양수, 날짜 YYYYMMDD, 회차 중복 없음
        _dr=b['distribution_rows'];_bad=[r.get('gijunYmd') for r in _dr if not re.fullmatch(r'\d{8}',str(r.get('gijunYmd'))) or not re.fullmatch(r'-?\d+(\.\d+)?',str(r.get('divAmt'))) or float(r['divAmt'])<=0]
        if _bad or len({r['gijunYmd'] for r in _dr})!=len(_dr): INPUT_BAD.append({'code':c,'rows':_bad[:5],'dup':len(_dr)-len({r['gijunYmd'] for r in _dr})})
        out={'snapshot':b['meta'],'ticker':c,'periods':{},'presentations':{}}
        for k in ['1개월','6개월','1년','전체']:
            bb=copy.deepcopy(b);bb['period']=k;v=period_bridge.run_period(bb,None,None);out['periods'][k]=v;out['presentations'][k]=presentation.detail_presentation(v,bb)
        s=json.dumps(out,ensure_ascii=False,separators=(',',':'));built[c]=s
        for it in cat['items']:
            if it['ticker']==c: it['available_period']['end']=b['meta']['data_cutoff']
    step('core_build',built=len(built),engine_hash=cat['snapshot']['engine_hash'])
    # 새 필수값 공란(CORE zeroin_failed 가 배포본 대비 새로 발생) = 회귀. 기존 102 공란은 baseline_gap 으로 집계만
    def zf(o): return any('zeroin_failed' in [x.get('code') for x in (v or {}).get('issues',[])] for v in (o.get('periods') or {}).values())
    newblank=[];gap=0
    for c in codes:
        so=json.load(open(f'{SITE}/data/{c}.json')) if os.path.exists(f'{SITE}/data/{c}.json') else {}
        g=zf(so);gap+=g
        if zf(json.loads(built[c])) and not g: newblank.append(c)
    MSUM['core_new_blank']=newblank[:20];MSUM['baseline_gap_preexisting']=gap
    step('metadata_regression',new_blank=len(newblank),baseline_gap_preexisting=gap,lost_or_changed=MSUM['lost_or_changed'])
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
    LOG['input_contamination']=INPUT_BAD
    if INPUT_BAD: LOG['result']='BLOCKED_INPUT_INVALID';step('blocked',reason='CORE 입력 오염(0·음수·비숫자 분배금/날짜 형식/회차 중복)',items=INPUT_BAD[:10]);raise SystemExit(6)
    # ---------- 4b 출력 단계: 지급일 실제/예상 구분 파일 (v5.3f 형식) ----------
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));import paydate_stage as PS
    CAL=PS.KRX();SMD=json.load(open(f'{SITE}/data/management-distributions.json'));sids={x['distribution_id'] for x in SMD['items']}
    NEWR=[(c,r) for c in codes for r in (lambda b:b.get('distribution_rows_raw',b['distribution_rows']))(json.load(open(f'{WORK}/inputs/{c}.json'))) if f"{c}-{r['gijunYmd']}" not in sids]
    PDOC,PADD,PDUP=PS.build(SMD,NEWR,CAL);PCHK,PCNT=PS.checks(SMD,PDOC,PADD,CAL)
    appeared=[f"{c}-{d['date']}" for c,v in LOG['collect'].items() for d in (v.get('div_changed') or []) if d.get('new_payDt') and not d.get('old_payDt')]
    PCNT['payDt_appeared_not_applied']=appeared[:50];PDOC['calendar']={**PDOC.get('calendar',{}),'calendar_sha256_used':CAL.sha}
    LOG['paydate']={'counts':PCNT,'checks':PCHK};step('paydate',**PCNT,fails=[x['check'] for x in PCHK if not x['pass']])
    if not all(x['pass'] for x in PCHK): LOG['result']='BLOCKED_PAYDATE';raise SystemExit(5)
    if MSUM['lost_or_changed'] or MSUM['core_new_blank'] or MSUM['store_integrity']=='BAD':
        LOG['result']='BLOCKED_META_LOSS';step('blocked',reason='승인 메타 유실/변경 또는 새 필수값 공란',loss=MSUM['loss_codes'],new_blank=MSUM['core_new_blank']);raise SystemExit(4)
    # ---------- 5 promote (immutable dir then pointer) ----------
    R=f'{AT}/releases/{RID}';assert not os.path.exists(R);TMP=R+'.partial';os.makedirs(f'{TMP}/data')
    files={}
    for c,s in built.items(): open(f'{TMP}/data/{c}.json','w').write(s);files[f'data/{c}.json']=sha(s.encode())
    cs=json.dumps(cat,ensure_ascii=False,separators=(',',':'));open(f'{TMP}/data/catalog.json','w').write(cs);files['data/catalog.json']=sha(cs.encode())
    os.makedirs(f'{TMP}/aux');ps_=json.dumps(PDOC,ensure_ascii=False,indent=1);open(f'{TMP}/aux/management-distributions.json','w').write(ps_);files['aux/management-distributions.json']=sha(ps_.encode())
    man={'release_id':RID,'created_kst':datetime.datetime.now(KST).isoformat(),'mode':A.mode,'asof':ASOF,'engine_hash':cat['snapshot']['engine_hash'],
         'cutoffs':{c:json.loads(built[c])['snapshot']['data_cutoff'] for c in codes},'collect_summary':st,'files':files,
         'raw_sha256':{c:v.get('sha256') for c,v in LOG['collect'].items()},'source_state':SRC_STATE,'paydate':PCNT,'metadata':MSUM,'metadata_store_sha256':sha(open(STORE_P,'rb').read()) if os.path.exists(STORE_P) else None,'note':'raw sources are NOT published; hashes only'}
    wjson(f'{TMP}/manifest.json',man)
    # verify before exposing
    bad=[p for p,h in files.items() if sha(open(f'{TMP}/{p}','rb').read())!=h];assert not bad,bad
    os.rename(TMP,R)
    prevlatest=json.load(open(f'{AT}/latest.json')) if os.path.exists(f'{AT}/latest.json') else None
    lt={'release_id':RID,'path':f'releases/{RID}/','manifest_sha256':sha(open(f'{R}/manifest.json','rb').read()),'promoted_kst':datetime.datetime.now(KST).isoformat(),
        'mode':A.mode,'previous':prevlatest and prevlatest['release_id'],'max_cutoff':max(man['cutoffs'].values()),'qa':'PASS','source_state':SRC_STATE,'paydate':{k:PCNT[k] for k in('out','added','added_kind')},'metadata':{k:v for k,v in MSUM.items() if k not in('loss_codes','core_new_blank')}}
    RES_='PASS_PROMOTED' if MSUM['metadata']=='stored' and not MSUM['site_baseline_only'] else 'PASS_PROMOTED_WITH_REUSE';lt['status']=RES_
    wjson(f'{AT}/latest.json.tmp',lt);os.replace(f'{AT}/latest.json.tmp',f'{AT}/latest.json')
    LOG['result']=RES_;step('promoted',release=RID,result=RES_)
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
      'qa_fail':[q['check'] for q in LOG['qa'] if not q['pass']],'source_state':LOG.get('source_state'),'paydate':(LOG.get('paydate') or {}).get('counts',{}).get('out'),'metadata':{k:v for k,v in (LOG.get('metadata') or {}).items() if k not in('loss_codes','core_new_blank')}})
    wjson(f'{AT}/runs/index.json',ix[:200]);json.dump(LOG,open(f'{RAW}/run_log.json','w'),ensure_ascii=False,indent=1)
    if A.publish_raw and LOG['collect']:
        dst=f'{AT}/raw/{RID}';assert not os.path.exists(dst);shutil.copytree(RAW,dst)
    M_=LOG.get('metadata') or {}
    ml=(f"metadata={M_.get('metadata')} metadata_refresh={M_.get('metadata_refresh')} zeroin_daily={M_.get('zeroin_daily')} stored={M_.get('stored')}/{M_.get('total')} "
        f"site_baseline_only={M_.get('site_baseline_only')} lost={M_.get('lost_or_changed')} new_blank={len(M_.get('core_new_blank') or [])} funetf_meta={M_.get('funetf_meta_verified')}/{M_.get('total')}(기준일 {M_.get('funetf_meta_as_of') or '-'})") if M_ else 'metadata=NOT_EVALUATED'
    pc=(LOG.get('paydate') or {}).get('counts') or {}
    ml+=f" source_state={LOG.get('source_state')} paydate=actual {pc.get('out',{}).get('actual','-')}/estimated {pc.get('out',{}).get('estimated','-')}(+{pc.get('added','-')})"
    print('RESULT',LOG['result'],RID,ml+(f' [시험주입:{SCN}]' if SCN!='none' else ''))
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        r=LOG['result'];head={'PASS_PROMOTED':'✅ 정상'+(' (원천 미변경·휴장 가능: 새 행 0)' if LOG.get('source_state')=='unchanged_all' else ''),'PASS_PROMOTED_WITH_REUSE':'⚠️ 승격됨(경고: 일부 종목 메타 저장소 미포함 → 사이트 기준본 재사용)'}.get(r,'❌ 승격 차단/실패')
        open(os.environ['GITHUB_STEP_SUMMARY'],'a').write(f"## oneclick: {r} — {head}\n\n- release: `{RID}`\n- 메타: **metadata={M_.get('metadata')}**, metadata_refresh={M_.get('metadata_refresh')} (일일 재수집 안 함이 정상), ZeroIn 일일 호출={M_.get('zeroin_daily')}\n- 저장 승인 메타 유지 {M_.get('stored')}/{M_.get('total')} (저장소 {M_.get('store_built_kst')}), 사이트 기준본 재사용 {M_.get('site_baseline_only')}, 유실/변경 {M_.get('lost_or_changed')}, 새 공란 {len(M_.get('core_new_blank') or [])}, 기존 공란(유지) {M_.get('baseline_gap_preexisting')}\n- 원천 상태: {LOG.get('source_state')} (unchanged_all=휴장·원천 미변경 정상 / collection_error=수집 오류)\n- 지급일: 실제 {pc.get('out',{}).get('actual','-')} / 예상 {pc.get('out',{}).get('estimated','-')} (이번 신규 {pc.get('added','-')} {pc.get('added_kind','')})\n- 실패·차단 시 latest 포인터와 기존 release 는 변경되지 않음\n- FunETF 메타 검증 {M_.get('funetf_meta_verified')}/{M_.get('total')} (기준일 {M_.get('funetf_meta_as_of') or '-'}), 미확인 {M_.get('funetf_meta_unconfirmed')}\n\n")
    sys.exit(0 if LOG['result']=='PASS_PROMOTED' else 1)
