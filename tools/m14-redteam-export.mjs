'use strict';
import fs from 'node:fs';
import vm from 'node:vm';
const files=['m14-q1.js','m14-q2.js','m14-q3.js','m14-q4a.js','m14-q4b.js'];
const box={window:{},console};vm.createContext(box);for(const f of files)vm.runInContext(fs.readFileSync(f,'utf8'),box,{filename:f});
const pools=['M14_POOL_1','M14_POOL_2','M14_POOL_3','M14_POOL_4A','M14_POOL_4B'].flatMap(k=>box.window[k]||[]);
const absRe=/\b(toujours|jamais|automatiquement|uniquement|obligatoirement|aucun(?:e)?|tous?|toutes?)\b/i;
const norm=s=>String(s||'').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9%]+/g,' ').trim();
const byCorrect=[0,0,0,0],byModule={},flagged=[];
for(const q of pools){
  byCorrect[q.correct]++;
  const m=byModule[q.module]||(byModule[q.module]={n:0,correct:[0,0,0,0],F:0,M:0,D:0});m.n++;m.correct[q.correct]++;m[q.difficulty]=(m[q.difficulty]||0)+1;
  const lens=q.options.map(x=>String(x).length),cl=lens[q.correct],avg=lens.reduce((a,b)=>a+b,0)/lens.length;
  const correctAbs=absRe.test(q.options[q.correct]),distractorAbs=q.options.map((x,i)=>i!==q.correct&&absRe.test(x)).filter(Boolean).length;
  const longest=cl===Math.max(...lens),shortest=cl===Math.min(...lens);
  const reasons=[];
  if(longest&&cl>=avg*1.35)reasons.push('correct-much-longer');
  if(shortest&&cl<=avg*.65)reasons.push('correct-much-shorter');
  if(!correctAbs&&distractorAbs>=2)reasons.push('absolutes-mainly-in-distractors');
  if(q.correct===0)reasons.push('correct=A');
  if(reasons.length)flagged.push({id:q.id,module:q.module,difficulty:q.difficulty,question:q.question,correct:q.correct,source:q.source,reasons,options:q.options,explanation:q.explanation,lengths:lens});
}
const qSeen=new Map(),dupQ=[];for(const q of pools){const k=norm(q.question);if(qSeen.has(k))dupQ.push([qSeen.get(k),q.id]);else qSeen.set(k,q.id)}
const optionSeen=new Map(),repeatOptions=[];for(const q of pools)for(const o of q.options){const k=norm(o);if(k.length<12)continue;const arr=optionSeen.get(k)||[];arr.push(q.id);optionSeen.set(k,arr)}for(const [text,ids] of optionSeen)if(ids.length>=3)repeatOptions.push({text,ids});
const report={total:pools.length,correctPosition:{A:byCorrect[0],B:byCorrect[1],C:byCorrect[2],D:byCorrect[3]},byModule,duplicateQuestions:dupQ,repeatedOptionPhrases:repeatOptions.sort((a,b)=>b.ids.length-a.ids.length).slice(0,50),flaggedCount:flagged.length,flagged};
fs.writeFileSync('tools/m14-redteam-report.json',JSON.stringify(report,null,2));
fs.writeFileSync('tools/m14-redteam-corpus.json',JSON.stringify(pools,null,2));
console.log(JSON.stringify({total:report.total,correctPosition:report.correctPosition,flaggedCount:report.flaggedCount,duplicateQuestions:dupQ.length,repeatedOptionPhrases:report.repeatedOptionPhrases.length},null,2));
