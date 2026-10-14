const R='/workspace/r194/account-uat/',L=require(R+'management-ledger.js'),T=require(R+'management-tax.js'),F=require(R+'fd-engine.js'),fs=require('fs');
T.init(JSON.parse(fs.readFileSync('/workspace/r194/data/tax-v53.json')));const REAL=JSON.parse(fs.readFileSync('/workspace/r194/data/management-distributions.json')).items;
const out=[];const ck=(n,c,d)=>{out.push({name:n,pass:!!c,detail:d});console.log((c?'PASS ':'FAIL ')+n+(d!==undefined?' '+JSON.stringify(d):''))};
const st=(tx,acc=[{account_id:'a',name:'A',type:'일반'}],conf)=>({schema_version:1,created_at:'2026-01-01T00:00:00Z',accounts:acc,transactions:tx.map((t,i)=>({transaction_id:'t'+i,account_id:'a',cycle_id:'c'+t[0],type:'initial_buy',order_key:i,trade_price:'1000',code:t[0],trade_date:t[1],quantity:t[2],...(t[3]||{})})),dividend_uses:[],metadata:{},...(conf?{dividend_confirmations:conf}:{})});
const SY=(code,ex,pay,ps,id,extra)=>({code,distribution_id:id||code+'-'+ex.replace(/-/g,''),per_share:ps,ex_date:ex,pay_date:pay,status:'confirmed',pay_date_kind:'actual',cashflow_included:true,...extra});
// 1 0원 출발: 오늘 등록 → 과거 회차 소급 0
let b=F.build(L,T,st([['329200','2026-10-14','10']]),REAL,{today:'2026-10-14'});ck('오늘 등록 시 과거 실입금 0원·소급 0건',b.rows.filter(r=>r.state!=='held').length===0,b.rows.length);
// 2 확정 일정 미수령(합성: 미래 지급일) → scheduled, 원장 영향 없음
b=F.build(L,T,st([['TST001','2026-09-01','10']]),[SY('TST001','2026-10-10','2026-10-20','100')],{today:'2026-10-14'});ck('[합성] 지급일 미래 → ②예정',b.rows[0]?.state==='scheduled'&&b.rows[0].pretax.str()==='1000',b.rows[0]?.state);
// 3 지급일 경과·확정 없음 → unconfirmed (자동 입금 아님)
b=F.build(L,T,st([['TST001','2026-09-01','10']]),[SY('TST001','2026-10-01','2026-10-05','100')],{today:'2026-10-14'});ck('지급일 경과·실입금 미확정 → 확인 필요(완료 아님)',b.rows[0].state==='unconfirmed');
// 4 실입금 확정 → done, 확정액 우선
b=F.build(L,T,st([['TST001','2026-09-01','10']],undefined,[{account_id:'a',distribution_id:'TST001-20261001',amount:'846',confirmed_at:'x'}]),[SY('TST001','2026-10-01','2026-10-05','100')],{today:'2026-10-14'});ck('실입금 확정 → ①완료, 확정액 846 우선',b.rows[0].state==='done'&&b.rows[0].net.str()==='846'&&b.rows[0].tax.str()==='154');
// 5 등록일 경계: 배당락=등록일 → 보류
b=F.build(L,T,st([['TST001','2026-10-01','10']]),[SY('TST001','2026-10-01','2026-10-05','100')],{today:'2026-10-14'});ck('배당락일=등록일 → 보류(금액 미계산)',b.rows[0].state==='held'&&b.rows[0].pretax===undefined);
b=F.build(L,T,st([['TST001','2026-10-03','10']]),[SY('TST001','2026-10-01','2026-10-20','100')],{today:'2026-10-14'});ck('등록 전 배당락·등록 후 지급 → 보류(권리 생성 안 함)',b.rows[0].state==='held');
// 6 12월 배당락→1월 지급: 지급월 기준 다음 해
b=F.build(L,T,st([['TST001','2025-12-01','10']]),[SY('TST001','2025-12-29','2026-01-05','100')],{today:'2026-10-14'});let s25=F.summarize(L,b,{year:2025,basis:'pre'}),s26=F.summarize(L,b,{year:2026,basis:'pre'});ck('12월 배당락·1월 지급 → 2026년 1월 집계(2025 0)',F.won(s25.total.add(s25.unconfirmed))===0&&F.won(s26.months[0].unconfirmed)===1000);
// 7 중복 회차(같은 distribution_id 2행) → 1회만
b=F.build(L,T,st([['TST001','2026-09-01','10']]),[SY('TST001','2026-10-01','2026-10-05','100'),SY('TST001','2026-10-01','2026-10-05','100')],{today:'2026-10-14'});ck('중복 회차 1회만 집계',b.rows.length===1);
// 8 주배당(합성 5회/월) 모두 개별 집계
const wk=['2026-09-04','2026-09-11','2026-09-18','2026-09-25','2026-10-02'].map(d=>SY('TST002',d,d.replace(/(\d\d)$/,m=>String(+m+2).padStart(2,'0')),'10'));b=F.build(L,T,st([['TST002','2026-09-01','10']]),wk,{today:'2026-10-14'});ck('[합성] 주배당 5회 개별 집계·합 500원',b.rows.length===5&&F.won(F.summarize(L,b,{year:2026,basis:'pre'}).unconfirmed)===500);
// 9 329200: 2024-06-28 0원 중복행 제외, 계산 59회
b=F.build(L,T,st([['329200','2019-12-01','1']]),REAL,{today:'2026-10-14'});const r3=b.rows.filter(r=>r.code==='329200');ck('329200 excluded_duplicate 제외·59회·세전 2,167원',r3.length===59&&!r3.some(r=>r.distribution_id==='329200-20240628')&&r3.reduce((v,r)=>v.add(r.pretax),L.D.of('0')).str()==='2167',r3.length);
// 10 세전/세후 + 계좌유형: ISA 세금 0, 일반 해외형 15.4%
const two=[{account_id:'a',name:'A',type:'일반'},{account_id:'b',name:'B',type:'ISA'}];let s=st([['0004G0','2026-01-02','100']],two);s.transactions.push({...s.transactions[0],transaction_id:'tb',account_id:'b',cycle_id:'cb'});b=F.build(L,T,s,REAL,{today:'2026-10-14'});const ra=b.rows.find(r=>r.account_id==='a'&&r.state!=='held'),rb=b.rows.find(r=>r.account_id==='b'&&r.distribution_id===ra.distribution_id);ck('세후: 일반 해외형 세금>0·ISA 세금 0 (기존 승인 규칙 재사용)',ra.tax.cmp('0')>0&&rb.tax.str()==='0'&&rb.net.cmp(rb.pretax)===0,{a:ra.rule_label,b:rb.rule_label});
// 11 수량 변경(매도) 반영
s=st([['0004G0','2026-01-02','100'],['0004G0','2026-06-01','40',{type:'sell',cycle_id:'c0004G0'}]]);b=F.build(L,T,s,REAL,{today:'2026-10-14'});const after=b.rows.find(r=>r.ex_date>'2026-06-01'&&r.state!=='held');ck('매도 후 회차 권리수량 60주 반영',after.quantity.str()==='60');
// 12 replay(기존 원장 엔진)과 세전 총액 일치(무중복 합산)
const rp=L.replay(s,REAL,'2026-10-14');let rs=L.D.of('0');for(const e of rp.events)if(e.kind==='dividend')rs=rs.add(e.amount);let fs2=L.D.of('0');for(const r of b.rows)if(r.state!=='held'&&r.state!=='scheduled')fs2=fs2.add(r.pretax);ck('기존 원장 replay 세전 배당 합 = 화면 엔진 합(무중복)',rs.cmp(fs2)===0,[rs.str(),fs2.str()]);
// 13 예상 산식 미승인
ck('예상(③) 승인 반영: FORECAST_APPROVED=true, 예상 자료 미전달 시 예상 행 0',F.FORECAST_APPROVED===true&&!b.rows.some(r=>r.state==='forecast'));
// 14 축약 표기
ck('표시 축약: 54,321→5.4만, 9,999→9,999원, 10,270,999→1,027.1만',F.man(54321)==='5.4만'&&F.man(9999)==='9,999원'&&F.man(10270999)==='1,027.1만');
fs.writeFileSync(process.argv[2],JSON.stringify(out,null,1));
