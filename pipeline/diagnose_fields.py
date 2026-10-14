"""v5.3e 필드별 결손 진단 (GrokBot 자체 검증)
비교: BEFORE = 수정 전 배포 JSON(c3f21ae), CORE = 복구 파이프라인 재생성 JSON(원본 Core 재실행), 그룹 = 112(기존) / 82(신규, inputs meta.snapshot_id=ETF82_Grok_20261011)
대상: UI가 실제 읽는 필드(real-detail.js, sections13/45-display.js, facts-display.js) × 194종 × 고정기간 4 = 776 칸.
판정: 있음 / 정상 공란(규칙 명시) / 결손. 결손 원인: CORE에도 없음 = 재생성에서도 없음, 변환 유실 = 재생성에는 있음(BEFORE에 없음).
'UI 누락'(JSON에 있으나 화면 미표시)은 화면 검사(screen_check.py)에서 별도 판정."""
import sys,os,json,collections
BEFORE,CORE,INPUTS=sys.argv[1:4]
def g(o,path):
    for k in path.split('.'):
        if not isinstance(o,dict) or k not in o:return KeyError
        o=o[k]
    return o
def blank(x):return x is None or x==''or x==[]or x=={} or x is KeyError
F=[('periods','status'),('periods','metadata.name'),('periods','metadata.issuer'),('periods','metadata.benchmark'),('periods','metadata.fee'),('periods','metadata.strategy'),('periods','metadata.type'),('periods','metadata.metadata_as_of'),('periods','metadata.links'),
('periods','cache.data_cutoff'),('periods','proof_meta.data_cutoff'),('periods','available_period.start'),('periods','actual_period.start'),('periods','series'),
('periods','performance.nav_change'),('periods','performance.navtr_change'),('periods','performance.distribution_sum'),
('periods','health.status'),('periods','health.raw_mdd'),('periods','health.navtr_mdd'),('periods','health.drawdown_reduction_pp'),
('periods','distribution.latest'),('periods','distribution.sum12'),('periods','distribution.sum_recent6'),('periods','distribution.sum_previous6'),('periods','distribution.monthly_average'),('periods','distribution.ratio'),('periods','distribution.ratio_nav'),('periods','distribution.ratio_as_of'),('periods','distribution.history'),
('presentations','reinvestment_effect_pp'),('presentations','health_display'),('presentations','distribution_history'),('presentations','distribution_recent12'),('presentations','facts'),('presentations','facts.stability.label'),('presentations','facts.movement.label'),('presentations','facts.feature.label')]
def normal(sec,path,v,p,b):
    """정상 공란 규칙. 문자열 사유를 돌려주면 정상, None이면 결손."""
    st=v.get('status');iss={i['code'] for i in v.get('issues')or[]};d=v.get('distribution')or{}
    if st!='OK' and 'insufficient_period' in iss and (path.startswith(('performance','health','actual_period','series')) or path in('reinvestment_effect_pp',)):return '기간 부족(insufficient_period) → Core 미실행'
    if path=='status' :return None
    if path in('distribution.latest','distribution.history','distribution_history') and not b['distribution_rows']:return '분배 0회(원천 분배 행 0)'
    if path=='distribution_recent12' and not [r for r in (d.get('history')or[]) ]:return '분배 0회'
    if path in('distribution.ratio','distribution.monthly_average') and d.get('ratio_status')=='insufficient_history':return '12개월 미만(ratio_status=insufficient_history)'
    if path.startswith('metadata.') and path!='metadata.name' and 'zeroin_failed' in iss:return None   # 원천 미제공: 결손으로 집계(CORE에도 없음)
    if path=='facts.stability.label' and g(p,'facts.stability.status')=='unavailable':return '기존 규칙상 산출 불가: '+str(g(p,'facts.stability.reason'))
    if path=='facts.movement.label' and g(p,'facts.movement.status')=='unavailable':return '기존 규칙상 산출 불가: '+str(g(p,'facts.movement.reason'))
    if path=='facts.feature.label' and g(p,'facts.feature')in(None,{},KeyError):return None
    if path=='distribution_recent12' and d.get('history'):return '최근 12개월 창에 회차 없음' if not g(p,'distribution_history') else None
    return None
codes=sorted(f[:-5] for f in os.listdir(INPUTS) if f.endswith('.json'))
grp={c:('82' if json.load(open(f'{INPUTS}/{c}.json'))['meta']['snapshot_id']=='ETF82_Grok_20261011' else '112') for c in codes}
T=collections.defaultdict(lambda:{'cells':0,'present':0,'normal':0,'missing_before':0,'cause':collections.Counter(),'fixed':0,'unresolved_codes':set(),'missing_codes':set(),'normal_reasons':collections.Counter(),'format':collections.Counter()})
for c in codes:
    B=json.load(open(f'{BEFORE}/{c}.json'));C=json.load(open(f'{CORE}/{c}.json'));b=json.load(open(f'{INPUTS}/{c}.json'))
    for k in C['periods']:
        for sec,path in F:
            t=T[(grp[c],sec+'.'+path)];t['cells']+=1
            vb=g(B[sec].get(k,{}),path);vc=g(C[sec].get(k,{}),path)
            if path.endswith('data_cutoff') and isinstance(vb,str):t['format']['YYYYMMDD' if len(vb)==8 else 'YYYY-MM-DD']+=1
            if not blank(vb):t['present']+=1;continue
            why=normal(sec,path,C['periods'][k],C['presentations'][k],b)
            if why:t['normal']+=1;t['normal_reasons'][why]+=1;continue
            t['missing_before']+=1;t['missing_codes'].add(c)
            if blank(vc):t['cause']['CORE 산출물에도 없음']+=1;t['unresolved_codes'].add(c)
            else:t['cause']['산출물에는 있고 표시 변환에서 유실']+=1;t['fixed']+=1
rows=[]
for (gname,field),t in sorted(T.items(),key=lambda x:(x[0][1],x[0][0])):
    rows.append({'group':gname,'field':field,'cells':t['cells'],'present_before':t['present'],'normal_blank':t['normal'],'missing_before':t['missing_before'],'cause':dict(t['cause']),'fixed':t['fixed'],'unresolved':t['missing_before']-t['fixed'],
                 'example_codes':sorted(t['missing_codes'])[:5],'unresolved_codes':sorted(t['unresolved_codes']),'normal_reasons':dict(t['normal_reasons']),'format':dict(t['format'])})
print(json.dumps({'groups':collections.Counter(grp.values()),'rows':rows},ensure_ascii=False,indent=1))
