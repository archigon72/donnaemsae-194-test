"""SW 캐시 구데이터 검사. phase=pre: 현재(구) 배포를 지속 프로필로 방문해 SW·캐시 확보. phase=post: 같은 프로필로 재방문해
캐시 이름 교체, 구 캐시 삭제, 페이지가 받는 data/0048J0.json·inputs/0048J0.json 이 새 내용인지, 오프라인 폴백도 새 내용인지 확인."""
import asyncio,json,sys
from playwright.async_api import async_playwright
BASE,PHASE,PROF,OUT=sys.argv[1:5]
Q="""async()=>{const ks=await caches.keys();const out={keys:ks,ctrl:!!navigator.serviceWorker.controller};for(const k of ks){const c=await caches.open(k);for(const p of ['data/0048J0.json','data/runtime-manifest.json','phase-worker.js','comparison-worker.js']){const r=await c.match(new URL(p,location.href).href);if(r){const t=await r.text();out[k+'|'+p]={len:t.length,facts:t.includes('"facts"'),health_display:t.includes('health_display'),accepted:t.includes('accepted_bundle_snapshots'),sha_nav:t.includes('nav_response.json')}}}}
const f=await (await fetch('data/0048J0.json')).text();out.fetched={facts:f.includes('"facts"'),len:f.length};return out}"""
async def main():
  async with async_playwright() as p:
    cx=await p.chromium.launch_persistent_context(PROF,executable_path='/usr/bin/google-chrome',args=['--no-sandbox'],headless=True,viewport={'width':390,'height':900})
    pg=cx.pages[0] if cx.pages else await cx.new_page()
    await pg.goto(BASE+'management.html?mode=ledger',wait_until='networkidle');await pg.wait_for_timeout(1500)
    await pg.reload(wait_until='networkidle');await pg.wait_for_timeout(1500)
    await pg.goto(BASE+'detail.html?code=0048J0',wait_until='networkidle');await pg.wait_for_timeout(2500)
    await pg.reload(wait_until='networkidle');await pg.wait_for_timeout(2500)
    await pg.evaluate("fetch('inputs/0048J0.json').then(r=>r.text())");await pg.wait_for_timeout(500)
    r={'online':await pg.evaluate(Q)}
    if PHASE=='post':
      await cx.set_offline(True);await pg.reload(wait_until='domcontentloaded');await pg.wait_for_timeout(2500)
      r['offline']=await pg.evaluate("async()=>{const t=await (await fetch('data/0048J0.json')).text();return {facts:t.includes('\"facts\"'),len:t.length}}")
      r['offline_modal_rows']=None
      await cx.set_offline(False)
    await cx.close()
  json.dump(r,open(f'{OUT}/swstale_{PHASE}.json','w'),ensure_ascii=False,indent=1);print(json.dumps(r,ensure_ascii=False)[:1500])
asyncio.run(main())
