"""배포 JSON(A) ↔ 생성 JSON(B) 비교. 바이트 동일 / 의미 동일 / 최상위·기간별 키 단위 차이를 출력."""
import sys,os,json
A,B=sys.argv[1],sys.argv[2];res={'byte_same':[],'semantic_same':[],'diff':{}}
for f in sorted(x for x in os.listdir(B) if x.endswith('.json')):
    a=open(f'{A}/{f}').read();b=open(f'{B}/{f}').read()
    if a==b:res['byte_same'].append(f[:-5]);continue
    x,y=json.loads(a),json.loads(b)
    if x==y:res['semantic_same'].append(f[:-5]);continue
    d={}
    for k in set(x)|set(y):
        if k in('periods','presentations'):
            for p in set(x.get(k,{}))|set(y.get(k,{})):
                xa,ya=x.get(k,{}).get(p,{}),y.get(k,{}).get(p,{})
                ks=sorted(q for q in set(xa)|set(ya) if xa.get(q)!=ya.get(q))
                if ks:d[f'{k}.{p}']=ks
        elif x.get(k)!=y.get(k):d[k]='differs'
    res['diff'][f[:-5]]=d
res['summary']={'files':len(res['byte_same'])+len(res['semantic_same'])+len(res['diff']),'byte_same':len(res['byte_same']),'semantic_same_only':len(res['semantic_same']),'diff':len(res['diff'])}
print(json.dumps(res,ensure_ascii=False,indent=1))
