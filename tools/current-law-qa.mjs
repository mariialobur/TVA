'use strict';
import fs from 'node:fs';
const read=f=>fs.readFileSync(f,'utf8');
let bad=0;const fail=m=>{bad++;console.error('FAIL:',m)},ok=m=>console.log('OK:',m);

const m10=read('m10-digital-plateformes-ecommerce.html');
const m10p=read('m10-current-law-2026.js');
if(!m10.includes('m10-digital-plateformes-ecommerce-core.html')||!m10.includes('m10-current-law-2026.js'))fail('M10 wrapper/core/current-law contract missing');else ok('M10 wrapper loads core + current-law patch');
try{new Function(m10p);ok('M10 current-law patch parses')}catch(e){fail('M10 current-law patch syntax: '+e.message)}
for(const n of ['≤ CHF 5','n’excédant pas CHF 5'])if(!m10p.includes(n))fail('M10 inclusive CHF 5 correction missing: '+n);
if(m10p.includes("['actuellement <5 CHF','actuellement <5 CHF']"))fail('M10 CHF 5 patch is a no-op');
ok('M10 small-consignment cutoff sentinel evaluated');

const m11=read('m11-controle-afc-tva.html'),m11p=read('m11-current-law-2026.js');
if(!m11.includes('m11-controle-afc-tva-core.html')||!m11.includes('m11-current-law-2026.js'))fail('M11 wrapper/core/current-law contract missing');else ok('M11 wrapper loads core + current-law patch');
try{new Function(m11p);ok('M11 current-law patch parses')}catch(e){fail('M11 current-law patch syntax: '+e.message)}
for(const n of ['Après interruption par l’assujetti','Nouveau délai de 5 ans (art. 42 al. 2)','interruption par l’AFC/recours → nouveau délai 2 ans'])if(!m11p.includes(n))fail('M11 art. 42 interruption branch missing: '+n);
if(!m11p.includes('10 ans'))fail('M11 absolute prescription guard missing');
else ok('M11 art. 42 taxpayer/AFC interruption branches hardened');

const q4a=read('m14-q4a.js');
if(!q4a.includes('inférieur ou égal à CHF 5')||!q4a.includes("n’excède pas CHF 5"))fail('M14 Q95 does not teach inclusive CHF 5 cutoff');
if(q4a.includes('un montant d’impôt à l’importation inférieur à CHF 5\"'))fail('M14 Q95 regressed to exclusive < CHF 5');
else ok('M14 Q95 aligned with ≤ CHF 5');

const m14=read('m14-examen-blanc-synthese-finale.html'),m14p=read('m14-current-law-2026.js');
if(!m14.includes('m14-current-law-2026.js'))fail('M14 current-law patch not loaded');
if(!(m14.indexOf('m14-q4b.js')<m14.indexOf('m14-current-law-2026.js')&&m14.indexOf('m14-current-law-2026.js')<m14.indexOf('m14-engine.js')))fail('M14 current-law patch must load after pools and before engine');
if(!m14.includes('impôt à l’importation ≤ CHF 5'))fail('M14 snapshot does not show inclusive CHF 5 cutoff');
try{new Function(m14p);ok('M14 current-law patch parses')}catch(e){fail('M14 current-law patch syntax: '+e.message)}
for(const n of ['affecte ou compte affecter exclusivement à des fins d’habitation','Le critère actuel n’est plus formulé comme une utilisation exclusivement «privée»'])if(!m14p.includes(n))fail('M14 immobilier current-law wording missing: '+n);
if(!m14.includes('Droit vérifié : 11.09.2026')||!m14.includes('Repères juridiques au 11.09.2026'))fail('M14 public current-law date labels not refreshed');
else ok('M14 current-law snapshot and art. 22 wording hardened');

const m13entry=read('m13-communication-data.js'),m13p=read('m13-current-law-2026.js');
if(!m13entry.includes('m13-communication-data-core.js')||!m13entry.includes('m13-current-law-2026.js'))fail('M13 data wrapper/core/current-law contract missing');
if(!m13p.includes('Art.42/69')||!m13p.includes('acte interruptif au sens de l’art. 42'))fail('M13 art. 42/69 prescription nuance missing');
else ok('M13 art. 42/69 prescription nuance present');

const m12=read('m12-jurisprudence-bank.js');
if(!m12.includes('ATF 149 IV 395')||!m12.includes('TVA à l’importation · soustraction intentionnelle')||!m12.includes('art. 96 al. 4 let. a'))fail('M12 ATF 149 IV 395 import-VAT scope missing');
else ok('M12 ATF 149 IV 395 scope remains import-specific');

if(bad){console.error(`\nCURRENT-LAW QA: ${bad} failure(s)`);process.exit(1)}
console.log('\nCURRENT-LAW QA: PASS');
