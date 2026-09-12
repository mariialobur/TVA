'use strict';
import { chromium } from 'playwright';
const base=process.env.BASE_URL||'http://127.0.0.1:4173/';
const browser=await chromium.launch({headless:true});
let failures=0;
const fail=m=>{failures++;console.error('FAIL:',m)},pass=m=>console.log('OK:',m);
const forbidden=[/Red-team/i,/Legal QA/i,/truth map/i,/Current-law snapshot/i,/Final Legal QA/i,/Practice & legal QA/i,/Course gate/i,/Gate 1/i,/Gate 2/i,/← Tableau de bord/i];
async function visibleText(page,file){
  await page.goto(base+file,{waitUntil:'domcontentloaded'});
  const iframe=page.locator('#module');
  if(await iframe.count()){
    const h=await iframe.elementHandle(),f=await h.contentFrame();
    await f.waitForLoadState('load');
    await page.waitForTimeout(900);
    return await f.locator('body').innerText();
  }
  await page.waitForTimeout(100);
  return await page.locator('body').innerText();
}
for(const file of ['m09-secteurs-sensibles-tva.html','m10-digital-plateformes-ecommerce.html','m11-controle-afc-tva.html','m12-jurisprudence-lab-tva.html','m13-communication-fiscale-cabinet.html','m14-examen-blanc-synthese-finale.html']){
  const p=await browser.newPage();
  try{
    const t=await visibleText(p,file);
    const hits=forbidden.filter(r=>r.test(t)).map(r=>r.source);
    if(hits.length)fail(file+' exposes internal learner-facing vocabulary: '+hits.join(', '));else pass(file+' public copy is learner-facing');
  }catch(e){fail(file+' UI audit: '+e.message)}
  await p.close();
}
{
  const p=await browser.newPage();
  try{
    await p.goto(base+'index.html',{waitUntil:'domcontentloaded'});
    const stages=await p.locator('.stage').count(),workshops=await p.locator('.practice-card').count(),cards=await p.locator('.card').count();
    const cta=(await p.locator('#continueBtn').innerText()).trim();
    if(stages!==4)fail('dashboard stage count '+stages+' != 4');else pass('dashboard renders 4 learning stages');
    if(workshops!==3)fail('dashboard workshop count '+workshops+' != 3');else pass('dashboard renders 3 practice workshops');
    if(cards!==14)fail('dashboard module card count '+cards+' != 14');else pass('dashboard still renders 14 modules');
    if(!/Commencer le parcours|Continuer · M\d{2}/.test(cta))fail('dashboard primary CTA is not actionable: '+cta);else pass('dashboard primary CTA is actionable');
  }catch(e){fail('dashboard learner-facing audit: '+e.message)}
  await p.close();
}
await browser.close();
if(failures){console.error(`\nSTUDENT-FACING QA: ${failures} failure(s)`);process.exit(1)}
console.log('\nSTUDENT-FACING QA: PASS');
