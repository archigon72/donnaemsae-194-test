import asyncio,json,sys
from playwright.async_api import async_playwright
BASE,TAG,OUT=sys.argv[1],sys.argv[2],sys.argv[3];CODES=sys.argv[4].split(',') if len(sys.argv)>4 else ['0048J0']
async def main():
  res={};errs=[]
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=await b.new_context(viewport={'width':390,'height':900},device_scale_factor=2,service_workers='block');pg=await cx.new_page()
    pg.on('console',lambda m:errs.append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:errs.append(str(e)))
    for c in CODES:
      await pg.goto(BASE+'detail.html?code='+c,wait_until='networkidle')
      await pg.wait_for_selector('[data-open-distribution-history]',timeout=60000);await pg.wait_for_timeout(800)
      sec=pg.locator('.dist-cards').first;await sec.scroll_into_view_if_needed()
      summ=await pg.evaluate("()=>[...document.querySelectorAll('.dist-card')].map(e=>e.innerText.replace(/\\s+/g,' '))")
      bars=await pg.evaluate("()=>{const h=document.querySelector('.dist-chart-heading');let n=h?.nextElementSibling;return {html_len:n?.outerHTML.length||0,rects:n?n.querySelectorAll('rect.bar, rect[data-index], .chart-bar').length:0,text:(n?.innerText||'').slice(0,200),rows:n?.dataset?.rows?JSON.parse(n.dataset.rows).length:null}}")
      if c=='0048J0':
        bx=await pg.evaluate("()=>{const a=document.querySelector('.dist-cards').getBoundingClientRect(),z=document.querySelector('.dist-chart-note').getBoundingClientRect();return [a.top+scrollY-10,z.bottom+scrollY+10]}")
        await pg.add_style_tag(content='nav,.portal-nav,[class*=bottom-nav],[class*=tabbar]{visibility:hidden!important}');await pg.evaluate("()=>{for(const e of document.querySelectorAll('body *')){const p=getComputedStyle(e).position;if(p==='fixed'&&e.getBoundingClientRect().bottom>=innerHeight-2)e.style.visibility='hidden'}}")
        await pg.screenshot(path=f'{OUT}/{TAG}_summary_history.png',full_page=True,clip={'x':0,'y':bx[0],'width':390,'height':bx[1]-bx[0]})
      await pg.click('[data-open-distribution-history]');await pg.wait_for_selector('#distribution-history-dialog[open]');await pg.wait_for_timeout(300)
      rows=await pg.evaluate("()=>[...document.querySelectorAll('#distribution-history-dialog tbody tr')].map(r=>[...r.cells].map(c=>c.innerText))")
      if c=='0048J0':await pg.locator('#distribution-history-dialog').screenshot(path=f'{OUT}/{TAG}_modal.png')
      await pg.keyboard.press('Escape')
      res[c]={'summary':summ,'bars':bars,'modal_rows':rows}
    await b.close()
  res['_console_errors']=errs
  json.dump(res,open(f'{OUT}/{TAG}_screen.json','w'),ensure_ascii=False,indent=1)
  r=res[CODES[0]];print(TAG,r['summary'][:2],r['bars'],len(r['modal_rows']),r['modal_rows'][:2],'errs',len(errs))
asyncio.run(main())
