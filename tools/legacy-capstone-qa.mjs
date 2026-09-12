'use strict';
import { chromium } from 'playwright';
const base=process.env.BASE_URL||'http://127.0.0.1:4173/';
const DASH='tvaSpecialisteTvaDashboardV1';
const sections=['theory','legis','cases','errors','quiz','memo','vocab','cheat'];
const mods=[
  ['M04','m04-tva-comptabilite-suisse.html'],
  ['M05','m05-deduction-impot-prealable-dip.html'],
  ['M06','m06-territorialite-tva-internationale.html'],
  ['M08','m08-immobilier-construction-tva.html']
];
const browser=await chromium.launch({headless:true});let failures=0;
const fail=m=>{failures++;console.error('FAIL:',m)},pass=m=>console.log('OK:',m);
async function work(p){const h=await p.waitForSelector('#module',{timeout:10000}),f=await h.contentFrame();if(!f)throw new Error('iframe unavailable');await f.waitForLoadState('load');return f}
async function openCases(f){
  const nav=f.locator('[data-section="cases"], [data-sec="cases"], [data-s="cases"]').first();
  if(await nav.count())await nav.click();
  else await f.evaluate(()=>{if(typeof goto==='function')goto('cases');else if(window.NAV&&typeof NAV.go==='function')NAV.go('cases')});
  try{await f.locator('#sec-cases').waitFor({state:'visible',timeout:2500})}
  catch(e){
    const chain=await f.evaluate(()=>{let el=document.getElementById('sec-cases'),out=[];for(let i=0;el&&i<8;i++,el=el.parentElement){const cs=getComputedStyle(el);out.push({tag:el.tagName,id:el.id,cls:el.className,display:cs.display,visibility:cs.visibility,opacity:cs.opacity})}return out});
    throw new Error('cases section remains hidden; ancestor chain='+JSON.stringify(chain));
  }
}
async function clickRealFinish(f){
  const b=f.locator('button[onclick*="finishModule"],button[onclick*="PROG.finish"],button[onclick*="goNextModule"],button[onclick*="PROG.goNext"]').last();
  if(!await b.count())throw new Error('real completion button not found');
  await b.dispatchEvent('click');
}
async function seedOtherGateRequirements(p,mod){
  await p.evaluate(([m,secs])=>{const visited={};secs.forEach(s=>visited[s]=true);localStorage.setItem('tva_course_gate_'+m+'_v2',JSON.stringify({visited,quizPassed:true,quizScore:75,done:false}))},[mod,sections]);
}
async function dashboardState(p,mod){return p.evaluate(([k,m])=>{try{return JSON.parse(localStorage.getItem(k)||'{}')[m]||null}catch(e){return null}},[DASH,mod])}
for(const [mod,file] of mods){
  const p=await browser.newPage();
  try{
    await p.goto(base+file,{waitUntil:'domcontentloaded'});await p.evaluate(()=>localStorage.clear());await p.reload({waitUntil:'domcontentloaded'});const f=await work(p);await p.waitForTimeout(300);await openCases(f);
    const card=f.locator('#legacy-capstone-'+mod);await card.waitFor({state:'visible',timeout:8000});
    if(await card.count()!==1)fail(mod+' written dossier missing');else pass(mod+' exposes one mandatory written dossier');
    const ta=card.locator('.legacy-capstone-draft'),btn=card.locator('.legacy-capstone-btn');
    if(!await btn.isDisabled())fail(mod+' model available before draft');
    await ta.fill('Analyse trop courte.');if(!await btn.isDisabled())fail(mod+' accepts undersized draft');
    const text=('Qualification base juridique traitement TVA preuve risque action recommandée contrôle documentation. ').repeat(12);
    await ta.fill(text);if(await btn.isDisabled())fail(mod+' rejects substantive draft');else pass(mod+' requires 80 words / 500 characters before model');

    // Isolate the written dossier as the only unmet completion condition.
    await seedOtherGateRequirements(p,mod);
    await clickRealFinish(f);await p.waitForTimeout(120);
    const done=await dashboardState(p,mod),toastText=await f.locator('#legacy-capstone-toast,#course-gate-toast').allTextContents();
    if(done==='done')fail(mod+' completed while written dossier was still unfinished');
    else if(!toastText.some(x=>/dossier professionnel|réponse libre|dossier/i.test(x)))fail(mod+' blocked completion but did not identify the missing written dossier');
    else pass(mod+' blocks completion when dossier is the only unmet gate');
    await f.evaluate(()=>{document.getElementById('legacy-capstone-toast')?.remove();document.getElementById('course-gate-toast')?.remove()});

    await btn.click();await p.waitForTimeout(100);
    if(!await card.locator('.legacy-capstone-model').isVisible())fail(mod+' model did not reveal');
    const st=await p.evaluate(m=>{try{return JSON.parse(localStorage.getItem('tvaLegacyCapstoneV1_'+m)||'{}')}catch(e){return {}}},mod);
    if(st.modelShown!==true||String(st.draft||'').length<500)fail(mod+' dossier completion not persisted');else pass(mod+' written dossier persists after comparison');
    await p.reload({waitUntil:'domcontentloaded'});const f2=await work(p);await p.waitForTimeout(250);await openCases(f2);
    const card2=f2.locator('#legacy-capstone-'+mod);await card2.waitFor({state:'visible',timeout:8000});if(!await card2.locator('.legacy-capstone-model').isVisible())fail(mod+' persisted model state lost after reload');else pass(mod+' persisted dossier survives reload');
  }catch(e){fail(mod+' legacy capstone runtime: '+e.message)}
  await p.close();
}
await browser.close();if(failures){console.error(`\nLEGACY CAPSTONE QA: ${failures} failure(s)`);process.exit(1)}console.log('\nLEGACY CAPSTONE QA: PASS');
