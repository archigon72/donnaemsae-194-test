/* Connect approved external data; delegate all rights/financial arithmetic to unchanged ledger. */
(function(root){'use strict';
// release194: status=estimated rows (FunETF payDt missing) use expected_pay_date = gijunYmd + 3 KRX business days.
// They are handed to the unchanged ledger as payable rows (pay_date_kind kept) so cash/reinvest/use include them once the date arrives.
function split(distributions){return {payable:distributions.filter(d=>d.status==='confirmed'||(d.status==='estimated'&&d.expected_pay_date)).map(d=>d.status==='estimated'?{...d,status:'confirmed',pay_date:d.expected_pay_date,pay_date_kind:'estimated'}:d),estimated:distributions.filter(d=>d.status==='estimated'&&d.expected_pay_date),pending:distributions.filter(d=>d.status==='payment_date_unknown'||(d.status==='estimated'&&!d.expected_pay_date))}}
function entitlements(state,distributions,L,asOf=L.today()){
 const rows=[],parts=split(distributions);for(const d of parts.pending.concat(parts.estimated)){if(d.ex_date>asOf)continue;for(const a of state.accounts){const q=L.entitlement(state,a.account_id,d.code,d.ex_date);if(q.cmp('0')>0)rows.push({account_id:a.account_id,code:d.code,ex_date:d.ex_date,quantity:q,amount:q.mul(d.per_share),status:d.status==='estimated'?'estimated':'payment_date_unknown',expected_pay_date:d.expected_pay_date||null,reflected:d.status==='estimated'&&d.expected_pay_date<=asOf,distribution_id:d.distribution_id})}}return rows;
}
function priceBasis(prices){const days=[...new Set((prices?.items||[]).map(p=>p.trade_date))].sort();return days.length>1?'가격 기준일 혼합':days.length?days[0].slice(5).replace('-','.')+' 종가 기준':'시장가격 미제공'}
function priceNotes(prices){const days=[...new Set((prices?.items||[]).map(p=>p.trade_date))].sort();return days.length>1?['일부 종목은 이전 종가 사용 · 종목별 가격 기준일 '+days[0]+'~'+days.at(-1)]:[]}
const api={split,entitlements,priceBasis,priceNotes};root.ManagementData=api;if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);
