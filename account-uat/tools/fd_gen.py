#!/usr/bin/env python3
"""미래배당 예상 사전계산 (account-uat 격리 전용). 실행: python3 account-uat/tools/fd_gen.py  (저장소 루트에서)
입력: data/management-distributions.json(v5.3f, 읽기 전용) · .github/oneclick/krx_calendar.json(공식/라이브러리 달력, 읽기 전용)
      · account-uat/tools/krx_official/<연도>.json (선택: KRX 공식 휴장일 공지 수동 등록 → 해당 연도 status=official)
      · 2028년 이후: python-holidays 0.106 financial_holidays('XKRX') 계산(주말·법정 고정 공휴일·음력 설/추석·대체휴일·연말 휴장) → status=estimated
출력: account-uat/fd-calendar.json(연도별 상태·출처·휴일) · account-uat/fd-forecast.json(예상 회차, 지급일 달력 상태 포함)
공식 연도가 추가되면 이 스크립트를 다시 실행하면 그 연도의 예상 지급일·라벨이 자동 재계산된다. 원장·CORE·기존 자료는 쓰지 않는다."""
import json,datetime as dt,collections,os,sys,glob,decimal
from fractions import Fraction
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
UAT=os.path.join(ROOT,'account-uat');HORIZON_EX_END='2028-12';CAL_END=2029
D=json.load(open(os.path.join(ROOT,'data/management-distributions.json')));K=json.load(open(os.path.join(ROOT,'.github/oneclick/krx_calendar.json')))
CUT=D['data_cutoff'];d=dt.date.fromisoformat
years={}
for y in range(2006,CAL_END+1):
  if f'{y}-12-31'<=K['range'][1]:
    years[y]={'status':'official' if y<=2026 else 'estimated','source':K['calendar_version']+(' · '+K['note_2027'] if y==2027 else ''),'holidays':{k:v for k,v in K['holidays'].items() if k.startswith(str(y))}}
need=[y for y in range(2006,CAL_END+1) if y not in years]
if need:
  import holidays
  assert holidays.__version__=='0.106',holidays.__version__
  fh=holidays.financial_holidays('XKRX',years=need)
  for y in need: years[y]={'status':'estimated','source':'python-holidays 0.106 financial_holidays("XKRX") 계산값(주말 제외·법정 고정일·음력 설/추석·대체휴일·선거일·연말 휴장) — KRX 미공표 추정','holidays':{k.isoformat():v for k,v in sorted(fh.items()) if k.year==y}}
for f in sorted(glob.glob(os.path.join(UAT,'tools','krx_official','*.json'))):
  o=json.load(open(f));y=int(o['year']);years[y]={'status':'official','source':o.get('source','KRX 공식 휴장일 공지 (수동 등록)'),'holidays':o['holidays']}
H=set(k for y in years.values() for k in y['holidays']);LAST=f'{max(years)}-12-31'
def bd(x):return x.weekday()<5 and x.isoformat() not in H
def plus3(ex):
  x=d(ex);n=0
  while n<3:
    x+=dt.timedelta(1)
    if x.isoformat()>LAST:raise SystemExit('달력 범위 부족: '+ex)
    if bd(x):n+=1
  return x.isoformat()
def span_status(ex,pay):
  ys=range(d(ex).year,d(pay).year+1);return 'official' if all(years[y]['status']=='official' for y in ys) else 'estimated'
est=[i for i in D['items'] if i.get('pay_date_kind')=='estimated'];mis=[i['distribution_id'] for i in est if plus3(i['ex_date'])!=i['pay_date']]
def mend_offset(ex):
  x=d(ex);last=(x.replace(day=28)+dt.timedelta(4)).replace(day=1)-dt.timedelta(1);k=0;y=x
  while True:
    y+=dt.timedelta(1)
    if y>last:break
    if bd(y):k+=1
  return k
def ex_in_month(y,m,k):
  last=(dt.date(y,m,28)+dt.timedelta(4)).replace(day=1)-dt.timedelta(1);x=last
  while not bd(x):x-=dt.timedelta(1)
  for _ in range(k):
    x-=dt.timedelta(1)
    while not bd(x):x-=dt.timedelta(1)
  return x.isoformat()
by=collections.defaultdict(list)
for i in D['items']:
  if i.get('cashflow_included')!=False and i['status'] in('confirmed','estimated'):by[i['code']].append(i)
codes=[x['ticker'] for x in json.load(open(os.path.join(ROOT,'data/catalog.json')))['items']]
y1=d(CUT).replace(year=d(CUT).year-1).isoformat();out={}
# T03(2026-10-19 확정): 월배당 판정 1순위 = FunETF 상품 페이지 '월말배당'/'월중배당' 태그(fd_tags.py 수집본), 태그 없거나 불명확 → 최근 실제 배당락이 연속 월·간격 25~40일.
# 충돌(태그 월배당인데 간격 불일치)은 태그 우선 + monthly_conflict 기록. 상장 후 90일 예외 없음. 예상 주당 = 최근 min(3, 양(+) 회차 수) 평균, 0원 회차 제외, 0회면 금액 미정.
TAGP=os.path.join(UAT,'tools','fd-monthly-tags.json');TAGS=json.load(open(TAGP))['items'] if os.path.exists(TAGP) else {}
def interval_monthly(ev):
  e=[i for i in ev if Fraction(i['per_share'])>0][-3:]
  if len(e)<2:return None
  for a_,b_ in zip(e,e[1:]):
    x,y=d(a_['ex_date']),d(b_['ex_date']);mg=(y.year-x.year)*12+y.month-x.month;gap=(y-x).days
    if mg!=1 or not 25<=gap<=40:return False
  return True
for c in codes:
  ev=sorted(by.get(c,[]),key=lambda i:i['ex_date'])
  n=len([i for i in ev if y1<i['ex_date']<=CUT])
  cad='weekly' if n>=40 else 'monthly' if n>=10 else 'quarterly' if n>=3 else 'semi/annual' if n>=1 else 'none/irregular'
  tg=TAGS.get(c) or {};tag=tg.get('monthly_tag') if tg.get('status')=='ok' else None;iv=interval_monthly(ev);basis_m=None
  if cad not in('weekly','none/irregular'):
    if tag:basis_m='funetf_tag:'+tag
    elif iv:basis_m='interval_25_40d'
    if basis_m:cad='monthly'
  if not ev or cad=='none/irregular':out[c]={'cadence':'none/irregular','n12':n,'events':[],'reason':'분배 이력 없음' if not ev else '직전 12개월 분배 없음 → 주기 추정 불가'};continue
  step=1 if cad=='monthly' else max(1,min(12,round(12/n)))
  offs=[mend_offset(i['ex_date']) for i in ev[-3:]];cnt=collections.Counter(offs);top=max(cnt.values());k=[o for o in reversed(offs) if cnt[o]==top][0]
  lx=d(ev[-1]['ex_date']);y,m=lx.year,lx.month;E=[]
  while True:
    m+=step
    while m>12:m-=12;y+=1
    if f'{y}-{m:02d}'>HORIZON_EX_END:break
    ex=ex_in_month(y,m,k);p=plus3(ex);E.append({'ex_date':ex,'pay_date':p,'cal':span_status(ex,p)})
  r={'cadence':cad,'n12':n,'step_months':step,'month_end_offset_bd':k,'last_ex':ev[-1]['ex_date'],'events':E}
  if cad=='monthly':
    r['monthly_basis']=basis_m or 'n12>=10'
    if tag and iv is False:r['monthly_conflict']='태그 월배당 · 최근 간격 불일치 → 태그 우선, 점검 대상'
    pos=[i for i in ev if Fraction(i['per_share'])>0][-3:]
    if pos:
      s=sum(Fraction(i['per_share']) for i in pos);r.update(per_share_sum=str(s) if s.denominator==1 else str(decimal.Decimal(s.numerator)/decimal.Decimal(s.denominator)),per_share_n=len(pos),basis=[i['distribution_id'] for i in pos])
  out[c]=r
cal={'schema':'dnmuat194-fd-calendar-v1','generated_by':'account-uat/tools/fd_gen.py','years':{str(y):{'status':v['status'],'source':v['source'],'holiday_count':len(v['holidays']),'holidays':v['holidays']} for y,v in sorted(years.items()) if y>=2024}}
doc={'schema':'dnmuat194-fd-forecast-v2','data_cutoff':CUT,'horizon':{'ex_end':HORIZON_EX_END,'calendar_end':LAST,'ui_year_max':int(HORIZON_EX_END[:4])},
 'calendar_status':{str(y):v['status'] for y,v in sorted(years.items()) if y>=2024},
 'rule':{'cadence':'직전 12개월 배당락 횟수: ≥40 weekly, ≥10 monthly, ≥3 quarterly, ≥1 semi/annual, 0 none','monthly':'1순위 FunETF 월말배당/월중배당 태그(tools/fd-monthly-tags.json) · 태그 없으면 최근 실제 배당락 연속 월·간격 25~40일 · 충돌 시 태그 우선(monthly_conflict) · 그 외 직전 12개월 ≥10회','amount':'monthly: 최근 min(3, 양(+) 회차 수) 주당 평균, 0원 제외, 0회면 금액 미정. 기타 금액 미정','ex_date':'마지막 실제 배당락월+주기, 월말 영업일 오프셋 최빈값','pay_date':'예상 배당락 다음날부터 3번째 KRX 영업일','cal':'official=지급일 산정 구간 전체가 공식 달력 연도 / estimated=추정 휴일 연도 포함 → 화면 추정 표시'},
 'self_check':{'estimated_pay_date_reproduced':len(est)-len(mis),'estimated_total':len(est),'mismatch':mis[:10]},'items':out}
o=sys.argv[1] if len(sys.argv)>1 else UAT
json.dump(cal,open(os.path.join(o,'fd-calendar.json'),'w'),ensure_ascii=False,separators=(',',':'));json.dump(doc,open(os.path.join(o,'fd-forecast.json'),'w'),ensure_ascii=False,separators=(',',':'))
print(json.dumps({'status':doc['calendar_status'],'reproduced':f"{len(est)-len(mis)}/{len(est)}",'events':sum(len(r['events']) for r in out.values()),'est_cal':sum(e['cal']=='estimated' for r in out.values() for e in r['events'])},ensure_ascii=False))
