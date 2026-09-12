'use strict';
import { chromium } from 'playwright';
const base=process.env.BASE_URL||'http://127.0.0.1:4173/',DASH='tvaSpecialisteTvaDashboardV1';
const mods=[
  ['M09','m09-secteurs-sensibles-tva.html','tva_m09_legal_qa_v2',['theory','sources','cases','errors','quiz','memo','cheat'],[2,5,7,9]],
  ['M10','m10-digital-plateformes-ecommerce.html','tva_m10_legal_qa_v2',['theory','sources','cases','errors','quiz','memo','vocab','cheat'],[4,6,9,11]],
  ['M11','m11-controle-afc-tva.html','tva_m11_legal_qa_v2',['theory','sources','cases','errors','quiz','memo','vocab','cheat'],[2,4,9,11]],
  ['M12','m12-jurisprudence-lab-tva.html','tva_m12_legal_qa_v2',['theory','sources','bank','cases','errors','quiz','memo','cheat'],[0,6,7,11]],
  ['M13','m13-communication-fiscale-cabinet.html','tva_m13_legal_qa_v2',['theory','sources','templates','cases','errors','quiz','memo','cheat'],[1,4,6,11]]
];
const browser=await chromium.launch({headless:true});let failures=0;const fail=m=>{failures++;console.error('FAIL:',m)},pass=m=>console.log('OK:',m);
async function dash(p,m){return p.evaluate(([k,x])=>{try{return JSON.parse(localStorage.getItem(k)||'{}')[x]}catch(e){return null}},[DASH,m])}
async function finish(p){return p.evaluate(async()=>{const r=window.finishModule();if(r&&typeof r.then==='function')await r})}
async function work(p){const el=p.locator('#module');if(await el.count()){const h=await p.waitForSelector('#module'),f=await h.contentFrame();await f.waitForLoadState('load');return f}return p}
for(const [mod,file,key,secs,required] of mods){
  const p=await browser.newPage();
  try{
    await p.goto(base+file,{waitUntil:'domcontentloaded'});await p.evaluate(()=>localStorage.clear());
    await p.evaluate(([k,ss])=>{const v={visited:{},quizScore:75};ss.forEach(s=>v.visited[s]=1);localStorage.setItem(k,JSON.stringify(v))},[key,secs]);
    await p.reload({waitUntil:'domcontentloaded'});await p.waitForTimeout(250);
    const w=await work(p),badges=await w.locator('.practice-required').count();
    if(badges!==4)fail(mod+' shows '+badges+' required cases instead of 4');else pass(mod+' marks 4 essential practical cases');
    await finish(p);await p.waitForTimeout(100);
    if(await dash(p,mod)==='done')fail(mod+' completed with QCM/sections but without essential cases');else pass(mod+' rejects completion without essential practical cases');
    await p.evaluate(([m,req])=>{const pg={complete:{}};req.forEach(i=>pg.complete[String(i)]=true);localStorage.setItem('tvaPracticeGateV1_'+m,JSON.stringify(pg))},[mod,required]);
    await p.reload({waitUntil:'domcontentloaded'});await p.waitForTimeout(250);await finish(p);await p.waitForTimeout(100);
    if(await dash(p,mod)!=='done')fail(mod+' rejected complete practical gate');else pass(mod+' accepts QCM + sections + 4 essential cases');
  }catch(e){fail(mod+' practice gate runtime: '+e.message)}
  await p.close();
}
await browser.close();if(failures){console.error(`\nPRACTICE GATE QA: ${failures} failure(s)`);process.exit(1)}console.log('\nPRACTICE GATE QA: PASS');
