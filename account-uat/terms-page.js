'use strict';
/* U25(2026-10-19): 용어·지표 이해하기 — 4범주 바로가기 + 요약 우선 카드(자세히 보기/접기).
   설명 원문은 data/term-help-content.json 그대로(ID·문구 불변). 요약 한 줄(SUM)만 화면용으로 추가. 산식·지표 변경 없음. */
function copyText(el,text){for(const part of String(text||'').split(/(\*\*[^*]+\*\*|`[^`]+`)/g)){if(!part)continue;if(part.startsWith('**')){const strong=document.createElement('strong');strong.textContent=part.slice(2,-2);el.append(strong);}else el.append(document.createTextNode(part.startsWith('`')?part.slice(1,-1):part));}}
const U25_CATS=[['분배금',['distribution-yield']],['자산가치와 성과',['nav','raw-nav','nav-tr','reinvestment-effect']],['하락과 회복',['mdd','recovery-period']],['시장 비교',['tracking-index','reference-market']]];
const U25_SUM={'distribution-yield':'최근 12개월 동안 지급된 1주당 분배금 합계를 현재 NAV와 비교한 비율','nav':'ETF가 보유한 자산을 기준으로 계산한 1주당 가치','raw-nav':'분배금을 재투자하지 않았다고 가정한 NAV 기준 성과','nav-tr':'세전 분배금을 같은 ETF에 모두 재투자했다고 가정한 NAV 기준 성과','reinvestment-effect':'같은 기간 NAV-TR과 Raw NAV 수익률의 차이(%p)','mdd':'선택 기간에 앞선 고점에서 가장 크게 떨어진 폭','recovery-period':'하락 후 이전 고점 수준을 다시 회복하는 데 걸린 기간','tracking-index':'ETF가 운용의 기준으로 삼는 지수','reference-market':'ETF 성과를 대표 시장과 비교할 때 쓰는 별도의 기준'};
/* 원문 첫 설명 블록(2줄)의 각 줄이 어떤 소제목에 해당하는지. 문장은 원문 그대로 사용 */
const U25_LINES={'distribution-yield':['무슨 뜻인가요?','왜 보나요?'],'raw-nav':['무슨 뜻인가요?','무슨 뜻인가요?'],'nav-tr':['무슨 뜻인가요?','왜 보나요?'],'reinvestment-effect':['무슨 뜻인가요?','어떻게 읽나요?'],'mdd':['무슨 뜻인가요?','어떻게 읽나요?'],'recovery-period':['무슨 뜻인가요?','어떻게 읽나요?'],'tracking-index':['무슨 뜻인가요?','왜 보나요?'],'reference-market':['무슨 뜻인가요?','어떻게 읽나요?']};
const U25_ORDER=['무슨 뜻인가요?','왜 보나요?','어떻게 읽나요?','주의할 점'];
function u25Groups(id,item){
 const g=new Map(U25_ORDER.map(k=>[k,[]]));const put=(k,x)=>g.get(k).push(x);
 for(const block of item.detail_blocks||[]){
  if(!block.text&&!block.bullets?.length)continue;const h=(block.heading||'').trim();
  if(h==='주의'){if(block.text)put('주의할 점',{text:block.text});for(const b of block.bullets||[])put('주의할 점',{text:b});continue}
  if(h==='무슨 뜻인가요?'||h==='왜 보나요?'){if(block.text)put(h,{text:block.text});if(block.bullets?.length)put(h,{bullets:block.bullets});continue}
  if(/어떻게 보면 되나요/.test(h)){const bs=block.bullets||[];
   /* NAV: 마지막 문장(연구소 분석 기준 안내)만 '주의할 점', 나머지는 '어떻게 읽나요?'. 문장 불변 */
   const cut=id==='nav'&&bs.length>=3?bs.length-1:bs.length;if(block.text)put('어떻게 읽나요?',{text:block.text});if(cut)put('어떻게 읽나요?',{bullets:bs.slice(0,cut)});for(const b of bs.slice(cut))put('주의할 점',{text:b});continue}
  if(!h&&block.text){const lines=block.text.split('\n'),map=U25_LINES[id];
   if(map&&lines.length===map.length){lines.forEach((t,i)=>put(map[i],{text:t}))}else put('무슨 뜻인가요?',{text:block.text});
   if(block.bullets?.length)put('무슨 뜻인가요?',{bullets:block.bullets});continue}
  put(h||'무슨 뜻인가요?',block);
 }
 return [...g.entries()].filter(([,v])=>v.length);
}
function u25Open(sec,open){const btn=sec.querySelector('.u25-toggle'),det=sec.querySelector('.u25-detail');if(!btn||!det)return;btn.setAttribute('aria-expanded',String(open));det.hidden=!open;btn.querySelector('span').textContent=open?'접기':'자세히 보기';sec.classList.toggle('is-open',open)}
function u25Go(id,smooth){const sec=document.getElementById(id);if(!sec||!sec.classList.contains('u25-card'))return false;u25Open(sec,true);requestAnimationFrame(()=>sec.scrollIntoView({block:'start',behavior:smooth?'smooth':'auto'}));return true}
(async()=>{
 const response=await fetch('./data/term-help-content.json');if(!response.ok)return;const data=await response.json(),nav=document.querySelector('.terms-nav'),sections=document.querySelector('#terms-sections');
 const q=new URLSearchParams(location.search),from=['detail.html','mobile-detail.html'].includes(q.get('from'))?q.get('from'):'detail.html';const back=new URL(from,location.href);if(/^[0-9A-Z]{6}$/.test(q.get('code')||''))back.searchParams.set('code',q.get('code'));document.getElementById('terms-back').href=back.href;
 if(matchMedia('(max-width:760px)').matches)document.body.classList.add('mobile');
 const analysis=document.getElementById('terms-analysis-tabs');for(const [id,label] of [['dist','분배'],['perf','실제성과'],['capital','원금체력'],['mdd','MDD·회복'],['market','시장대비'],['facts','팩트']]){const a=document.createElement('button'),url=new URL(back);url.hash=id;a.type='button';a.className='analysis-tab';a.addEventListener('click',()=>location.assign(url.href));a.textContent=label;analysis.append(a);}const current=document.createElement('button');current.type='button';current.className='section-terms analysis-tab active';current.textContent='용어';current.setAttribute('aria-current','page');analysis.append(current);
 const terms=data.terms||{},seen=new Set();
 const cats=U25_CATS.map(([n,ids])=>[n,ids.filter(id=>terms[id])]);
 const rest=Object.keys(terms).filter(id=>!U25_CATS.some(([,ids])=>ids.includes(id)));if(rest.length)cats.push(['기타',rest]);   // JSON에 새 용어가 생겨도 누락 없이 표시
 const navTitle=document.createElement('p');navTitle.className='u25-nav-title';navTitle.textContent='용어 바로가기';nav.append(navTitle);
 let first=null;
 for(const [cat,ids] of cats){
  const row=document.createElement('div');row.className='u25-cat';const lab=document.createElement('span');lab.className='u25-cat-name';lab.textContent=cat;const chips=document.createElement('div');chips.className='u25-chips';row.append(lab,chips);nav.append(row);
  const ch=document.createElement('p');ch.className='u25-cat-h';ch.textContent=cat;sections.append(ch);
  for(const id of ids){const item=terms[id];seen.add(id);
   const link=document.createElement('a');link.href='#'+id;link.textContent=item.title;link.addEventListener('click',e=>{e.preventDefault();history.replaceState(null,'','#'+id);u25Go(id,true)});chips.append(link);
   const section=document.createElement('section');section.id=id;section.className='u25-card';section.dataset.cat=cat;
   const heading=document.createElement('h2');heading.textContent=item.title;section.append(heading);
   const sum=document.createElement('p');sum.className='u25-sum';sum.textContent=U25_SUM[id]||String(item.short||'').split('\n')[0].replace(/\*\*|`/g,'');section.append(sum);
   const det=document.createElement('div');det.className='u25-detail';det.id=id+'-detail';
   for(const [h,list] of u25Groups(id,item)){const box=document.createElement('div');box.className='u25-block'+(h==='주의할 점'?' u25-caution':'');const h3=document.createElement('h3');h3.textContent=h;box.append(h3);
    for(const x of list){if(x.text){const p=document.createElement('p');p.className='term-detail-copy';copyText(p,x.text);box.append(p)}if(x.bullets?.length){const ul=document.createElement('ul');ul.className='term-detail-copy';for(const t of x.bullets){const li=document.createElement('li');copyText(li,t);ul.append(li)}box.append(ul)}}
    det.append(box)}
   const btn=document.createElement('button');btn.type='button';btn.className='u25-toggle';btn.setAttribute('aria-controls',det.id);btn.setAttribute('aria-expanded','false');btn.innerHTML='<span>자세히 보기</span>';btn.addEventListener('click',()=>u25Open(section,btn.getAttribute('aria-expanded')!=='true'));
   section.append(btn,det);sections.append(section);u25Open(section,false);if(!first)first=section;}
 }
 // The sections are data-driven, so apply an incoming anchor after insertion.
 const want=decodeURIComponent(location.hash.slice(1));
 if(!(want&&u25Go(want,false))&&first)u25Open(first,true);
 addEventListener('hashchange',()=>u25Go(decodeURIComponent(location.hash.slice(1)),true));
})();
