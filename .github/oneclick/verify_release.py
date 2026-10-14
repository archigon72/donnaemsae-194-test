"""격리 release 무결성 검증: latest.json → manifest sha → 모든 파일 sha / release_id 일치. 로컬 경로 또는 HTTPS 기준."""
import json,sys,hashlib,urllib.request,time,os
B=sys.argv[1].rstrip('/')+'/'
def get(p):
    if B.startswith('http'):
        with urllib.request.urlopen(B+p+('?cb=%d'%time.time()),timeout=60) as r: return r.read()
    return open(B+p,'rb').read()
sha=lambda b:hashlib.sha256(b).hexdigest()
L=json.loads(get('latest.json'));mb=get(L['path']+'manifest.json');M=json.loads(mb);bad=[]
if sha(mb)!=L['manifest_sha256']: bad.append('manifest sha != latest.manifest_sha256')
if M['release_id']!=L['release_id']: bad.append('release_id mismatch')
for p,h in M['files'].items():
    b=get(L['path']+p)
    if sha(b)!=h: bad.append('sha mismatch '+p)
    elif p.startswith('data/') and p!='data/catalog.json' and json.loads(b)['snapshot']['snapshot_id']!=M['release_id']: bad.append('snapshot_id != release_id '+p)
print(json.dumps({'release_id':L['release_id'],'files':len(M['files']),'bad':bad[:10],'verdict':'PASS' if not bad else 'FAIL'},ensure_ascii=False));sys.exit(1 if bad else 0)
