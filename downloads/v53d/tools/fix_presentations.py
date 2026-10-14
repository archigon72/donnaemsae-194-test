"""v5.3d 최소 수정: data/<code>.json 의 presentations[기간]에 distribution_history / distribution_recent12 가
빠진 종목만, 배포된 presentation.py(detail_presentation)를 배포된 periods[기간](view model)·inputs/<code>.json 에
그대로 적용한 결과의 이 두 키만 추가한다. 기존 키·값과 periods(Core 결과)는 바꾸지 않는다. 회차·금액 생성 없음."""
import json,sys,os
ROOT=sys.argv[1];sys.path.insert(0,ROOT);import presentation as P
KEYS=('distribution_history','distribution_recent12');changed=[];kept={}
for f in sorted(os.listdir(f'{ROOT}/data')):
    if not(len(f)==11 and f.endswith('.json') and f[:6].upper()==f[:6] and f[:6].isalnum()):continue
    c=f[:6];path=f'{ROOT}/data/{f}';s=open(path).read();d=json.loads(s)
    if all(all(k in (d.get('presentations') or {}).get(p,{}) for k in KEYS) for p in d['periods']):continue
    b=json.load(open(f'{ROOT}/inputs/{c}.json'))
    for p,v in d['periods'].items():
        exp=json.loads(json.dumps(P.detail_presentation(v,b)));cur=d['presentations'].setdefault(p,{})
        for k,val in cur.items():
            if exp.get(k)!=val:kept.setdefault(c,set()).add(k)   # 기존 키는 그대로 둠(범위 밖, 잔여 문제로 보고)
        for k in KEYS:
            if k not in cur:cur[k]=exp[k]
    open(path,'w').write(json.dumps(d,ensure_ascii=False));changed.append(c)
print(len(changed),' '.join(changed));print('existing keys left unchanged though recompute differs:',len(kept),sorted({k for v in kept.values() for k in v}))
