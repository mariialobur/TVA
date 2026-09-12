'use strict';
import { chromium } from 'playwright';
const base=process.env.BASE_URL||'http://127.0.0.1:4173/';
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
  await f.locator('#sec-cases').waitFor({state:'visible',timeout:8000});
}
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
    await f.evaluate(()=>{const b=document.createElement('button');b.id='qa-finish-probe';b.textContent='Terminer '+(window.parent.COURSE_GATE_CONFIG?.module||'module');b.setAttribute('onclick','finishModule()');document.body.appendChild(b);b.click()});
    await p.waitForTimeout(80);if(!await f.locator('#legacy-capstone-toast').count())fail(mod+' completion guard did not block unfinished dossier');else pass(mod+' blocks module completion before dossier comparison');
    await f.evaluate(()=>document.getElementById('legacy-capstone-toast')?.remove());
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
