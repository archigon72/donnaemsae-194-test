"""ETF82 입력 번들 복구 (v5.3e, GrokBot 자체 검증)
문제: 신규 82종 inputs/<code>.json 의 manifest.sha256 에 'nav_response.json' 키가 없어 원본 adapter 가 KeyError(adapter_failed)로 멈춘다.
      또 meta(proof_meta)의 data_cutoff 형식이 실제 CORE 실행 때 기록된 값('20261008')과 다르다('2026-10-08').
근거: 2026-10-12 실제 CORE 실행 산출물(data/<code>.json periods[*].cache = 실행 시 manifest, periods[*].proof_meta = 실행 시 meta)에
      기록된 값. 4개 기간 기록이 서로 같을 때만 복구하고, nav_rows·distribution_rows·zeroin_metadata 는 건드리지 않는다.
복구: manifest := 기록 manifest(실행 중 추가된 analysis_input_policy 제외), meta := 기록 proof_meta. 원 manifest 의 sha256/sha256_note 는
      번들 최상위 conversion_record 에 보존(Core 는 읽지 않음). data/runtime-manifest.json 의 해당 파일 sha256 갱신.
사용: python3 pipeline/restore_etf82_inputs.py <site_root> <recorded_core_output_dir>
"""
import sys,os,json,hashlib
ROOT,REC=sys.argv[1],sys.argv[2];RM=f'{ROOT}/data/runtime-manifest.json';man=json.load(open(RM));done=[];skip=[]
for f in sorted(os.listdir(f'{ROOT}/inputs')):
    p=f'{ROOT}/inputs/{f}';b=json.load(open(p))
    if 'nav_response.json' in (b['manifest'].get('sha256') or {}):continue
    d=json.load(open(f'{REC}/{f}'));caches=[];metas=[]
    for v in d['periods'].values():
        c=dict(v['cache']);c.pop('analysis_input_policy',None);caches.append(c);metas.append(v['proof_meta'])
    if any(c!=caches[0] for c in caches) or any(m!=metas[0] for m in metas):skip.append(f[:-5]);continue
    rec=caches[0]
    same={k:b['manifest'][k]==rec.get(k) for k in b['manifest'] if k not in('sha256','sha256_note')}
    assert all(same.values()),(f,same)                      # sha256 외 manifest 필드는 기록과 같아야 함
    assert {k:v for k,v in b['meta'].items() if k!='data_cutoff'}=={k:v for k,v in metas[0].items() if k!='data_cutoff'},f
    b['conversion_record']={'manifest_sha256':b['manifest'].get('sha256'),'manifest_sha256_note':b['manifest'].get('sha256_note'),'meta_data_cutoff':b['meta'].get('data_cutoff'),'restored_by':'pipeline/restore_etf82_inputs.py v5.3e'}
    b['manifest']=dict(rec);b['meta']=metas[0]
    s=json.dumps(b,ensure_ascii=False);open(p,'w').write(s)
    man['files']['inputs/'+f]=hashlib.sha256(s.encode()).hexdigest();done.append(f[:-5])
open(RM,'w').write(json.dumps(man,indent=2))
print('restored',len(done),'skipped',skip)
