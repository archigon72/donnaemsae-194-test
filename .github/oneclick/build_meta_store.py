"""승인 메타 저장소 생성 (GrokBot). 일일 경로 아님.
입력: 사이트 inputs/<code>.json 의 zeroin_metadata(기존 승인 메타, 원본 그대로 보존) + funetf_meta.py 산출 raw JSON-LD(있을 때만).
규칙: effective(표시·CORE 입력) = 기존 승인값. FunETF 값은 'funetf' 별도 필드(필드별 검증상태)로만 추가 → 기존 102 공란 미충전, 기존값 미변경.
      FunETF 필드는 파싱·의미 검증된 것만 status=verified. 빈 값/파싱 오류/식별자 불일치/429 는 unverified 로 남김.
출력: <out>/product_meta_store.json, <out>/compare_existing_vs_funetf.csv, <out>/field_coverage.csv, <out>/issuer_map.json
사용: python3 build_meta_store.py --site <root> --raw <funetf_meta out dir> --out <dir>"""
import argparse,json,os,re,hashlib,csv,collections,datetime
ap=argparse.ArgumentParser();ap.add_argument('--site',required=True);ap.add_argument('--raw',required=True);ap.add_argument('--out',required=True);A=ap.parse_args()
os.makedirs(A.out,exist_ok=True);sha=lambda b:hashlib.sha256(b).hexdigest()
cj=lambda o:json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))
codes=sorted(f[:-5] for f in os.listdir(f'{A.site}/inputs') if f.endswith('.json'))
LOGP=f'{A.raw}/collect_log.json';CL=json.load(open(LOGP))['items'] if os.path.exists(LOGP) else {}
FEE=[('total_fee_pct',r'(?<!합성)총\s*보수\s*연\s*([0-9]+(?:\.[0-9]+)?)\s*%'),('synthetic_total_fee_pct',r'합성총보수\s*연\s*([0-9]+(?:\.[0-9]+)?)\s*%'),('effective_burden_pct',r'실부담비율\s*연\s*([0-9]+(?:\.[0-9]+)?)\s*%')]
def parse(c):
    p=f'{A.raw}/raw/{c}.jsonld.json'
    if not os.path.exists(p):
        st=(CL.get(c) or {}).get('status','not_attempted');return {'status':st,'attempts':(CL.get(c) or {}).get('attempts')},None
    raw=open(p,'rb').read();R=json.loads(raw);fp=R['FinancialProduct'];ap_={x.get('propertyID'):x.get('value') for x in fp.get('additionalProperty',[])}
    f={};fs={}
    def put(k,v,ok,why=None): f[k]=v if ok else None;fs[k]='verified' if ok else ('blank' if v in (None,'') else 'parse_error:'+str(why))
    prov=(fp.get('provider') or {});put('issuer_short',prov.get('name'),bool(prov.get('name')));f['issuer_url']=prov.get('url')
    fee=fp.get('feesAndCommissionsSpecification') or '';f['fee_text']=fee or None
    parts=[x.strip() for x in fee.split(',') if x.strip()]
    for k,rx in FEE:
        m=[re.fullmatch(rx.replace('(?<!합성)',''),x) if k!='total_fee_pct' else re.fullmatch(r'총\s*보수\s*연\s*([0-9]+(?:\.[0-9]+)?)\s*%',x) for x in parts];m=[x for x in m if x]
        put(k,m[0].group(1) if len(m)==1 else None,len(m)==1,'not exactly one match' if fee else None)
    ix=ap_.get('etf:underlyingIndex');put('underlying_index',ix,bool(ix))
    rk=ap_.get('etf:riskGrade');m=re.fullmatch(r'([1-6])등급\s*\((.+)\)',str(rk or ''));put('risk_grade',int(m.group(1)) if m else None,bool(m),'format');f['risk_text']=rk
    ld=ap_.get('etf:listingDate');put('listing_date',ld,bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}',str(ld or ''))),'format')
    return {'status':'ok','retrieved_kst':R['retrieved_kst'],'dateModified':R.get('dateModified'),'url':R['url'],'html_sha256':R['html_sha256'],'raw_sha256':sha(raw),'fields':f,'field_status':fs},R
items={};pairs=collections.defaultdict(set);ev=collections.defaultdict(list)
for c in codes:
    b=json.load(open(f'{A.site}/inputs/{c}.json'));zm=b.get('zeroin_metadata') or {}
    fu,_=parse(c)
    items[c]={'name':b['manifest'].get('name') or zm.get('name'),'isin':b['manifest']['isin'],'approved':{'zeroin_metadata':zm,'sha256':sha(cj(zm).encode()),'source':zm.get('source') or 'site inputs zeroin_metadata (기존 승인본)'},'funetf':fu}
    if fu['status']=='ok' and fu['fields'].get('issuer_short') and zm.get('issuer'): pairs[fu['fields']['issuer_short']].add(zm['issuer']);ev[fu['fields']['issuer_short']].append(c)
imap={k:{'formal':sorted(v)[0] if len(v)==1 else None,'candidates':sorted(v),'evidence_codes':ev[k][:10],'status':'verified_unique' if len(v)==1 else 'ambiguous'} for k,v in pairs.items()}
for c,it in items.items():
    fu=it['funetf']
    if fu['status']=='ok':
        s=fu['fields'].get('issuer_short');m=imap.get(s)
        fu['fields']['issuer_formal']=m['formal'] if m and m['status']=='verified_unique' else None
        fu['field_status']['issuer_formal']='verified(map: 기존 승인 formal↔FunETF short 1:1, 근거 '+','.join(m['evidence_codes'][:3])+')' if m and m['formal'] else 'unmapped'
    # effective = 기존 승인값 (FunETF로 덮지 않고 공란도 채우지 않음)
    it['effective']={'source':'approved','fields':{k:it['approved']['zeroin_metadata'].get(k) for k in ('issuer','index_name','fee','strategy','listing_date')}}
store={'schema':'donnaemsae.product_meta_store.v1','built_kst':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).isoformat(),
 'rules':{'effective':'기존 승인 메타 그대로(유지). FunETF는 별도 funetf 필드, 필드별 verified만 의미 확정.','blank_policy':'기존 공란은 채우지 않음; 새 공란·유실만 회귀 차단','refresh':'일일 수집 안 함(metadata_refresh=skipped). 최초 보완·신규 종목·변경 발견·대표 요청 시 funetf_meta.py 수동 실행',
  'fee_split':'feesAndCommissionsSpecification 을 쉼표로 분리 후 "총 보수 연 X%"→total, "합성총보수 연 X%"→synthetic, "실부담비율 연 X%"→effective_burden; 각 1회 정확 일치만 verified',
  'index':'FunETF etf:underlyingIndex 값만 기록; 기존 index_name/benchmark 와 동일 가정 안 함(비교표 참조)'},
 'issuer_map':imap,'items':items}
store['items_sha256']=sha(cj(items).encode())
open(f'{A.out}/product_meta_store.json','w').write(json.dumps(store,ensure_ascii=False,indent=1,sort_keys=True))
json.dump(imap,open(f'{A.out}/issuer_map.json','w'),ensure_ascii=False,indent=1,sort_keys=True)
# 비교표
def norm(s): return re.sub(r'\s+','',str(s or '')).lower()
with open(f'{A.out}/compare_existing_vs_funetf.csv','w',newline='') as fh:
    w=csv.writer(fh);w.writerow(['code','name','field','existing_approved','funetf','funetf_status','compare'])
    for c,it in items.items():
        z=it['approved']['zeroin_metadata'];fu=it['funetf'];F=fu.get('fields') or {};S=fu.get('field_status') or {}
        rows=[('issuer',z.get('issuer'),F.get('issuer_formal'),S.get('issuer_formal')),('issuer_short','',F.get('issuer_short'),S.get('issuer_short')),
              ('fee(total)',z.get('fee'),F.get('total_fee_pct'),S.get('total_fee_pct')),('synthetic_total_fee','',F.get('synthetic_total_fee_pct'),S.get('synthetic_total_fee_pct')),
              ('effective_burden','',F.get('effective_burden_pct'),S.get('effective_burden_pct')),('index',z.get('index_name'),F.get('underlying_index'),S.get('underlying_index')),
              ('risk_grade','',F.get('risk_text'),S.get('risk_grade')),('listing_date',z.get('listing_date'),F.get('listing_date'),S.get('listing_date'))]
        for f,e,v,s in rows:
            if fu['status']!='ok': cmp='funetf_'+fu['status']
            elif not e: cmp='existing_blank(유지·미충전)'
            elif v is None: cmp='funetf_unverified'
            elif f=='fee(total)': cmp='same' if abs(float(e)-float(v))<1e-9 else 'DIFF'
            elif f=='listing_date': cmp='same' if str(e).replace('.','-')==v else 'DIFF'
            else: cmp='same' if norm(e)==norm(v) else 'DIFF'
            w.writerow([c,it['name'],f,e,v,s or fu['status'],cmp])
# 필드 커버리지
fields=['issuer_short','issuer_formal','total_fee_pct','synthetic_total_fee_pct','effective_burden_pct','underlying_index','risk_grade','listing_date']
with open(f'{A.out}/field_coverage.csv','w',newline='') as fh:
    w=csv.writer(fh);w.writerow(['field','verified','not_available_or_parse(page ok)','unconfirmed(429/http/not attempted)','total'])
    for f in fields:
        ok=sum(1 for it in items.values() if it['funetf']['status']=='ok' and (it['funetf']['field_status'].get(f,'')).startswith('verified'))
        pg=sum(1 for it in items.values() if it['funetf']['status']=='ok')-ok
        w.writerow([f,ok,pg,len(items)-ok-pg,len(items)])
print(json.dumps({'items':len(items),'funetf_status':dict(collections.Counter(it['funetf']['status'] for it in items.values())),'issuer_map':{k:v['status'] for k,v in imap.items()},'items_sha256':store['items_sha256']},ensure_ascii=False))
