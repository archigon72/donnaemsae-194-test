"""v5.3d 원장 보호 검증 — 별첨 사진 사례(직접매수 500주·재투자 0주·세후 누적 수령 121,000원)를 모사한 가상 원장.
실제 원장 미사용. 격리 브라우저 컨텍스트, 가상 계좌. 세후 121,000원 = 자동 세후 4건(99,449원) + 9/29 회차 가상 확정 실입금 21,551원."""
import asyncio,json,sys,re
from playwright.async_api import async_playwright
BASE,TAG,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
KEY='donnaemsae.management.facts.v1';AID='virt-0048j0-case';ACC='가상-0048J0사례계좌'
SEED={"schema_version":1,"created_at":"2026-10-14T00:00:00.000Z","accounts":[{"account_id":AID,"name":ACC,"type":"일반"}],
 "dividend_confirmations":[{"account_id":AID,"distribution_id":"0048J0-20260929","amount":"21551","confirmed_at":"2026-10-14T00:00:00.000Z"}],
 "transactions":[{"transaction_id":"virt-tx-1","account_id":AID,"code":"0048J0","cycle_id":"virt-cy-1","type":"initial_buy","trade_date":"2026-05-01","order_key":0,"quantity":"500","trade_price":"13500"}],
 "dividend_uses":[{"use_id":"virt-use-1","account_id":AID,"use_date":"2026-10-10","order_key":0,"amount":"20000"}],"metadata":{"app":"donnaemsae-lab","scope":"user-facts"}}
R={'checks':[],'errors':[],'obs':{}}
def check(n,ok,d=None):R['checks'].append({'check':n,'pass':bool(ok),'detail':d});print(('PASS ' if ok else 'FAIL ')+n,json.dumps(d,ensure_ascii=False)[:300])
INST="""()=>({flow:[...document.querySelectorAll('.mc-flow li,.mu-flow-tile')].map(x=>x.textContent.replace(/\\s+/g,' ').trim()),qty:document.body.innerText.match(/직접매수 [\\d,]+주 \\/ 재투자 [\\d,]+주|[\\d,]+주 중 [\\d,]+주는 배당이 만든 수량/g)||[],basis:[...document.querySelectorAll('[data-divbasis]')].map(b=>[b.dataset.divbasis,b.getAttribute('aria-pressed')])})"""
def amt(flow,key):
    for x in flow:
        if key in x:
            m=re.findall(r'([\d,]+)원',x);return int(m[-1].replace(',','')) if m else x
async def inst(pg,basis):
    await pg.goto(BASE+'management.html?mode=performance',wait_until='networkidle');await pg.wait_for_timeout(600)
    await pg.click('[data-scope=instrument]');await pg.wait_for_timeout(200);await pg.select_option('#scope-value','0048J0');await pg.wait_for_timeout(300)
    await pg.click(f'button[data-divbasis={basis}]');await pg.wait_for_timeout(300);return await pg.evaluate(INST)
async def avail(pg):
    await pg.goto(BASE+'management.html?mode=ledger',wait_until='networkidle');await pg.wait_for_timeout(500);await pg.click('[data-action=use]');await pg.wait_for_timeout(250)
    await pg.select_option('#use-form select[name=account]',index=0);await pg.dispatch_event('#use-form select[name=account]','change');await pg.wait_for_timeout(150)
    t=await pg.inner_text('#available-cash');await pg.keyboard.press('Escape');return t
async def comp(pg):
    await pg.goto(BASE+'management.html?mode=composition',wait_until='networkidle');await pg.wait_for_timeout(500);return await pg.inner_text('.mu-comp-amt')
async def settype(pg,typ):
    await pg.goto(BASE+'management.html?mode=ledger',wait_until='networkidle');await pg.wait_for_timeout(400);await pg.click('[data-action=acctype]');await pg.wait_for_timeout(250)
    await pg.select_option(f'#acctype-form select[data-acc="{AID}"]',typ);await pg.click('#acctype-form button[type=submit]');await pg.wait_for_timeout(500)
async def store(pg):return json.loads(await pg.evaluate(f"localStorage.getItem('{KEY}')"))
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    cx=await b.new_context(viewport={'width':390,'height':900},device_scale_factor=2,service_workers='block');pg=await cx.new_page()
    pg.on('console',lambda m:R['errors'].append(m.text) if m.type=='error' else None);pg.on('pageerror',lambda e:R['errors'].append(str(e)))
    await pg.goto(BASE+'management.html?mode=ledger',wait_until='networkidle');await pg.evaluate("([k,v])=>localStorage.setItem(k,v)",[KEY,json.dumps(SEED,ensure_ascii=False)])
    s0=await store(pg);O=R['obs']
    O['net']=n=await inst(pg,'net')
    await pg.screenshot(path=f'{OUT}/{TAG}_ledger_case_net.png',full_page=True)
    O['pre']=pr=await inst(pg,'pre');O['comp']=await comp(pg);O['avail']=await avail(pg)
    check('보유수량: 직접매수 500주 / 재투자 0주','직접매수 500주 / 재투자 0주' in n['qty'],n['qty'])
    check('직접투자 원가 6,750,000원(500주×13,500원)',O['comp'].replace(' ','')=='6,750,000원',O['comp'])
    check('세후 받은 배당 121,000원',amt(n['flow'],'받은 배당')==121000,n['flow'])
    check('재투자 배당 0원',amt(n['flow'],'다시 투자')==0,n['flow'])
    check('세전 받은 배당 142,500원(43+60+60+61+61원×500주)',amt(pr['flow'],'받은 배당')==142500,pr['flow'])
    check('사용/잔액 계좌 단위: 사용 가능 101,000원(121,000−20,000)','101,000' in O['avail'],O['avail'])
    check('사용/남은 배당 종목 화면은 계좌 공유 표기',any('계좌' in x for x in n['flow'] if '사용' in x or '남아' in x),n['flow'])
    await settype(pg,'ISA');O['isa']=i=await inst(pg,'net');s1=await store(pg)
    check('계좌 유형 ISA 변경: 자동분 세금 0 재계산, 확정 실입금 21,551원 유지 → 133,551원',amt(i['flow'],'받은 배당')==133551,i['flow'])
    check('유형 변경 시 원장 거래·사용·확정 실입금 불변(유형만 변경)',{k:v for k,v in s1.items() if k!='accounts'}=={k:v for k,v in s0.items() if k!='accounts'} and s1['accounts'][0]['type']=='ISA',s1['accounts'])
    await settype(pg,'일반');O['back']=bk=await inst(pg,'net');s2=await store(pg)
    check('일반으로 되돌림: 121,000원 복귀, 원장 전체 = 시작 원장',amt(bk['flow'],'받은 배당')==121000 and s2==s0,bk['flow'])
    await pg.reload(wait_until='networkidle');O['reload']=rl=await inst(pg,'net')
    check('새로고침 후 동일(121,000원, 500주/0주)',amt(rl['flow'],'받은 배당')==121000 and rl['qty']==n['qty'],rl['flow'])
    check('콘솔 오류 0',not R['errors'],R['errors'][:3])
    O['stored_final']=s2;await b.close()
  json.dump(R,open(f'{OUT}/{TAG}_ledger_guard.json','w'),ensure_ascii=False,indent=1)
asyncio.run(main())
