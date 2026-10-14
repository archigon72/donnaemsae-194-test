const R='/workspace/r194/account-uat/',L=require(R+'management-ledger.js'),T=require(R+'management-tax.js'),F=require(R+'fd-engine.js'),fs=require('fs');
T.init(JSON.parse(fs.readFileSync('/workspace/r194/data/tax-v53.json')));const DI=JSON.parse(fs.readFileSync('/workspace/r194/data/management-distributions.json')).items,FC=JSON.parse(fs.readFileSync(R+'fd-forecast.json'));
const out=[];const ck=(n,c,d)=>{out.push({name:n,pass:!!c,detail:d});console.log((c?'PASS ':'FAIL ')+n+(d!==undefined?' '+JSON.stringify(d).slice(0,300):''))};
const z=()=>L.D.of('0'),TD='2026-10-14';
const mk=(list,accs)=>({schema_version:1,created_at:'2026-01-01T00:00:00Z',accounts:accs||[{account_id:'a',name:'A',type:'일반'},{account_id:'b',name:'B',type:'ISA'},{account_id:'c',name:'C',type:'연금저축'}],transactions:list.map((t,i)=>({transaction_id:'t'+i,account_id:t[0],cycle_id:'c'+t[0]+t[1],type:t[4]||'initial_buy',order_key:i,trade_price:'1000',code:t[1],trade_date:t[2],quantity:t[3]})),dividend_uses:[],metadata:{}});
const codes=[...new Set(JSON.parse(fs.readFileSync('/workspace/r194/data/catalog.json')).items.map(x=>x.ticker))];
const lastReal={};for(const d of DI)if(d.cashflow_included!==false&&(!lastReal[d.code]||d.ex_date>lastReal[d.code]))lastReal[d.code]=d.ex_date;
const ST=['done','scheduled','unconfirmed','forecast'];
let agg={funds:0,rows:0,fc:0,und:0,monthSum:0,accSum:0,filt:0,tax:0,dup:0,overlap:0,afterLast:0,ledger:0,errs:[]};
for(const c of codes){agg.funds++;
 const s=mk([['a',c,'2025-01-02','10'],['b',c,'2025-06-02','7'],['c',c,TD,'3']]);const before=JSON.stringify(s);
 let b;try{b=F.build(L,T,s,DI,{today:TD,forecast:FC})}catch(e){agg.errs.push(c+':'+e.message);continue}
 if(JSON.stringify(s)!==before)agg.ledger++;
 agg.rows+=b.rows.length;agg.fc+=b.rows.filter(r=>r.state==='forecast'&&!r.undecided).length;agg.und+=b.rows.filter(r=>r.undecided).length;
 const keys=b.rows.map(r=>r.key);if(new Set(keys).size!==keys.length)agg.dup++;
 if(b.rows.some(r=>r.forecast&&r.ex_date<=lastReal[c]))agg.afterLast++;
 const mo=new Set(b.rows.filter(r=>!r.forecast).map(r=>r.account_id+r.ex_date.slice(0,7)));if(b.rows.some(r=>r.forecast&&mo.has(r.account_id+r.ex_date.slice(0,7))))agg.overlap++;
 for(const y of [2025,2026,2027])for(const basis of ['pre','post']){const S=F.summarize(L,b,{year:y,accounts:null,basis});
  for(const k of ST){const ms=S.months.reduce((v,m)=>v.add(m[k]),z());if(ms.cmp(S[k]))agg.monthSum++}
  const as=[...S.byAcc.values()].reduce((v,A)=>v.add(A.done).add(A.scheduled).add(A.forecast),z());if(as.cmp(S.total))agg.accSum++;
  const parts=['a','b','c'].map(a=>F.summarize(L,b,{year:y,accounts:new Set([a]),basis}));const ps=parts.reduce((v,P)=>v.add(P.total),z());if(ps.cmp(S.total)||parts.reduce((v,P)=>v+P.undecided,0)!==S.undecided)agg.filt++;
  const AB=F.summarize(L,b,{year:y,accounts:new Set(['a','b']),basis});if(AB.total.cmp(parts[0].total.add(parts[1].total)))agg.filt++;
  if(basis==='post'){const P=F.summarize(L,b,{year:y,accounts:null,basis:'pre'});const taxNoUnc=S.rows.filter(r=>r.state!=='held'&&!r.undecided&&r.state!=='unconfirmed').reduce((v,r)=>v.add(r.tax),z());if(P.total.sub(S.total).cmp(taxNoUnc)||S.tax.cmp(taxNoUnc))agg.tax++;}
 }
 for(const r of b.rows)if(r.state!=='held'&&!r.undecided&&r.net&&r.pretax.sub(r.tax).cmp(r.net)&&!r.confirmed)agg.tax++;
}
ck('194종 전체: 오류 0',!agg.errs.length,agg.errs.slice(0,3));
ck('월별 합 = 연간 합 (상태 4종 × 2025~2027 × 세전/세후)',agg.monthSum===0,agg.monthSum);
ck('계좌별 합 = 전체 계좌 총액',agg.accSum===0,agg.accSum);
ck('계좌 필터 일관성: 단일 계좌 합 = 전체, A+B 선택 = A + B, 금액 미정 건수 합 일치',agg.filt===0,agg.filt);
ck('세전-세후 차 = 세금 합(완료·예정·예상), 행별 세후 = 세전 - 세금',agg.tax===0,agg.tax);
ck('①②③ 무중복: 키 중복 0, 예상은 실제 마지막 배당락 이후만, 같은 계좌·월 실제/예상 겹침 0',agg.dup===0&&agg.afterLast===0&&agg.overlap===0,{dup:agg.dup,after:agg.afterLast,overlap:agg.overlap});
ck('원장 객체 불변(예상 기록 없음)',agg.ledger===0);
console.log('stats',JSON.stringify({funds:agg.funds,rows:agg.rows,forecast_amount_rows:agg.fc,undecided_rows:agg.und}));
// 329200
let s=mk([['a','329200','2026-01-02','10']]);let b=F.build(L,T,s,DI,{today:TD,forecast:FC});const f3=b.rows.filter(r=>r.forecast);
const avg=L.D.of(FC.items['329200'].per_share_sum).div('3');ck('329200 월배당 예상 = 최근3회 평균(33원) × 10주, 첫 예상 배당락 10-29·지급 11-03',FC.items['329200'].cadence==='monthly'&&avg.str()==='33'&&f3[0].ex_date==='2026-10-29'&&f3[0].pay_date==='2026-11-03'&&f3[0].pretax.str()==='330',f3[0]&&[f3[0].ex_date,f3[0].pay_date,f3[0].pretax.str()]);
// Dec→Jan
const dj=f3.find(r=>r.ex_date.startsWith('2026-12'));const S26=F.summarize(L,b,{year:2026,basis:'pre'}),S27=F.summarize(L,b,{year:2027,basis:'pre'});
ck('12월 예상 배당락(12-29) → 1월 지급(2027-01-05), 2027년 1월 집계',dj.pay_date==='2027-01-05'&&W(S27.months[0].forecast)===330&&W(S26.months[11].forecast)===330,[dj.pay_date]);
function W(v){return F.won(v)}
// 등록일 경계: 등록일 = 예상 배당락일 → 보류
s=mk([['a','329200','2026-10-29','10']]);b=F.build(L,T,s,DI,{today:TD,forecast:FC});const h=b.rows.find(r=>r.ex_date==='2026-10-29');ck('등록일 = 예상 배당락일(10-29) → 보류, 다음 회차부터 예상',h&&h.state==='held'&&b.rows.find(r=>r.ex_date==='2026-11-27').state==='forecast');
// 분기 금액 미정
const q=Object.entries(FC.items).find(([c,r])=>r.cadence==='quarterly')[0];s=mk([['a',q,'2026-01-02','10']]);b=F.build(L,T,s,DI,{today:TD,forecast:FC});const qs=F.summarize(L,b,{year:2027,basis:'pre'});
ck('분기 종목('+q+'): 예상 금액 미정, 연간 합계 제외(0 아님·건수 표시)',qs.undecided>0&&W(qs.forecast)===0&&b.rows.filter(r=>r.forecast).every(r=>r.undecided&&r.pretax===null));
// 0238P0 이력 없음
ck('분배 이력 없는 종목(0238P0) → 예상 일정 없음',FC.items['0238P0'].events.length===0);
// +3 영업일 재현
ck('예상 지급일 규칙이 기존 +3영업일(estimated) 회차 100% 재현',FC.self_check.estimated_pay_date_reproduced===FC.self_check.estimated_total&&FC.self_check.estimated_total===3416,FC.self_check);
// 달력 범위
const maxPay=Object.values(FC.items).flatMap(r=>r.events).reduce((m,e)=>e.pay_date>m?e.pay_date:m,'');ck('예상 지급일 ≤ KRX 달력 범위 끝(2027-12-31)',maxPay<='2027-12-31',maxPay);
// ISA 세금 0
s=mk([['b','329200','2026-01-02','10']]);b=F.build(L,T,s,DI,{today:TD,forecast:FC});ck('ISA 예상 세금 0·세후=세전',b.rows.filter(r=>r.forecast).every(r=>r.tax.str()==='0'&&r.net.cmp(r.pretax)===0));
fs.writeFileSync(process.argv[2],JSON.stringify({checks:out,stats:agg},null,1));
