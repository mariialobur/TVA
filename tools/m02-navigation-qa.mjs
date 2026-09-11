'use strict';
import { chromium } from 'playwright';

const base=process.env.BASE_URL||'http://127.0.0.1:4173/';
const browser=await chromium.launch({headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
let failures=0;
const fail=m=>{failures++;console.error('FAIL:',m)};
const pass=m=>console.log('OK:',m);

try{
  await page.goto(base+'m02-qualification-operations.html',{waitUntil:'domcontentloaded'});
  const handle=await page.waitForSelector('#module',{timeout:10000});
  const frame=await handle.contentFrame();
  if(!frame)throw new Error('M02 iframe unavailable');
  await frame.waitForLoadState('load');
  await frame.waitForFunction(()=>document.documentElement.dataset.m02HierarchyFixed==='1',{timeout:10000});

  const hierarchy=await frame.evaluate(()=>{
    const content=document.querySelector('#main > .content')||document.querySelector('.content');
    const cases=document.getElementById('sec-cases');
    return ['errors','quiz','memo','vocab','cheat'].map(sec=>{
      const el=document.getElementById('sec-'+sec);
      return {sec,parentIsContent:!!el&&el.parentElement===content,nestedInCases:!!el&&!!cases&&cases.contains(el)};
    });
  });
  for(const x of hierarchy){
    if(!x.parentIsContent||x.nestedInCases)fail(`M02 ${x.sec} hierarchy invalid`);
    else pass(`M02 ${x.sec} is a top-level section`);
  }

  for(const sec of ['errors','quiz','memo','vocab','cheat']){
    await frame.evaluate(s=>window.goto(s),sec);
    await page.waitForTimeout(80);
    const state=await frame.evaluate(s=>{
      const el=document.getElementById('sec-'+s);
      if(!el)return {missing:true};
      const cs=getComputedStyle(el),r=el.getBoundingClientRect();
      let p=el.parentElement,hiddenAncestor=false;
      while(p&&p!==document.body){const x=getComputedStyle(p);if(x.display==='none'||x.visibility==='hidden'){hiddenAncestor=true;break}p=p.parentElement}
      return {missing:false,display:cs.display,visibility:cs.visibility,height:r.height,text:(el.innerText||'').trim().length,hiddenAncestor};
    },sec);
    if(state.missing||state.display==='none'||state.visibility==='hidden'||state.hiddenAncestor||state.height<40||state.text<40)fail(`M02 ${sec} not visibly rendered: ${JSON.stringify(state)}`);
    else pass(`M02 ${sec} renders visible content`);
  }

  await frame.evaluate(()=>window.goto('memo'));
  await frame.waitForFunction(()=>document.getElementById('fc-term')?.textContent?.trim().length>1,{timeout:5000});
  const memo=await frame.evaluate(()=>{
    const card=document.getElementById('fc-card'),front=document.getElementById('fc-front');
    const cr=card?.getBoundingClientRect(),fr=front?.getBoundingClientRect();
    return {term:document.getElementById('fc-term')?.textContent?.trim()||'',cardHeight:cr?.height||0,frontHeight:fr?.height||0,frontPosition:front?getComputedStyle(front).position:''};
  });
  if(!memo.term||memo.cardHeight<100||memo.cardHeight>700||memo.frontPosition==='absolute')fail(`M02 memo card layout invalid: ${JSON.stringify(memo)}`);
  else pass('M02 native memo card is populated and bounded');
}catch(e){fail('M02 navigation runtime: '+e.message)}

await browser.close();
if(failures){console.error(`\nM02 NAVIGATION QA: ${failures} failure(s)`);process.exit(1)}
console.log('\nM02 NAVIGATION QA: PASS');
