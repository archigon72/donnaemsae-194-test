"""v5.3d 동일 구조 자동 정합성 검사 (GrokBot 자체 검증). 배포 자료만 사용.
대상: data/<code>.json(카탈로그 194종) × 고정기간 4개. 기준: 배포 presentations[기간] 이
배포 presentation.py.detail_presentation(배포 periods[기간], 배포 inputs/<code>.json) 결과와 완전히 같은가.
추가 기준: distribution.history 회차 수 == presentations.distribution_history 회차 수."""
import json,sys,os
ROOT=sys.argv[1];sys.path.insert(0,ROOT);import presentation as P
cat=json.load(open(f'{ROOT}/data/catalog.json'))
codes=sorted(f[:-5] for f in os.listdir(f'{ROOT}/data') if len(f)==11 and f.endswith('.json') and f[:6].isalnum() and f[:6].upper()==f[:6])
res={'targets':len(codes),'periods':0,'mismatch':{},'history_gap':{},'missing_keys':{},'dist_keys_mismatch':{}}
for c in codes:
    d=json.load(open(f'{ROOT}/data/{c}.json'));b=json.load(open(f'{ROOT}/inputs/{c}.json'))
    for k,v in d['periods'].items():
        res['periods']+=1;dep=(d.get('presentations') or {}).get(k) or {}
        exp=json.loads(json.dumps(P.detail_presentation(v,b)))
        if dep!=exp:res['mismatch'].setdefault(c,[]).append(k)
        if any(dep.get(x)!=exp[x] for x in ('distribution_history','distribution_recent12')):res['dist_keys_mismatch'].setdefault(c,[]).append(k)
        miss=[x for x in exp if x not in dep]
        if miss:res['missing_keys'].setdefault(c,{})[k]=miss
        h=len((v.get('distribution') or {}).get('history') or []);ph=len(dep.get('distribution_history') or [])
        if h!=ph:res['history_gap'].setdefault(c,{})[k]=[h,ph]
res['summary']={'mismatch_codes':len(res['mismatch']),'mismatch_periods':sum(map(len,res['mismatch'].values())),'history_gap_codes':len(res['history_gap']),'history_gap_periods':sum(map(len,res['history_gap'].values())),'missing_keys_codes':len(res['missing_keys']),'dist_keys_mismatch_codes':len(res['dist_keys_mismatch']),'dist_keys_mismatch_periods':sum(map(len,res['dist_keys_mismatch'].values()))}
print(json.dumps(res,ensure_ascii=False,indent=1))
