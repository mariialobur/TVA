'use strict';
import fs from 'node:fs';

// 1) M04 source has two browser-open DIV ancestors at the theory -> legislation boundary.
// Close the unclosed theory-block and sec-theory in source so later sections are true siblings.
const m04='m04-tva-comptabilite-suisse-base.html';
let html=fs.readFileSync(m04,'utf8');
const marker='<!-- ══════════════════ LÉGISLATION ══════════════════ -->';
if(!html.includes(marker))throw new Error('M04 legislation marker not found');
if(!html.includes('<!-- M04 DOM HARDENING: close legacy theory wrappers -->')){
  html=html.replace(marker,'<!-- M04 DOM HARDENING: close legacy theory wrappers -->\n</div>\n</div>\n'+marker);
  fs.writeFileSync(m04,html);
}

// 2) Make written dossier a first-class completion requirement in the central legacy gate.
const gateFile='course-legacy-gate.js';
let gate=fs.readFileSync(gateFile,'utf8');
const oldStatus=`    const missing=required.filter(s=>!gate.visited[s]);\n    return {ok:missing.length===0&&gate.quizPassed,missing};`;
const newStatus=`    const missing=required.filter(s=>!gate.visited[s]);\n    let capstoneOk=true;\n    if(cfg.capstone){\n      try{capstoneOk=JSON.parse(localStorage.getItem('tvaLegacyCapstoneV1_'+cfg.module)||'{}').modelShown===true}catch(e){capstoneOk=false}\n    }\n    return {ok:missing.length===0&&gate.quizPassed&&capstoneOk,missing,capstoneOk};`;
if(gate.includes(oldStatus))gate=gate.replace(oldStatus,newStatus);
else if(!gate.includes("tvaLegacyCapstoneV1_"))throw new Error('legacy gate status target not found');
const oldToast=`if(!st.ok){toast(d,'Validation refusée : '+(st.missing.length?'sections à parcourir : '+st.missing.join(', ')+'. ':'')+(!gate.quizPassed?'QCM ≥ 75 % requis.':''),false);return}`;
const newToast=`if(!st.ok){toast(d,'Validation refusée : '+(st.missing.length?'sections à parcourir : '+st.missing.join(', ')+'. ':'')+(!gate.quizPassed?'QCM ≥ 75 % requis. ':'')+(cfg.capstone&&!st.capstoneOk?'Dossier professionnel à réponse libre requis.':''),false);return}`;
if(gate.includes(oldToast))gate=gate.replace(oldToast,newToast);
else if(!gate.includes('Dossier professionnel à réponse libre requis.'))throw new Error('legacy gate toast target not found');
fs.writeFileSync(gateFile,gate);
console.log('Legacy capstone hardening applied.');
