'use strict';
import { chromium } from 'playwright';
const base=process.env.BASE_URL||'http://127.0.0.1:4173/';
const mods=[
  ['M09','m09-secteurs-sensibles-tva.html',9],
  ['M10','m10-digital-plateformes-ecommerce.html',11],
  ['M11','m11-controle-afc-tva.html',11],
  ['M12','m12-jurisprudence-lab-tva.html',11],
  ['M13','m13-communication-fiscale-cabinet.html',11]
];
const browser=await chromium.launch({headless:true});let failures=0;
const fail=m=>{failures++;console.error('FAIL:',m)},pass=m=>console.log('OK:',m);
async function work(p){const el=p.locator('#module');if(await el.count()){const h=await p.waitForSelector('#module'),f=await h.contentFrame();await f.waitForLoadState('load');return f}return p}
for(const [mod,file,idx] of mods){
  const p=await browser.newPage();
  try{
    await p.goto(base+file,{waitUntil:'domcontentloaded'});await p.evaluate(()=>localStorage.clear());await p.reload({waitUntil:'domcontentloaded'});await p.waitForTimeout(350);
    const w=await work(p);try{await w.evaluate(()=>{if(typeof go==='function')go('cases')})}catch(e){}
    const card=w.locator('#sec-cases .capstone-dossier');await card.waitFor({timeout:8000});
    if(await card.count()!==1)fail(mod+' capstone dossier missing');
    else pass(mod+' exposes one written capstone dossier');
    if(await card.locator('.opt').count()!==0)fail(mod+' capstone still exposes A/B/C/D options');
    else pass(mod+' capstone replaces multiple-choice steps');
    const ta=card.locator('.capstone-draft'),btn=card.locator('.capstone-compare');
    if(!await btn.isDisabled())fail(mod+' model available before draft');
    await ta.fill('Analyse trop courte.');if(!await btn.isDisabled())fail(mod+' accepts undersized draft');
    const text=('Qualification base légale traitement TVA preuves risques recommandation. ').repeat(12);
    await ta.fill(text);if(await btn.isDisabled())fail(mod+' rejects substantive draft');
    else pass(mod+' requires substantive written position before model');
    await btn.click();await p.waitForTimeout(100);
    if(!await card.locator('.capstone-model').isVisible())fail(mod+' model did not reveal');
    const state=await p.evaluate(([m,i])=>{let c={},g={};try{c=JSON.parse(localStorage.getItem('tvaCapstoneDossierV1_'+m)||'{}')}catch(e){}try{g=JSON.parse(localStorage.getItem('tvaPracticeGateV1_'+m)||'{}')}catch(e){}return {model:!!c.modelShown,practice:g.complete?.[String(i)]===true}},[mod,idx]);
    if(!state.model||!state.practice)fail(mod+' capstone completion not persisted into practical gate');
    else pass(mod+' written dossier persists and satisfies its essential-case gate');
  }catch(e){fail(mod+' capstone runtime: '+e.message)}
  await p.close();
}
await browser.close();if(failures){console.error(`\nCAPSTONE DOSSIER QA: ${failures} failure(s)`);process.exit(1)}console.log('\nCAPSTONE DOSSIER QA: PASS');
