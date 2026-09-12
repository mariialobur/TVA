'use strict';
import fs from 'node:fs';
import vm from 'node:vm';
const read=f=>fs.readFileSync(f,'utf8');
const files=['m14-q1.js','m14-q2.js','m14-q3.js','m14-q4a.js','m14-q4b.js'];
const box={window:{},console};vm.createContext(box);for(const f of files)vm.runInContext(read(f),box,{filename:f});
const Q=['M14_POOL_1','M14_POOL_2','M14_POOL_3','M14_POOL_4A','M14_POOL_4B'].flatMap(k=>box.window[k]||[]);
let failures=0;const fail=m=>{failures++;console.error('FAIL:',m)},ok=m=>console.log('OK:',m);
if(Q.length!==130)fail('expected 130 questions, got '+Q.length);else ok('130-question bank intact');
const ids=new Set(),texts=new Set(),mods={};for(const q of Q){if(ids.has(q.id))fail('duplicate id '+q.id);ids.add(q.id);if(texts.has(q.question))fail('duplicate question '+q.id);texts.add(q.question);if(!Array.isArray(q.options)||q.options.length!==4)fail(q.id+' must have 4 options');if(new Set(q.options).size!==4)fail(q.id+' duplicate options');if(!Number.isInteger(q.correct)||q.correct<0||q.correct>3)fail(q.id+' invalid correct index');const m=mods[q.module]||(mods[q.module]={n:0,F:0,M:0,D:0});m.n++;m[q.difficulty]=(m[q.difficulty]||0)+1}
for(let i=1;i<=13;i++){const m='M'+String(i).padStart(2,'0'),x=mods[m];if(!x||x.n!==10)fail(m+' must have 10 questions');else if((x.F||0)<2||(x.M||0)<4||(x.D||0)<3)fail(m+' difficulty coverage too weak: '+JSON.stringify(x))}if(!failures)ok('module and difficulty coverage intact');
const engine=read('m14-engine.js');try{new Function(engine);ok('M14 engine JavaScript parses')}catch(e){fail('M14 engine syntax: '+e.message)}for(const n of ['function prep(q)','const order=shuffle(q.options.map((_,i)=>i))','c.correct=order.indexOf(q.correct)','final:{label:\'Final Pro · 52Q\'','pattern:[\'F\',\'M\',\'M\',\'D\']','pct>=75&&moduleFloor'])if(!engine.includes(n))fail('runtime exam invariant missing: '+n);if(engine.includes('function prep(q)')&&engine.includes('c.correct=order.indexOf(q.correct)'))ok('runtime option shuffle remaps correct answer');
const forbidden=/Temporal gate|Negative research|bank M12|historical bridge/i;for(const q of Q){const s=[q.competence,q.question,q.explanation].join(' ');if(forbidden.test(s))fail('internal learner-facing wording remains in Q'+q.id+': '+s.match(forbidden)[0])}
const byId=Object.fromEntries(Q.map(q=>[q.id,q]));
if(!/affecte ou compte affecter exclusivement à des fins d’habitation/i.test(byId[19]?.question||''))fail('Q19 current art.22 habitation wording missing');
if(!String(byId[95]?.options?.[0]||'').includes('inférieur ou égal à CHF 5'))fail('Q95 inclusive CHF 5 criterion missing');
const q103=(byId[103]?.options?.[0]||'')+' '+(byId[103]?.explanation||'');for(const n of ['cinq ans','deux ans','dix ans'])if(!q103.includes(n))fail('Q103 art.42 branch missing '+n);
if(!engine.includes('x.length>=500&&capWords(x)>=80')||!engine.includes('80 mots')||!engine.includes('500 caractères'))fail('M14 capstone written threshold must be 80 words / 500 chars');else ok('M14 capstones require substantive written response');
const abs=/\b(toujours|jamais|automatiquement|uniquement|obligatoirement)\b/i,longIds=[],absoluteIds=[];for(const q of Q){const lens=q.options.map(x=>String(x).length),avg=lens.reduce((a,b)=>a+b,0)/4,cl=lens[q.correct];if(cl>avg*1.65&&cl-avg>22)longIds.push(q.id);const distract=q.options.filter((_,i)=>i!==q.correct);if(!abs.test(q.options[q.correct])&&distract.filter(x=>abs.test(x)).length>=2)absoluteIds.push(q.id)}
console.log('STYLE METRICS: correct-much-longer='+longIds.length+'; multi-absolute-distractors='+absoluteIds.length);console.log('LENGTH-SIGNAL IDS:',longIds.join(','));console.log('ABSOLUTE-LEAK IDS:',absoluteIds.join(','));if(longIds.length>35)fail('too many length-signalled correct answers: '+longIds.length);if(absoluteIds.length>28)fail('too many questions signalled by absolutist distractors: '+absoluteIds.length);
if(failures){console.error('\nM14 RED-TEAM QA: '+failures+' failure(s)');process.exit(1)}console.log('\nM14 RED-TEAM QA: PASS');
