/* 미래배당 화면 계산 (UAT 후보). 원장은 읽기만 하고 절대 쓰지 않는다.
   상태 구분: done=① 원장 실입금 확정(dividend_confirmations) · scheduled=② 확정 일정 미수령(지급일 미래) ·
   unconfirmed=지급일 경과·실입금 미확정(원장 자동입금 생성 안 함) · held=등록일 경계 보류(권리 확인 불가) ·
   forecast=③ 예상 — 승인된 예측 산식 없음 → 금액·날짜 계산 안 함(FORECAST_APPROVED=false).
   세금: 기존 승인 ManagementTax.compute 재사용. 등록 전 지급 회차는 소급하지 않음. */
(function(root){'use strict';
const FORECAST_APPROVED=false;
function regDates(state){const m=new Map();for(const t of state.transactions){const k=t.account_id+':'+t.code;if(!m.has(k)||t.trade_date<m.get(k))m.set(k,t.trade_date)}return m}
function heldNow(L,state,a,code){return L.entitlement(state,a,code,'9999-12-31').cmp('0')>0}
function build(L,T,state,dists,opt){
 const today=opt.today||L.today(),accTypes=new Map(state.accounts.map(a=>[a.account_id,a.type||'일반'])),conf=new Map((state.dividend_confirmations||[]).map(c=>[c.account_id+':'+c.distribution_id,c]));
 const reg=regDates(state),distMap=new Map(dists.map(d=>[d.distribution_id,d])),codes=new Set(state.transactions.map(t=>t.code)),out=[],seen=new Set();
 for(const d of dists){if(!codes.has(d.code)||d.cashflow_included===false)continue;if(d.status!=='confirmed'&&d.status!=='estimated')continue;if(!d.ex_date||!d.pay_date)continue;
  for(const a of state.accounts){const id=a.account_id,k=id+':'+d.code,r=reg.get(k);if(!r)continue;const key=id+':'+d.distribution_id;if(seen.has(key))continue;seen.add(key);
   if(d.pay_date<r)continue; /* 등록 전 지급 → 소급 금지 */
   const q=L.entitlement(state,id,d.code,d.ex_date),base={key,account_id:id,code:d.code,distribution_id:d.distribution_id,ex_date:d.ex_date,pay_date:d.pay_date,pay_date_kind:d.pay_date_kind||(d.status==='estimated'?'estimated':'actual'),per_share:d.per_share,acct_type:accTypes.get(id)};
   if(q.cmp('0')<=0){if(d.ex_date<=r&&heldNow(L,state,id,d.code))out.push({...base,state:'held',quantity:null,reason:'등록일('+r+') 이전·당일 배당락 회차 — 기존 자료로 권리 확정 여부를 확인할 수 없어 보류'});continue}
   const pre=q.mul(d.per_share),tx=T&&T.ready()?T.compute(L,{amount:pre,code:d.code,distribution_id:d.distribution_id,quantity:q},accTypes.get(id),distMap):null;
   const cf=conf.get(key);let st=d.pay_date>today?'scheduled':cf?'done':'unconfirmed';
   const net=cf&&st==='done'?L.D.of(cf.amount):tx?tx.net:null;
   out.push({...base,state:st,quantity:q,pretax:pre,tax:tx?(cf&&st==='done'?pre.sub(net):tx.tax):null,net,rule_label:tx?tx.rule_label:'세금 자료 미로딩',confirmed:!!cf});}}
 /* 배당락 이벤트(보유 종목, 표시용) */
 const ex=[];for(const d of dists){if(!codes.has(d.code)||d.cashflow_included===false||!d.ex_date)continue;for(const a of state.accounts){const r=reg.get(a.account_id+':'+d.code);if(!r||d.ex_date<r)continue;const q=L.entitlement(state,a.account_id,d.code,d.ex_date);ex.push({account_id:a.account_id,code:d.code,distribution_id:d.distribution_id,date:d.ex_date,quantity:q,per_share:d.per_share})}}
 return {rows:out,ex,today,forecast:{approved:FORECAST_APPROVED,label:'예상 미승인 · 산식 미정'}};
}
function amt(L,r,basis){if(r.state==='held')return null;return basis==='pre'?r.pretax:r.net}
function won(v){return v==null?null:Math.round(v.num())}
function man(w){if(w==null)return '—';const s=w<0?'-':'',a=Math.abs(w);if(a<10000)return s+a.toLocaleString('ko-KR')+'원';const t=Math.round(a/1000)/10;return s+t.toLocaleString('ko-KR',{minimumFractionDigits:1,maximumFractionDigits:1})+'만'}
function exact(L,v){if(v==null)return '—';const s=v.str(2),[i,f]=s.split('.');return Number(i).toLocaleString('ko-KR')+(f?'.'+f:'')+'원'}
function summarize(L,b,{year,accounts,basis}){const z=()=>L.D.of('0'),sel=r=>(!accounts||accounts.has(r.account_id))&&r.pay_date.slice(0,4)===String(year);
 const rows=b.rows.filter(sel),S={done:z(),scheduled:z(),unconfirmed:z(),tax:z(),held:0,months:Array.from({length:12},()=>({done:z(),scheduled:z(),unconfirmed:z(),n:0})),byAcc:new Map()};
 for(const r of rows){const m=+r.pay_date.slice(5,7)-1;S.months[m].n++;if(r.state==='held'){S.held++;S.months[m].held=(S.months[m].held||0)+1;continue}const v=amt(L,r,basis);if(v==null)continue;S[r.state]=S[r.state].add(v);S.months[m][r.state]=S.months[m][r.state].add(v);if(r.state!=='unconfirmed'&&r.tax)S.tax=S.tax.add(r.tax);
  const A=S.byAcc.get(r.account_id)||{done:z(),scheduled:z(),unconfirmed:z(),n:0};A[r.state]=A[r.state].add(v);A.n++;S.byAcc.set(r.account_id,A)}
 S.rows=rows;S.total=S.done.add(S.scheduled);return S}
const api={build,summarize,man,exact,won,amt,FORECAST_APPROVED};root.FutureDividend=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);
