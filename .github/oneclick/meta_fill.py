"""FunETF 우선 메타 보완 (GrokBot, 1차 구축). 기존 승인 zeroin_metadata 의 공란 필드만 FunETF verified 값으로 채움.
   기존 값 변경 금지. issuer 는 CORE 운용사 라우팅(core_issuer_key)을 바꾸므로 채우지 않음(대표 판단 항목). strategy 는 FunETF 미제공 → 승인 문구 유지."""
import json,sys,os
def fill(zm,item):
    """FunETF verified 값으로 기존 승인 메타의 '공란' 필드만 채움. 기존 값은 절대 변경하지 않음."""
    zm=dict(zm or {});fu=(item or {}).get('funetf') or {}
    if fu.get('status')!='ok':return zm,{}
    F=fu.get('fields') or {};S=fu.get('field_status') or {};done={}
    def ok(k):return str(S.get(k,'')).startswith('verified') and F.get(k) not in (None,'')
    rules=[('fee','total_fee_pct',lambda v:v),('index_name','underlying_index',lambda v:v),('listing_date','listing_date',lambda v:v.replace('-','.'))]
    for dst,src,cv in rules:
        if zm.get(dst) in (None,'') and ok(src):zm[dst]=cv(F[src]);done[dst]=src
    return zm,done
if __name__=='__main__':
    S=json.load(open(sys.argv[2]))['items'];n=0
    for f in os.listdir(sys.argv[1]):
        p=f'{sys.argv[1]}/{f}';b=json.load(open(p));z,d=fill(b.get('zeroin_metadata'),S.get(f[:-5]))
        if d:b['zeroin_metadata']=z;open(p,'w').write(json.dumps(b,ensure_ascii=False));n+=1
    print('filled',n)
