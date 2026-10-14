"""직접지정 기간 실행 확인: 기간 버튼 '직접지정' → 시작/종료일 입력 → 적용 → 결과/오류 기록."""
import asyncio,json,sys
from playwright.async_api import async_playwright
BASE,TAG,OUT=sys.argv[1],sys.argv[2],sys.argv[3];CASES=[x.split(':') for x in sys.argv[4].split(',')]
async def main():
  res={};errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=await b.new_context(viewport={'width':390,'height':900},device_scale_factor=2,service_workers='block');pg=await cx.new_page()
    pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:errs.append(str(e)))
    for code,s,e in CASES:
      await pg.goto(BASE+'detail.html?code='+code,wait_until='networkidle');await pg.wait_for_selector('[data-open-distribution-history]',timeout=60000)
      await pg.locator('button',has_text='직접지정').first.click();await pg.wait_for_timeout(300)
      await pg.fill('#real-start',s);await pg.fill('#real-end',e);await pg.click('[data-real-apply]')
      try:await pg.wait_for_function("()=>{const c=document.querySelector('.period-caption');const st=document.querySelector('.definition[role=status]');return (c&&c.textContent.includes('%s'))||document.body.innerText.match(/실패|오류|mismatch|불가/)}"%s,timeout=180000)
      except Exception as x:pass
      await pg.wait_for_timeout(1500)
      r=await pg.evaluate("()=>({caption:document.querySelector('.period-caption')?.textContent,status:document.querySelector('header .definition[role=status]')?.textContent,err:document.querySelector('#real-date-error:not([hidden])')?.textContent,alerts:[...document.querySelectorAll('[role=alert]:not([hidden])')].map(x=>x.textContent).filter(Boolean).slice(0,3),dist:[...document.querySelectorAll('.dist-card strong')].map(x=>x.textContent),perf:document.body.innerText.match(/NAV-TR[^\\n]{0,40}/g)?.slice(0,3)})")
      res[code+':'+s+'~'+e]=r;print(code,json.dumps(r,ensure_ascii=False)[:400])
      await pg.screenshot(path=f'{OUT}/{TAG}_custom_{code}.png')
    await b.close()
  res['_errors']=errs;json.dump(res,open(f'{OUT}/{TAG}_custom.json','w'),ensure_ascii=False,indent=1);print('errs',errs[:5])
asyncio.run(main())
