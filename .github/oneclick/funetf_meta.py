"""FunETF 상품 메타(JSON-LD FinancialProduct) 수집기 — 일일 경로 아님. 최초 보완/신규 종목/대표 요청 점검 시에만 수동 실행 (GrokBot).
정중한 요청: 순차 1건씩, 요청 간격 --gap 초(기본 2.5), HTTP 429 는 Retry-After 또는 30·60·120초 백오프, 최대 3회 재시도 후 'rate_limited(미확인)'.
접근 제한 우회 없음(IP/UA 위장·병렬화 없음). 출력: <out>/raw/<code>.jsonld.json(원본 FinancialProduct 노드), <out>/collect_log.json
사용: python3 funetf_meta.py --site <root> --out <dir> [--codes a,b] [--gap 2.5]"""
import argparse,json,os,re,time,hashlib,datetime,urllib.request,urllib.error
ap=argparse.ArgumentParser();ap.add_argument('--site',required=True);ap.add_argument('--out',required=True);ap.add_argument('--codes');ap.add_argument('--gap',type=float,default=2.5)
A=ap.parse_args();KST=datetime.timezone(datetime.timedelta(hours=9))
UA={'User-Agent':'Mozilla/5.0 (donnaemsae-194-test metadata check; low-rate)'}
codes=sorted(f[:-5] for f in os.listdir(f'{A.site}/inputs') if f.endswith('.json'))
if A.codes: codes=[c for c in codes if c in A.codes.split(',')]
os.makedirs(f'{A.out}/raw',exist_ok=True);LOG={'started_kst':datetime.datetime.now(KST).isoformat(),'gap_s':A.gap,'policy':'sequential; 429 backoff Retry-After|30,60,120s; max 3 retries','items':{}}
def get(u):
    att=[]
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=40) as r: att.append(r.status);return r.status,r.read(),att
        except urllib.error.HTTPError as e:
            att.append(e.code)
            if e.code==429 and i<3: ra=e.headers.get('Retry-After');time.sleep(min(int(ra),300) if ra and ra.isdigit() else (30,60,120)[i]);continue
            return e.code,None,att
        except Exception as e:
            att.append(type(e).__name__)
            if i<3: time.sleep(10*(i+1));continue
            return None,None,att
    return None,None,att
for n,c in enumerate(codes):
    p=f'{A.out}/raw/{c}.jsonld.json'
    if os.path.exists(p): LOG['items'][c]={'status':'ok','cached':True};continue
    isin=json.load(open(f'{A.site}/inputs/{c}.json'))['manifest']['isin'];u=f'https://www.funetf.co.kr/product/etf/view/{isin}'
    st,body,att=get(u);it={'isin':isin,'url':u,'http':st,'attempts':att,'retrieved_kst':datetime.datetime.now(KST).isoformat()}
    if st==200 and body:
        h=body.decode('utf-8','replace');it['html_sha256']=hashlib.sha256(body).hexdigest();fp=None;wp=None
        for m in re.finditer(r'<script[^>]*ld\+json[^>]*>(.*?)</script>',h,re.S):
            try: g=json.loads(m.group(1))
            except Exception: continue
            for node in (g.get('@graph') or [g]):
                if node.get('@type')=='FinancialProduct': fp=node
                if node.get('@type')=='WebPage': wp=node
        if fp and str(fp.get('identifier'))==c:
            fp={k:v for k,v in fp.items()};fp['additionalProperty']=[x for x in fp.get('additionalProperty',[]) if not str(x.get('propertyID','')).startswith('etf:holding')]
            json.dump({'code':c,'isin':isin,'url':u,'retrieved_kst':it['retrieved_kst'],'html_sha256':it['html_sha256'],'dateModified':(wp or {}).get('dateModified'),'FinancialProduct':fp},open(p,'w'),ensure_ascii=False,indent=1);it['status']='ok'
        else: it['status']='parse_error' if not fp else 'identifier_mismatch'
    elif st==429: it['status']='rate_limited'
    else: it['status']='http_error'
    LOG['items'][c]=it;print(n+1,c,it['status'],att,flush=True);time.sleep(A.gap)
LOG['finished_kst']=datetime.datetime.now(KST).isoformat()
import collections;LOG['counts']=dict(collections.Counter(v['status'] for v in LOG['items'].values()))
json.dump(LOG,open(f'{A.out}/collect_log.json','w'),ensure_ascii=False,indent=1);print('COUNTS',LOG['counts'])
