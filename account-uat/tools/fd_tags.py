#!/usr/bin/env python3
"""FunETF 상품 상세 상단 태그(월말배당/월중배당) 수집 (account-uat 미래배당 주기 판정 1순위 근거). 읽기 전용 수집, 저율(1.5초 간격).
실행: python3 account-uat/tools/fd_tags.py  (저장소 루트에서) → account-uat/tools/fd-monthly-tags.json. 이후 fd_gen.py 재실행."""
import json,os,re,time,datetime as dt,urllib.request
ROOT=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..'))
codes=[x['ticker'] for x in json.load(open(os.path.join(ROOT,'data/catalog.json')))['items']]
out={}
for c in codes:
  isin=json.load(open(os.path.join(ROOT,'inputs',c+'.json')))['manifest']['isin'];url='https://www.funetf.co.kr/product/etf/view/'+isin
  try:
    h=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0 (donnaemsae-194-test tag check; low-rate)'}),timeout=30).read().decode('utf-8','replace')
    m=re.search(r'<div class="product-tag">(.*?)</div>',h,re.S);tags=[re.sub(r'\s+',' ',t).strip() for t in re.findall(r'<span[^>]*>(.*?)</span>',m.group(1),re.S)] if m else []
    mt=[t for t in tags if t in('월말배당','월중배당')]
    out[c]={'isin':isin,'tags':tags,'monthly_tag':mt[0] if mt else None,'status':'ok' if m else 'tag_block_missing'}
  except Exception as e:out[c]={'isin':isin,'tags':[],'monthly_tag':None,'status':'error:'+type(e).__name__}
  time.sleep(1.5)
doc={'schema':'dnmuat194-fd-monthly-tags-v1','source':'FunETF 상품 상세 https://www.funetf.co.kr/product/etf/view/<ISIN> .product-tag','collected_at':dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).isoformat(timespec='seconds'),'items':out}
json.dump(doc,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'fd-monthly-tags.json'),'w'),ensure_ascii=False,indent=0)
from collections import Counter;print(Counter(v['monthly_tag'] for v in out.values()),Counter(v['status'] for v in out.values()))
