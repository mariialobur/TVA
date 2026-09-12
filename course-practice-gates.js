'use strict';
(()=>{
  const CONFIG={
    M09:{required:[2,5,7,9]},
    M10:{required:[4,6,9,11]},
    M11:{required:[2,4,9,11]},
    M12:{required:[0,6,7,11]},
    M13:{required:[1,4,6,11]}
  };
  const DASH='tvaSpecialisteTvaDashboardV1';
  const mod=(location.pathname.match(/\/m(09|10|11|12|13)-/i)||[])[1];
  const MODULE=mod?'M'+mod:null;
  if(!MODULE||!CONFIG[MODULE])return;
  const cfg=CONFIG[MODULE],STORE='tvaPracticeGateV1_'+MODULE;

  function load(){try{return JSON.parse(localStorage.getItem(STORE)||'{}')}catch(e){return {}}}
  function save(v){try{localStorage.setItem(STORE,JSON.stringify(v))}catch(e){}}
  function state(){const s=load();if(!s.steps)s.steps={};if(!s.complete)s.complete={};return s}
  function requiredDone(s=state()){return cfg.required.filter(i=>s.complete[String(i)]===true).length}
  function allDone(){return requiredDone()===cfg.required.length}
  function cases(doc){return [...doc.querySelectorAll('#sec-cases .case')]}
  function stepsIn(card){return [...card.querySelectorAll('.qstep,.qs')]}
  function isCorrect(btn){
    if(btn.dataset.ok!==undefined)return btn.dataset.ok==='1';
    const oc=btn.getAttribute('onclick')||'';
    return /(?:caseAnswer|ans)\s*\(\s*this\s*,\s*true\s*\)/.test(oc);
  }
  function caseTitle(card,idx){
    const h=card.querySelector('.casehead,.caseh,h3');
    return (h?.textContent||('Cas '+(idx+1))).replace(/\s*Cas requis.*$/,'').trim();
  }

  function addStyles(doc){
    if(doc.getElementById('practice-gate-style'))return;
    const st=doc.createElement('style');st.id='practice-gate-style';st.textContent=`
      .practice-required{outline:2px solid rgba(201,168,76,.55);outline-offset:2px}
      .practice-required-badge{display:inline-block;margin-left:8px;padding:3px 7px;border-radius:999px;background:#F3E8C2;color:#654900;font-size:10px;font-weight:800;vertical-align:middle}
      .practice-required.practice-complete{outline-color:#71A589}
      .practice-required.practice-complete .practice-required-badge{background:#E7F5EC;color:#245C3E}
      #practice-gate-box{border-left:4px solid #C9A84C;background:#fffaf0}
      #practice-gate-box.practice-ok{border-left-color:#2A6B48;background:#E7F5EC}
      #practice-gate-box p{margin:5px 0 0}
    `;doc.head.appendChild(st);
  }

  function decorate(doc){
    if(!doc?.body)return;
    addStyles(doc);
    const list=cases(doc);if(!list.length)return;
    const s=state();
    cfg.required.forEach(idx=>{
      const card=list[idx];if(!card)return;
      card.classList.add('practice-required');
      card.classList.toggle('practice-complete',s.complete[String(idx)]===true);
      const host=card.querySelector('.casehead,.caseh,h3')||card;
      let badge=card.querySelector('.practice-required-badge');
      if(!badge){badge=doc.createElement('span');badge.className='practice-required-badge';host.appendChild(badge)}
      badge.textContent=s.complete[String(idx)]===true?'✓ Cas essentiel travaillé':'Cas essentiel · requis';
    });
    const sec=doc.getElementById('sec-cases');if(!sec)return;
    let box=doc.getElementById('practice-gate-box');
    if(!box){
      box=doc.createElement('div');box.id='practice-gate-box';box.className='card';
      const hero=sec.querySelector('.hero');
      if(hero)hero.insertAdjacentElement('afterend',box);else sec.prepend(box);
    }
    const n=requiredDone(s);box.classList.toggle('practice-ok',n===cfg.required.length);
    box.innerHTML='<strong>Validation pratique · '+n+'/'+cfg.required.length+' cas essentiels</strong><p>Travaillez intégralement les quatre cas marqués « requis ». Le QCM mesure la maîtrise des règles ; ces dossiers vérifient que vous savez les appliquer dans une situation professionnelle.</p>';
    const complete=doc.querySelector('.complete');
    if(complete&&!complete.querySelector('.practice-validation-note')){
      const p=doc.createElement('p');p.className='practice-validation-note';p.textContent='La validation du module exige également les 4 cas essentiels marqués dans la section Cas pratiques.';
      const btn=complete.querySelector('button');if(btn)complete.insertBefore(p,btn);else complete.appendChild(p);
    }
  }

  function record(doc,btn){
    const card=btn.closest('.case');if(!card)return;
    const list=cases(doc),idx=list.indexOf(card);if(!cfg.required.includes(idx))return;
    const step=btn.closest('.qstep,.qs');if(!step)return;
    const ss=stepsIn(card),si=ss.indexOf(step);if(si<0)return;
    const s=state(),k=String(idx);if(!s.steps[k])s.steps[k]={};
    s.steps[k][String(si)]={done:true,correct:isCorrect(btn)};
    s.complete[k]=ss.length>0&&ss.every((_,j)=>s.steps[k]?.[String(j)]?.done===true);
    s.updatedAt=Date.now();save(s);decorate(doc);
  }

  function completionMessage(doc){return doc.getElementById('complete-msg')||doc.getElementById('completeMsg')}
  function block(doc,win){
    const n=requiredDone(),msg=completionMessage(doc);
    if(msg)msg.textContent='Validation incomplète : '+n+'/'+cfg.required.length+' cas essentiels travaillés. Terminez les quatre cas marqués « requis », puis validez à nouveau le module.';
    try{if(typeof win.go==='function')win.go('cases')}catch(e){}
    decorate(doc);
  }

  function guardFinish(win,doc){
    if(!win||win.__tvaPracticeGateInstalled)return;
    const original=win.finishModule;if(typeof original!=='function')return;
    win.__tvaPracticeGateInstalled=true;
    win.__tvaPracticeOriginalFinish=original;
    win.finishModule=function(...args){
      if(!allDone()){block(doc,win);return false}
      return original.apply(this,args);
    };
  }

  function attach(doc,win){
    if(!doc?.body)return false;
    decorate(doc);guardFinish(win,doc);
    if(!doc.body.dataset.practiceGateListener){
      doc.body.dataset.practiceGateListener='1';
      doc.addEventListener('click',e=>{
        const btn=e.target.closest?.('.opt');if(!btn||!btn.closest('#sec-cases'))return;
        setTimeout(()=>record(doc,btn),0);
      },true);
    }
    return true;
  }

  function init(){
    const frame=document.getElementById('module');
    if(!frame){
      attach(document,window);
      setTimeout(()=>attach(document,window),150);
      return;
    }
    const apply=()=>{try{return attach(frame.contentDocument,frame.contentWindow)}catch(e){return false}};
    frame.addEventListener('load',()=>{setTimeout(apply,0);setTimeout(apply,150)});
    let tries=0;const t=setInterval(()=>{tries++;if(apply()||tries>80)clearInterval(t)},50);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
