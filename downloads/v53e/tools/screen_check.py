"""분배 요약/전체기간·재투자 효과·건전성(MDD)·facts 화면 캡처와 'JSON 있음 → 화면 표시' 대조 (UI 누락 판정)."""
import asyncio,json,sys,re,urllib.request
from playwright.async_api import async_playwright
BASE,TAG,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
CASES=[x.split(':') for x in (sys.argv[4] if len(sys.argv)>4 else '0004G0:,0048J0:,0238P0:,329200:전체,0203D0:1년,0203D0:전체').split(',')]
async def main():
  res={};errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=await b.new_context(viewport={'width':390,'height':900},device_scale_factor=2,service_workers='block');pg=await cx.new_page()
    pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:errs.append(str(e)))
    for code,per in CASES:
      await pg.goto(BASE+'detail.html?code='+code,wait_until='networkidle');await pg.wait_for_selector('[data-open-distribution-history]',timeout=60000);await pg.wait_for_timeout(600)
      if per:
        btn=pg.locator('.period-buttons button, button[aria-pressed]',has_text=per).first
        dis=await btn.get_attribute('disabled') if await btn.count() else 'missing'
        if dis is None:await btn.click();await pg.wait_for_timeout(1500)
        else:res[f'{code}:{per}']={'period_button':'disabled' if dis is not None else 'missing'}
      key=f'{code}:{per or "기본"}';r=res.setdefault(key,{})
      r['period_active']=await pg.evaluate("[...document.querySelectorAll('button.active[aria-pressed=true]')].map(b=>b.textContent).join('|')")
      await pg.evaluate("document.querySelectorAll('details.panel').forEach(d=>d.open=true)");await pg.add_style_tag(content='nav,.portal-nav{visibility:hidden!important}');await pg.wait_for_timeout(300)
      await pg.evaluate("()=>{for(const e of document.querySelectorAll('body *')){const s=getComputedStyle(e);if(s.position==='fixed'&&e.getBoundingClientRect().bottom>=innerHeight-2)e.style.visibility='hidden'}}")
      for sec in ('dist','capital','mdd','facts'):
        el=pg.locator('#'+sec);r[sec]=(await el.inner_text())[:900]
        await el.screenshot(path=f'{OUT}/{TAG}_{code}_{per or "기본"}_{sec}.png')
      await pg.click('[data-open-distribution-history]');await pg.wait_for_timeout(300)
      r['modal_rows']=await pg.evaluate("document.querySelectorAll('#distribution-history-dialog tbody tr td:nth-child(3)').length");await pg.keyboard.press('Escape')
      print(key,r['period_active'],'modal',r['modal_rows'],'| capital:',re.sub(r'\s+',' ',r['capital'])[:160],'| facts:',re.sub(r'\s+',' ',r['facts'])[:200])
    await b.close()
  res['_errors']=errs;json.dump(res,open(f'{OUT}/{TAG}_screens.json','w'),ensure_ascii=False,indent=1);print('errs',errs[:3])
asyncio.run(main())
