"""T06 회귀 시험(GrokBot, 2026-10-19): oneclick.py 의 실제 merge() 로 증분 병합을 흉내 내어
기존 행 total=이전 응답, 새 행 total=새 응답 이 섞여도 분배 안정성이 '응답 완전성 미확인'으로 떨어지지 않는지 확인.
반대로 최신 total 이 행 수와 안 맞는(누락) 경우는 계속 판단불가여야 한다. 네트워크·사이트 파일 쓰기 없음.
사용: python3 pipeline/test_incremental_merge_total.py [site_root]"""
import sys,os,ast,json,copy,re,zipfile,tempfile,types
S=os.path.abspath(sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(__file__),'..'))
src=open(f'{S}/.github/oneclick/oneclick.py',encoding='utf-8').read();tree=ast.parse(src)
fn=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in('merge','norm_row')]
g={'copy':copy,'re':re,'RID':'test-rid','A':types.SimpleNamespace(mode='test')};exec(compile(ast.Module(body=fn,type_ignores=[]),'oneclick.merge','exec'),g)
RT=tempfile.mkdtemp();zipfile.ZipFile(f'{S}/runtime_source.zip').extractall(RT);sys.path[:0]=[RT,S];sys.dont_write_bytecode=True
import period_bridge,presentation
def stab(b):
    bb=copy.deepcopy(b);bb['period']='1년';v=period_bridge.run_period(bb,None,None);return presentation.detail_presentation(v,bb)['facts']['stability']
res=[];ok=True
def check(name,cond,detail):
    global ok;ok&=bool(cond);res.append({'case':name,'pass':bool(cond),'detail':detail})
for code in ('0052D0','441640'):
    b=json.load(open(f'{S}/inputs/{code}.json'))
    D0=b['distribution_rows'];n=len(D0);last=D0[0];N0=b['nav_rows'][0]
    # 실제 사고 재현: 직전 응답(회차 n-1, total=n-1)을 기준본으로, 새 응답(회차 n, total=n)을 merge()로 증분 병합
    T=int(str(last['total']));base=copy.deepcopy(b);base['distribution_rows']=[dict(r,total=T-1) for r in D0[1:]]
    if 'distribution_rows_raw' in base:base['distribution_rows_raw']=[dict(r,total=T-1) for r in base['distribution_rows_raw'] if r['gijunYmd']!=last['gijunYmd']]
    D=[dict(r,total=T) for r in D0];info={};nb=g['merge'](code,base,b['nav_rows'],D,info);nb['meta']=b['meta'];nb['manifest']=b['manifest'];newdiv={'total':T}
    tots=sorted({str(r.get('total')) for r in nb['distribution_rows']})
    check(f'{code} merge 결과 total 혼재',len(tots)>=2,{'totals':tots,'div_added':info['div_added']})
    check(f'{code} 기존 행 불변(diff 게이트 조건)',nb['distribution_rows'][1:]==base['distribution_rows'],{})
    s0=stab(b);s=stab(nb);check(f'{code} 혼재 total → 판단 가능',s['status']=='OK' and s==s0,{'status':s['status'],'reason':s.get('reason'),'label':s.get('label'),'n':s.get('event_count')})
    check(f'{code} 옛 규칙(전 행 total 동일)이면 실패하는 입력',len({str(r.get('total')) for r in nb['distribution_rows']})>1,{})
    check(f'{code} 현재 입력 결과',s0['status']=='OK',{'status':s0['status'],'label':s0.get('label'),'n':s0.get('event_count')})
    bad=copy.deepcopy(nb);bad['distribution_rows'][0]['total']=newdiv['total']+1   # 응답상 1건 누락
    s2=stab(bad);check(f'{code} 최신 total≠행수 → 판단불가 유지',s2.get('reason')=='distribution response completeness unverified',{'status':s2['status'],'reason':s2.get('reason')})
    bad2=copy.deepcopy(nb);bad2['distribution_rows'][3]['total']=newdiv['total']+5   # 과거 행 total 이 최신보다 큼
    s3=stab(bad2);check(f'{code} 과거 total>최신 → 판단불가',s3.get('reason')=='distribution response completeness unverified',{'status':s3['status']})
    bad3=copy.deepcopy(nb);bad3['distribution_rows'][2]['total']=None
    s4=stab(bad3);check(f'{code} total 공란 → 판단불가',s4.get('reason')=='distribution response completeness unverified',{'status':s4['status']})
print(json.dumps({'result':'PASS' if ok else 'FAIL','cases':res},ensure_ascii=False,indent=1));sys.exit(0 if ok else 1)
