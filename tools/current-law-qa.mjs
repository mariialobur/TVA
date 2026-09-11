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
if(!bad)ok('M10 small-consignment cutoff hardened at ≤ CHF 5');

const q4a=read('m14-q4a.js');
if(!q4a.includes('inférieur ou égal à CHF 5')||!q4a.includes("n’excède pas CHF 5"))fail('M14 Q95 does not teach inclusive CHF 5 cutoff');
if(q4a.includes('un montant d’impôt à l’importation inférieur à CHF 5\"'))fail('M14 Q95 regressed to exclusive < CHF 5');
else ok('M14 Q95 aligned with ≤ CHF 5');

const m13entry=read('m13-communication-data.js'),m13p=read('m13-current-law-2026.js');
if(!m13entry.includes('m13-communication-data-core.js')||!m13entry.includes('m13-current-law-2026.js'))fail('M13 data wrapper/core/current-law contract missing');
if(!m13p.includes('Art.42/69')||!m13p.includes('acte interruptif au sens de l’art. 42'))fail('M13 art. 42/69 prescription nuance missing');
else ok('M13 art. 42/69 prescription nuance present');

const m12=read('m12-jurisprudence-bank.js');
if(!m12.includes('ATF 149 IV 395')||!m12.includes('TVA à l’importation · soustraction intentionnelle')||!m12.includes('art. 96 al. 4 let. a'))fail('M12 ATF 149 IV 395 import-VAT scope missing');
else ok('M12 ATF 149 IV 395 scope remains import-specific');

if(bad){console.error(`\nCURRENT-LAW QA: ${bad} failure(s)`);process.exit(1)}
console.log('\nCURRENT-LAW QA: PASS');
