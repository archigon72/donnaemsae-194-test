"""oneclick PASS release → 테스트 사이트 반영 (GrokBot, 1차 구축). 수동 실행 전용.
대상(한 번에 전부 또는 전무): data/<194>.json, data/catalog.json, inputs/<194>.json, data/runtime-manifest.json(snapshot·inputs sha),
references/<4>.json(참고시장, 같은 snapshot), data/management-distributions.json, data/prices.json(새 NAV 종가가 더 최신인 종목만), data/update-record.json(이전 커밋·release 기록).
auto-test/latest.json 등 auto-test/ 는 건드리지 않음. CORE·세금·원장·화면 파일 불변.
게이트: ① release 해시 검증 ② source_state≠collection_error ③ 종목별 diff 게이트(기존 NAV·분배 행 불변, 새 행은 기존 최신일 이후만,
       승인 메타 값 불변, 기준일 역행 없음) ④ 스테이징 트리에서 pipeline/validate_json.py FAIL 0.
'변경 없음'(새 행 0·메타 동일)이면 아무것도 쓰지 않고 NO_CHANGE 로 종료.
사용: python3 apply_release.py --site <repo_root> --release <release_dir> [--dry-run]"""
import argparse,json,os,sys,hashlib,shutil,subprocess,tempfile,datetime
ap=argparse.ArgumentParser();ap.add_argument('--site',required=True);ap.add_argument('--release',required=True);ap.add_argument('--dry-run',action='store_true')
A=ap.parse_args();S=os.path.abspath(A.site);R=os.path.abspath(A.release);KST=datetime.timezone(datetime.timedelta(hours=9))
sha=lambda b:hashlib.sha256(b).hexdigest();J=lambda p:json.load(open(p));OUT={'release':os.path.basename(R),'site':S}
def stop(code,msg,**k):OUT.update(result=code,reason=msg,**k);print(json.dumps(OUT,ensure_ascii=False,indent=1));sys.exit(0 if code in('APPLIED','NO_CHANGE','DRY_RUN_OK') else 2)
man=J(f'{R}/manifest.json');bad=[p for p,h in man['files'].items() if not os.path.isfile(f'{R}/{p}') or sha(open(f'{R}/{p}','rb').read())!=h]   # t174: 누락 파일도 차단(예외 종료 대신 BLOCKED)
if bad:stop('BLOCKED','release 해시 불일치',files=bad[:5])
if man.get('source_state')=='collection_error':stop('BLOCKED','수집 오류 release')
codes=sorted(f[:-5] for f in os.listdir(f'{S}/inputs') if f.endswith('.json'))
if sorted(f[:-5] for f in os.listdir(f'{R}/inputs'))!=codes:stop('BLOCKED','release 종목 구성이 사이트 194종과 다름')
RID=man['release_id'];cat=J(f'{R}/data/catalog.json')
if cat['snapshot']['snapshot_id']!=RID:stop('BLOCKED','catalog snapshot 불일치')
EMPTY=(None,'',{},[]);viol=[];chg={};newrows={};metachg={}
for c in codes:
    o=J(f'{S}/inputs/{c}.json');n=J(f'{R}/inputs/{c}.json');d=J(f'{R}/data/{c}.json');v=[]
    if d.get('ticker')!=c or d['snapshot'].get('snapshot_id')!=RID or n['meta'].get('snapshot_id')!=RID:v.append('id/snapshot')
    for key in('nav_rows','distribution_rows','distribution_rows_raw'):
        if key not in o:continue
        on,nn=o[key],n.get(key,[])
        if len(nn)<len(on) or nn[len(nn)-len(on):]!=on:v.append(key+': 기존 행 변경/삭제')
        add=nn[:len(nn)-len(on)]
        if on and any(r['gijunYmd']<=on[0]['gijunYmd'] for r in add):v.append(key+': 기존 최신일 이전 행 추가')
        if key=='nav_rows':newrows[c]=len(add)
        if key=='distribution_rows':newrows[c+'#div']=len(add)
    if n['meta'].get('data_cutoff','')<o['meta'].get('data_cutoff',''):v.append('기준일 역행')
    if {k:x for k,x in n['meta'].items() if k not in('data_cutoff','snapshot_id')}!={k:x for k,x in o['meta'].items() if k not in('data_cutoff','snapshot_id')}:v.append('meta 기타 필드 변경')
    oz=o.get('zeroin_metadata') or {};nz=n.get('zeroin_metadata') or {}
    lost=[k for k,x in oz.items() if x not in EMPTY and nz.get(k)!=x]
    if lost:v.append('승인 메타 변경/유실: '+','.join(lost))
    added=[k for k in nz if oz.get(k) in EMPTY and nz.get(k) not in EMPTY]
    if added:metachg[c]=added
    if v:viol.append({'code':c,'v':v})
    if newrows.get(c) or newrows.get(c+'#div') or added:chg[c]=1
if viol:stop('BLOCKED','diff 게이트 위반',violations=viol[:10],n=len(viol))
# T02(2026-10-19): 참고시장 4종도 같은 release(snapshot) 로 함께 반영. 없으면 화면 비교가 Snapshot mismatch → 차단
REFC=sorted(f[:-5] for f in os.listdir(f'{S}/references') if f.endswith('.json'))
if not os.path.isdir(f'{R}/references') or sorted(f[:-5] for f in os.listdir(f'{R}/references'))!=REFC:stop('BLOCKED','release 에 참고시장 4종 없음/구성 다름 → 비교 snapshot 불일치 발생')
rviol=[]
for c in REFC:
    o=J(f'{S}/references/{c}.json');n=J(f'{R}/references/{c}.json');v=[]
    if n['meta'].get('snapshot_id')!=RID:v.append('snapshot')
    for key in('nav_rows','distribution_rows'):
        on,nn=o.get(key,[]),n.get(key,[])
        if len(nn)<len(on) or nn[len(nn)-len(on):]!=on:v.append(key+': 기존 행 변경/삭제')
    if n['meta'].get('data_cutoff','')<o['meta'].get('data_cutoff',''):v.append('기준일 역행')
    if n.get('reference_identity')!=o.get('reference_identity'):v.append('identity 변경')
    if v:rviol.append({'code':c,'v':v})
if rviol:stop('BLOCKED','참고시장 diff 게이트 위반',violations=rviol)
OUT['changed_codes']=len(chg);OUT['nav_rows_added']=sum(x for k,x in newrows.items() if '#' not in k);OUT['div_rows_added']=sum(x for k,x in newrows.items() if '#' in k)
OUT['meta_filled_codes']=len(metachg);OUT['cutoff_max']=max(J(f'{R}/inputs/{c}.json')['meta']['data_cutoff'] for c in codes)
if not chg:stop('NO_CHANGE','새 행 0 · 메타 변경 0 — 반영할 내용 없음(업데이트 성공 아님)')
# ---- 스테이징 ----
ST=tempfile.mkdtemp(prefix='apply-');shutil.copytree(f'{S}/pipeline',f'{ST}/pipeline');os.makedirs(f'{ST}/data');os.makedirs(f'{ST}/inputs')
W={}   # rel path -> bytes
for c in codes:
    W[f'data/{c}.json']=open(f'{R}/data/{c}.json','rb').read();W[f'inputs/{c}.json']=open(f'{R}/inputs/{c}.json','rb').read()
W['data/catalog.json']=open(f'{R}/data/catalog.json','rb').read()
W['data/management-distributions.json']=open(f'{R}/aux/management-distributions.json','rb').read()
for c in REFC:W[f'references/{c}.json']=open(f'{R}/references/{c}.json','rb').read()
rm=J(f'{S}/data/runtime-manifest.json');rm['snapshot']=cat['snapshot']
for c in codes:rm['files'][f'inputs/{c}.json']=sha(W[f'inputs/{c}.json'])
for c in REFC:rm['files'][f'references/{c}.json']=sha(W[f'references/{c}.json'])
W['data/runtime-manifest.json']=json.dumps(rm,indent=2).encode()
pr=J(f'{S}/data/prices.json');pupd=[]
for it in pr['items']:
    n=json.loads(W[f"inputs/{it['code']}.json"]);r=n['nav_rows'][0];td=f"{r['gijunYmd'][:4]}-{r['gijunYmd'][4:6]}-{r['gijunYmd'][6:]}"
    if r.get('clsp') not in EMPTY and td>(it.get('trade_date') or ''):
        it.update(price=str(int(round(float(r['clsp'])))),trade_date=td,as_of=None,market_status='closed',price_type='close',fetched_at=man.get('created_kst'),source='FUNETF_ETFNAV_CLSP_ONECLICK_'+RID);pupd.append(it['code'])
W['data/prices.json']=json.dumps(pr,ensure_ascii=False,separators=(',',':')).encode();OUT['prices_updated']=len(pupd)
os.makedirs(f'{ST}/references')
for p,b in W.items():open(f'{ST}/{p}','wb').write(b)
vp=subprocess.run([sys.executable,f'{ST}/pipeline/validate_json.py',ST],capture_output=True,text=True)
try:vj=json.loads(vp.stdout);vf=vj['counts'].get('FAIL',0)
except Exception:vf=-1;vj={'raw':vp.stdout[-300:]+vp.stderr[-300:]}
OUT['validate']=vj.get('counts',vj)
if vf!=0:stop('BLOCKED','스테이징 검증 실패',fail_by_check=vj.get('fail_by_check'))
prev=subprocess.run(['git','-C',S,'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
rec={'release_id':RID,'applied_kst':datetime.datetime.now(KST).isoformat(),'previous_commit':prev,'revert_hint':'git revert <이 반영 커밋> (force push 금지)',
     'changed_codes':len(chg),'nav_rows_added':OUT['nav_rows_added'],'div_rows_added':OUT['div_rows_added'],'meta_filled_codes':len(metachg),'prices_updated':len(pupd),'cutoff_max':OUT['cutoff_max'],'source_state':man.get('source_state')}
W['data/update-record.json']=json.dumps(rec,ensure_ascii=False,indent=1).encode()
if A.dry_run:shutil.rmtree(ST);stop('DRY_RUN_OK','검증 통과(쓰기 없음)',record=rec)
# ---- 반영: 전부 임시파일에 쓴 뒤 일괄 교체(중간 실패 시 원복) ----
bak={}
try:
    for p,b in W.items():open(f'{S}/{p}.applytmp','wb').write(b)
    for p in W:
        q=f'{S}/{p}'
        if os.path.exists(q):bak[p]=open(q,'rb').read()
        os.replace(q+'.applytmp',q)
except Exception as e:
    for p,b in bak.items():open(f'{S}/{p}','wb').write(b)
    for p in W:
        if os.path.exists(f'{S}/{p}.applytmp'):os.remove(f'{S}/{p}.applytmp')
    stop('ROLLED_BACK','반영 중 오류 → 원복: '+str(e)[:120])
shutil.rmtree(ST);stop('APPLIED','반영 완료(커밋은 수동, 일괄 1커밋)',record=rec,meta_filled_sample=dict(list(metachg.items())[:3]))
