import json,datetime as dt,collections,statistics as st,sys
from fractions import Fraction
R='/workspace/r194/';D=json.load(open(R+'data/management-distributions.json'));C=json.load(open(R+'.github/oneclick/krx_calendar.json'))
H=set(C['holidays']);RS,RE=C['range'];CUT=D['data_cutoff']
d=dt.date.fromisoformat
def bd(x):return x.weekday()<5 and x.isoformat() not in H
def plus3(ex):
  x=d(ex);n=0
  while n<3:
    x+=dt.timedelta(1)
    if x.isoformat()>RE:return None
    if bd(x):n+=1
  return x.isoformat()
# 1 검증: 기존 estimated pay_date 재현
est=[i for i in D['items'] if i.get('pay_date_kind')=='estimated']
mis=[i['distribution_id'] for i in est if plus3(i['ex_date'])!=i['pay_date']]
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
cat=json.load(open(R+'data/catalog.json'))['items'];codes=[x['ticker'] for x in cat]
y1=(d(CUT).replace(year=d(CUT).year-1)).isoformat()
out={};notes=[]
for c in codes:
  ev=sorted(by.get(c,[]),key=lambda i:i['ex_date'])
  if not ev:out[c]={'cadence':'none/irregular','n12':0,'events':[],'reason':'분배 이력 없음'};continue
  n=len([i for i in ev if y1<i['ex_date']<=CUT])
  cad='weekly' if n>=40 else 'monthly' if n>=10 else 'quarterly' if n>=3 else 'semi/annual' if n>=1 else 'none/irregular'
  if cad=='none/irregular':out[c]={'cadence':cad,'n12':n,'events':[],'reason':'직전 12개월 분배 없음 → 주기 추정 불가'};continue
  last3=ev[-3:];ps_sum=sum(Fraction(i['per_share']) for i in last3)
  step=1 if cad=='monthly' else max(1,min(12,round(12/n)))
  offs=[mend_offset(i['ex_date']) for i in ev[-3:]];k=collections.Counter(offs).most_common();k=max(k,key=lambda t:(t[1],offs[::-1].index(t[0])*-1))[0]
  lx=d(ev[-1]['ex_date']);y,m=lx.year,lx.month;E=[];drop=0
  while True:
    m+=step
    while m>12:m-=12;y+=1
    if f'{y}-{m:02d}'>RE[:7]:break
    ex=ex_in_month(y,m,k);p=plus3(ex)
    if p is None:drop+=1;continue
    E.append({'ex_date':ex,'pay_date':p})
  r={'cadence':cad,'n12':n,'step_months':step,'month_end_offset_bd':k,'last_ex':ev[-1]['ex_date'],'events':E,'dropped_out_of_calendar':drop}
  if cad=='monthly':r.update(per_share_sum=str(ps_sum.numerator/ps_sum.denominator) if ps_sum.denominator==1 or (10**12*ps_sum).denominator==1 else None,per_share_n=3,basis=[i['distribution_id'] for i in last3])
  out[c]=r
# per_share_sum exact decimal check
for c,r in out.items():
  if r.get('cadence')=='monthly':
    s=sum(Fraction(i['per_share']) for i in sorted(by[c],key=lambda i:i['ex_date'])[-3:]);r['per_share_sum']=format(s.numerator/s.denominator,'f') if False else str(s) if s.denominator==1 else None
    if r['per_share_sum'] is None:
      import decimal;r['per_share_sum']=str(decimal.Decimal(s.numerator)/decimal.Decimal(s.denominator))
doc={'schema':'dnmuat194-fd-forecast-v1','generated':'2026-10-14','data_cutoff':CUT,'calendar':{'id':C['calendar_id'],'version':C['calendar_version'],'range':C['range'],'note_2027':C['note_2027']},
 'rule':{'cadence':'직전 12개월(데이터 기준일 2026-10-08 기준, 이전 1년 초과~기준일 이하) 분배 횟수: ≥40 weekly, ≥10 monthly, ≥3 quarterly, ≥1 semi/annual, 0 none (백테스트와 동일)','amount':'monthly만: 최근 3회 주당 분배금 평균(옵션 C). 그 외: 금액 미정','ex_date':'마지막 실제 배당락월 + 주기(monthly 1개월, 기타 round(12/횟수)개월); 일자 = 최근 3회의 월말 기준 영업일 오프셋 최빈값(동률 시 최근)','pay_date':'예상 배당락일 다음날부터 3번째 KRX 영업일(기존 +3영업일 규칙·krx_calendar)','precedence':'실제/기존 자료 회차가 있는 마지막 배당락일 이후만 예측 → 중복 없음'},
 'self_check':{'estimated_pay_date_reproduced':len(est)-len(mis),'estimated_total':len(est),'mismatch':mis[:10]},'items':out}
json.dump(doc,open(sys.argv[1],'w'),ensure_ascii=False,separators=(',',':'))
cc=collections.Counter(r['cadence'] for r in out.values());print(cc,'plus3 repro',len(est)-len(mis),'/',len(est));print(json.dumps(out['329200'],ensure_ascii=False)[:500]);print(sum(r.get('dropped_out_of_calendar',0) for r in out.values()))
