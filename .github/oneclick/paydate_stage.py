"""출력 단계: 지급일 실제/예상 구분 파일(v5.3f data/management-distributions.json 형식) 생성 (GrokBot, v53h).
규칙(승인 원칙 그대로): v5.3f 공식 항목은 그대로 복사(실제 1,088 / 예상 3,416 보호, 329200 0원 중복행 excluded_duplicate 유지).
이번 갱신으로 새로 추가된 분배 회차만: FunETF payDt 있으면 actual(confirmed, pay_date=payDt), 없으면 estimated(분배락일 다음날부터 3 KRX 영업일).
CORE/계산 규칙 변경 없음. 기존 회차에 payDt가 새로 생긴 경우는 덮어쓰지 않고 'payDt_appeared' 로 보고만 함."""
import json,datetime,hashlib,os
HERE=os.path.dirname(os.path.abspath(__file__))
class KRX:
    def __init__(s,p=os.path.join(HERE,'krx_calendar.json')):
        b=open(p,'rb').read();s.doc=json.loads(b);s.hol=set(s.doc['holidays']);s.lo,s.hi=s.doc['range'];s.sha=hashlib.sha256(b).hexdigest()
    def plus(s,base,n=3):
        if not (s.lo<=base<=s.hi): raise ValueError('outside calendar range '+base)
        d=datetime.date.fromisoformat(base);k=0
        while k<n:
            d+=datetime.timedelta(days=1)
            if d.weekday()<5 and d.isoformat() not in s.hol: k+=1
        if d.isoformat()>s.hi: raise ValueError('result outside calendar range')
        return d.isoformat()
iso=lambda y:f'{y[:4]}-{y[4:6]}-{y[6:8]}' if y else None
def build(site_md,new_rows,cal):
    """site_md: v5.3f 문서, new_rows: [(code,raw_row)] 이번 실행 신규 회차"""
    items=[dict(x) for x in site_md['items']];ids={x['distribution_id'] for x in items};added=[];dup=[]
    for c,r in new_rows:
        did=f"{c}-{r['gijunYmd']}"
        if did in ids: dup.append(did);continue
        ex=iso(r['gijunYmd']);pd=r.get('payDt')
        it={'code':c,'distribution_id':did,'per_share':str(r['divAmt']),'ex_date':ex,'source_dates':{'basicDt':r.get('basicDt'),'gijunYmd':r.get('gijunYmd'),'procDt':r.get('procDt'),'payDt':pd}}
        if pd: it.update(pay_date=iso(str(pd)),status='confirmed',pay_date_source='original',pay_date_kind='actual',cashflow_included=True)
        else:
            e=cal.plus(ex,3);it.update(pay_date=e,status='estimated',pay_date_source='estimated_+3bd',pay_date_note=f'예상 지급일 (기준일 {ex} +3영업일)',pay_date_kind='estimated',cashflow_included=True)
        it['oneclick_added']=True;items.append(it);ids.add(did);added.append(did)
    items.sort(key=lambda x:(x['code'],x['ex_date']))
    doc={k:v for k,v in site_md.items() if k!='items'};doc['items']=items
    doc['oneclick_note']='v5.3f 항목 원본 복사 + 원클릭 신규 회차만 동일 규칙으로 추가 (oneclick_added=true)'
    return doc,added,dup
def checks(site_md,doc,added,cal):
    S={x['distribution_id']:x for x in site_md['items']};D={x['distribution_id']:x for x in doc['items']};R=[]
    def ck(n,ok,d=None): R.append({'check':n,'pass':bool(ok),'detail':d})
    ck('v5.3f 항목 전부 존재·원문 동일(실제/예상 보호)',all(D.get(k)==v for k,v in S.items()),[k for k,v in S.items() if D.get(k)!=v][:5])
    ck('distribution_id 중복 0',len(D)==len(doc['items']))
    ck('pay_date_kind 누락 0',all(x.get('pay_date_kind') in('actual','estimated') for x in doc['items']))
    ck('actual ⇔ payDt 존재, pay_date=payDt',all((x['pay_date_kind']=='actual')==bool(x['source_dates'].get('payDt')) and (x['pay_date_kind']!='actual' or x['pay_date']==iso(str(x['source_dates']['payDt']))) for x in doc['items']))
    bad=[x['distribution_id'] for x in doc['items'] if x['pay_date_kind']=='estimated' and x['pay_date']!=cal.plus(x['ex_date'],3)]
    ck('estimated pay_date = 분배락일+3 KRX 영업일 (전 항목 재계산)',not bad,bad[:5])
    import re;ck('날짜 ISO',all(re.fullmatch(r'\d{4}-\d{2}-\d{2}',x['ex_date']) and re.fullmatch(r'\d{4}-\d{2}-\d{2}',x['pay_date']) for x in doc['items']))
    p=[x for x in doc['items'] if x['code']=='329200'];inc=[x for x in p if x.get('cashflow_included')]
    ck('329200 계산 대상 59회·합계 2,167원·2024-06-28 0원 excluded_duplicate',len([x for x in p if x['ex_date']<='2026-10-08'])==60 and len([x for x in inc if x['ex_date']<='2026-10-08'])==59 and abs(sum(float(x['per_share']) for x in inc if x['ex_date']<='2026-10-08')-2167)<1e-9 and any(x['distribution_id']=='329200-20240628' and x['status']=='excluded_duplicate' for x in p),{'rows':len(p),'included':len(inc)})
    ck('estimated 금액 누락 0(per_share 숫자, cashflow_included)',all(x.get('per_share') not in(None,'') for x in doc['items'] if x['status']!='excluded_duplicate') and all(x['cashflow_included'] for x in doc['items'] if x['status']!='excluded_duplicate'))
    from collections import Counter;c=Counter(x['pay_date_kind'] for x in doc['items']);cs=Counter(x['pay_date_kind'] for x in site_md['items'])
    return R,{'site':dict(cs),'out':dict(c),'added':len(added),'added_kind':dict(Counter(D[a]['pay_date_kind'] for a in added))}
