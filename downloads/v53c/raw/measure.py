import asyncio,json,sys
from playwright.async_api import async_playwright
BASE,TAG,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
KEY='donnaemsae.management.facts.v1';SEED=open('seed.json').read()
MEAS="""()=>{const t=document.querySelector('.mu-tabs:has(> button[data-comp])'),h=document.querySelector('.mu-comp-hero');const r=x=>x.getBoundingClientRect();const cs=getComputedStyle(h);const hr=r(h);const inner=hr.width-parseFloat(cs.borderLeftWidth)-parseFloat(cs.borderRightWidth)-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
const btn=[...t.querySelectorAll('button')].map(b=>{const g=document.createRange();g.selectNodeContents(b);const tr=g.getBoundingClientRect(),br=r(b);const s=getComputedStyle(b);return {t:b.textContent,pressed:b.getAttribute('aria-pressed'),btnCx:+(br.left+br.width/2).toFixed(2),textCx:+(tr.left+tr.width/2).toFixed(2),dx:+((tr.left+tr.width/2)-(br.left+br.width/2)).toFixed(2),w:+br.width.toFixed(2),h:+br.height.toFixed(2),textH:+tr.height.toFixed(1),lines:Math.round(tr.height/parseFloat(s.lineHeight||s.fontSize*1.2)||1),overflow:b.scrollWidth>b.clientWidth,style:{bg:s.backgroundColor,bc:s.borderColor,color:s.color,fw:s.fontWeight,fs:s.fontSize,radius:s.borderRadius,minh:s.minHeight}}});
const tr=r(t),ts=getComputedStyle(t),wrapInner=tr.width-2*parseFloat(ts.borderLeftWidth)-parseFloat(ts.paddingLeft)-parseFloat(ts.paddingRight);return {wrapInnerW:+wrapInner.toFixed(2),fill:+((r(t.lastElementChild).right-r(t.firstElementChild).left)/wrapInner*100).toFixed(1),vw:innerWidth,wrapW:+tr.width.toFixed(2),wrapL:+tr.left.toFixed(2),cardW:+hr.width.toFixed(2),cardL:+hr.left.toFixed(2),cardInnerW:+inner.toFixed(2),btnSpan:+(r(t.lastElementChild).right-r(t.firstElementChild).left).toFixed(2),docOverflow:document.documentElement.scrollWidth>innerWidth,btn}}"""
OTH="""()=>{const P=['display','grid-template-columns','gap','padding','background-color','border','border-radius','width','font-size','font-weight','color','text-align','justify-content','align-items','min-height','white-space','line-height'];return [...document.querySelectorAll('.mu-tabs, .mu-tabs button, [role=tablist], [role=tab], .mu-seg, .mu-seg button')].filter(e=>!e.matches('[data-comp]')&&!e.querySelector('[data-comp]')).map(e=>{const s=getComputedStyle(e);return [e.className+'|'+(e.textContent||'').trim().slice(0,20),P.map(p=>s.getPropertyValue(p)).join(';')]})}"""
PAGES=['management.html?mode=composition','management.html?mode=ledger','management.html?mode=dividends','management.html?mode=performance','management.html?mode=valuation','asset-home.html']
async def main():
  res={'meas':{},'other':{},'errors':[]}
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    for w in (360,390,412,430):
      cx=await b.new_context(viewport={'width':w,'height':900},device_scale_factor=2,service_workers='block');pg=await cx.new_page()
      pg.on('console',lambda m:res['errors'].append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:res['errors'].append(str(e)))
      await pg.goto(BASE+'management.html?mode=ledger',wait_until='networkidle');await pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,SEED])
      for tab in ('instrument','account'):
        await pg.goto(BASE+'management.html?mode=composition',wait_until='networkidle');await pg.wait_for_timeout(500)
        if tab=='account':await pg.click('[data-comp=account]');await pg.wait_for_timeout(300)
        m=await pg.evaluate(MEAS);res['meas'][f'{w}_{tab}']=m
        if tab=='instrument':
          h=await pg.locator('.mu-comp-hero').bounding_box();t=await pg.locator('.mu-tabs:has(> button[data-comp])').bounding_box()
          y0=h['y']-8;y1=t['y']+t['height']+90
          await pg.screenshot(path=f'{OUT}/{TAG}_{w}_card.png',clip={'x':0,'y':y0,'width':w,'height':y1-y0})
          if w==390:await pg.screenshot(path=f'{OUT}/{TAG}_390_full.png',full_page=True)
      if w==390:
        for u in PAGES:
          await pg.goto(BASE+u,wait_until='networkidle');await pg.wait_for_timeout(500);res['other'][u]=await pg.evaluate(OTH)
      await cx.close()
    await b.close()
  json.dump(res,open(f'{OUT}/{TAG}.json','w'),ensure_ascii=False,indent=1)
  for k,m in res['meas'].items():print(k,'wrap',m['wrapW'],'card',m['cardW'],'inner',m['cardInnerW'],'span',m['btnSpan'],'/',m['wrapInnerW'],m['fill'],'%',[(x['t'],x['dx'],x['w'],x['lines']) for x in m['btn']],'ovf',m['docOverflow'])
  print('errors',len(res['errors']),res['errors'][:3],'other',sum(len(v) for v in res['other'].values()))
asyncio.run(main())
