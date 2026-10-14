"""v5.3e 배포 JSON 자동 검증 (GrokBot 자체 검증). 배포 자료만 사용.
사용: python3 pipeline/validate_json.py <site_root> [regenerated_dir]
각 검사 결과는 PASS / FAIL / SKIP(정상 공란 규칙으로 해당 없음). 로그 끝에 집계와 FAIL 목록."""
import sys,os,json,datetime,collections
from decimal import Decimal as D,getcontext
getcontext().prec=40
ROOT=sys.argv[1];REGEN=sys.argv[2] if len(sys.argv)>2 else None
cat=json.load(open(f'{ROOT}/data/catalog.json'));CNT=collections.Counter();FAILS=[];SK=collections.Counter()
def chk(name,ok,ctx,skip=False):
    if skip:CNT['SKIP']+=1;SK[name]+=1;return
    CNT['PASS' if ok else 'FAIL']+=1
    if not ok:FAILS.append({'check':name,**ctx})
def num(x):
    try:D(str(x));return True
    except Exception:return False
import re
def iso(x):
    if not isinstance(x,str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}',x):return False
    try:datetime.date.fromisoformat(x);return True
    except Exception:return False
def shift_month(d,n):
    m=d.year*12+d.month-1-n;y,mo=divmod(m,12);import calendar
    return d.replace(year=y,month=mo+1,day=min(d.day,calendar.monthrange(y,mo+1)[1]))
codes=sorted(f[:-5] for f in os.listdir(f'{ROOT}/inputs') if f.endswith('.json'))
catcodes={i.get('code') or i.get('ticker') for i in cat['items']}
for c in codes:
    d=json.load(open(f'{ROOT}/data/{c}.json'));b=json.load(open(f'{ROOT}/inputs/{c}.json'))
    ctx={'code':c}
    chk('코드: 파일명=ticker=번들 ticker, 카탈로그 포함',d['ticker']==c==b['ticker'] and c in catcodes,ctx)
    chk('기준점: snapshot=카탈로그 snapshot',d['snapshot']==cat['snapshot'],ctx)
    chk('키: periods/presentations 4개 기간',sorted(d['periods'])==sorted(d['presentations'])==sorted(['1개월','6개월','1년','전체']),ctx)
    for k,v in d['periods'].items():
        p=d['presentations'][k];x={'code':c,'period':k};dist=v.get('distribution') or {};hist=dist.get('history') or []
        chk('기간 ticker 일치',v['ticker']==c and (v.get('metadata') or {}).get('ticker')==c,x)
        chk('proof_meta = 입력 번들 meta',v.get('proof_meta')==b['meta'],x)
        chk('표시 키 5종 존재(reinvestment_effect_pp, health_display, distribution_history, distribution_recent12, facts)',all(q in p for q in('reinvestment_effect_pp','health_display','distribution_history','distribution_recent12','facts')),x)
        ap=v.get('available_period') or {}
        chk('available_period 날짜 형식(ISO)',iso(ap.get('start','')) and iso(ap.get('end','')),x)
        ok=v['status']=='OK'
        if ok:
            a=v['actual_period']
            chk('actual_period ⊂ available_period',ap['start']<=a['start']<=a['end']<=ap['end'],x)
            chk('series 관측수 = actual_period.observations',len(v['series'])==a['observations'],x)
            pf=v['performance']
            chk('performance 수치 형식',all(num(pf[q]) for q in('nav_change','navtr_change','distribution_sum','nav_first','nav_last')),x)
            s=sum((D(str(r['amount'])) for r in hist if a['start']<=r['date']<=a['end']),D(0))
            chk('distribution_sum = 분석기간 회차합',D(str(pf['distribution_sum']))==s,{**x,'sum':str(s),'v':pf['distribution_sum']})
            e=D(str(pf['navtr_change']))-D(str(pf['nav_change']))
            chk('reinvestment_effect_pp = navtr_change − nav_change(독립 재계산)',p.get('reinvestment_effect_pp') is not None and D(str(p['reinvestment_effect_pp']))==e,x)
            h=v['health']
            chk('health 수치 형식·상태',h and h.get('status')=='OK' and num(h['raw_mdd']) and num(h['navtr_mdd']) and D(str(h['raw_mdd']))<=0 and D(str(h['navtr_mdd']))<=0,x)
            chk('health_display 구조(raw/navtr)',isinstance(p.get('health_display'),dict) and set(p['health_display'])=={'raw','navtr'},x)
        else:
            iss={i['code'] for i in v.get('issues') or []}
            chk('비정상 상태 사유 명시(insufficient_period/core_failed 등)',bool(iss-{'zeroin_failed','benchmark_unavailable'}),{**x,'issues':sorted(iss)})
            chk('정상 공란: 성과·건전성 미산출 시 reinvestment_effect_pp=null',p.get('reinvestment_effect_pp') is None,x)
            for q in('series','performance','health'):SK['정상 공란(기간 부족/Core 미실행): '+q]+=1;CNT['SKIP']+=1
        if not dist:chk('분배 블록',False,x);continue
        last=datetime.date.fromisoformat(dist['ratio_as_of']);f12=str(shift_month(last,12));f6=str(shift_month(last,6))
        e12=[r for r in hist if f12<r['date']<=str(last)]
        s12=sum((D(str(r['amount'])) for r in e12),D(0))
        chk('요약 sum12 = 최근 12개월 회차합',D(str(dist['sum12']))==s12,{**x,'calc':str(s12),'v':dist['sum12']})
        chk('sum_recent6 + sum_previous6 = sum12',D(str(dist['sum_recent6']))+D(str(dist['sum_previous6']))==D(str(dist['sum12'])),x)
        if hist:
            chk('latest = 마지막 회차',dist['latest']==sorted(hist,key=lambda r:r['date'])[-1],x)
        else:chk('latest',True,x,skip=True)
        if dist.get('ratio') is not None:
            chk('ratio = sum12 / ratio_nav × 100',abs(D(str(dist['ratio']))-D(str(dist['sum12']))/D(str(dist['ratio_nav']))*100)<D('1e-30'),x)
        else:chk('ratio(12개월 미만 정상 공란)',dist.get('ratio_status')=='insufficient_history',x,skip=dist.get('ratio_status')=='insufficient_history')
        ph=p.get('distribution_history') or []
        chk('전체기간 표시 회차 = CORE 회차(수·날짜·금액)',sorted((r['date'],str(r['amount'])) for r in ph)==sorted((r['date'],str(r['amount'])) for r in hist),{**x,'core':len(hist),'shown':len(ph)})
        r12=p.get('distribution_recent12') or []
        chk('최근12 막대 합 = sum12',sum((D(str(r['amount'])) for r in r12),D(0))==s12,{**x,'bars':len(r12),'sum':str(sum((D(str(r['amount'])) for r in r12),D(0))),'sum12':str(s12)})
        for q in('cache','proof_meta'):
            dc=(v.get(q) or {}).get('data_cutoff') or ''
            chk(f'{q}.data_cutoff 형식 ISO(YYYY-MM-DD)',iso(dc),{**x,'value':dc})
if REGEN:
    for c in codes:
        chk('CORE 재생성 = 배포(바이트 동일)',open(f'{ROOT}/data/{c}.json','rb').read()==open(f'{REGEN}/{c}.json','rb').read(),{'code':c})
byname=collections.Counter(f['check'] for f in FAILS)
print(json.dumps({'targets':{'codes':len(codes),'periods':len(codes)*4},'counts':dict(CNT),'fail_by_check':dict(byname),'skip_by_rule':dict(SK),'fails':FAILS},ensure_ascii=False,indent=1))
