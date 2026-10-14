"""모의/재생 시험용: 저장소 inputs 의 기존 원천 행을 FunETF 응답 형식으로 되돌려 replay 디렉터리 생성 (실수집 아님)."""
import json,os,sys
S,O=sys.argv[1],sys.argv[2]
for f in os.listdir(f'{S}/inputs'):
    if not f.endswith('.json'): continue
    b=json.load(open(f'{S}/inputs/{f}'));c=f[:-5];os.makedirs(f'{O}/{c}',exist_ok=True)
    json.dump(b['nav_rows'][:15],open(f'{O}/{c}/nav.json','w'),ensure_ascii=False)
    json.dump(b.get('distribution_rows_raw',b['distribution_rows']),open(f'{O}/{c}/div.json','w'),ensure_ascii=False)
