'use strict';
(()=>{
  const cfg=window.COURSE_GATE_CONFIG||{};
  const frame=document.getElementById('module');
  if(!frame||!cfg.module||!cfg.src)return;
  const DASH='tvaSpecialisteTvaDashboardV1';
  const GKEY='tva_course_gate_'+cfg.module+'_v2';
  const required=cfg.sections||['theory','legis','cases','errors','quiz','memo','vocab','cheat'];
  let gate={visited:{theory:true},quizPassed:false,quizScore:0,done:false};
  try{gate=Object.assign(gate,JSON.parse(localStorage.getItem(GKEY)||'{}'));gate.visited=Object.assign({theory:true},gate.visited||{})}catch(e){}
  const save=()=>{try{localStorage.setItem(GKEY,JSON.stringify(gate))}catch(e){}};
  const esc=s=>String(s||'').replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  function mark(s){if(required.includes(s)){gate.visited[s]=true;save()}}
  function inferObject(o){
    if(!o||typeof o!=='object')return;
    required.forEach(s=>{
      if(o[s]===1||o[s]===true)gate.visited[s]=true;
      if(o.done&&(o.done[s]===1||o.done[s]===true))gate.visited[s]=true;
      if(o.visited&&(o.visited[s]===1||o.visited[s]===true))gate.visited[s]=true;
    });
    if(required.includes(o.section))gate.visited[o.section]=true;
    const pass=o.quiz_passed===1||o.quiz_passed===true||o.quizPassed===1||o.quizPassed===true;
    const scores=[o.quiz_score,o.quizScore,o.quiz_best,o.quizBest,o.bestScore,o.lastScore,o.quiz&&o.quiz.score,o.quiz&&o.quiz.best];
    const score=Math.max(0,...scores.map(Number).filter(Number.isFinite));
    if(pass||score>=75){gate.quizPassed=true;gate.quizScore=Math.max(gate.quizScore||0,score||75)}
  }
  function inferStorage(){
    for(let i=0;i<localStorage.length;i++){
      const k=localStorage.key(i)||'';
      if(!cfg.storagePrefixes?.some(p=>k.startsWith(p)))continue;
      try{inferObject(JSON.parse(localStorage.getItem(k)||'{}'))}catch(e){}
    }
    save();
  }
  function scoreFromDom(d){
    const sels=['#r-pct','#score','#result-score','#quiz-score','.results-score','.score'];
    let best=gate.quizScore||0;
    sels.forEach(sel=>d.querySelectorAll(sel).forEach(el=>{
      const style=getComputedStyle(el);
      if(style.display==='none'||style.visibility==='hidden')return;
      const m=(el.textContent||'').match(/(\d{1,3})(?:\s*%|$)/);
      if(m)best=Math.max(best,Number(m[1]));
    }));
    if(best>=75){gate.quizPassed=true;gate.quizScore=best;save()}
  }
  function activeSection(d){
    required.forEach(s=>{
      const el=d.getElementById('sec-'+s);
      if(!el)return;
      const cs=getComputedStyle(el);
      if(el.classList.contains('active')||(cs.display!=='none'&&cs.visibility!=='hidden'))mark(s);
    });
  }
  function sectionFromTarget(t){
    const holder=t.closest('[data-sec],[data-s],[data-section]');
    if(holder)return holder.dataset.sec||holder.dataset.s||holder.dataset.section||'';
    const oc=t.getAttribute?.('onclick')||'';
    const m=oc.match(/(?:NAV\.)?(?:go|goto)\(\s*['"]([^'"]+)['"]/);
    return m?m[1]:'';
  }
  function completionTarget(t){
    const oc=t.getAttribute?.('onclick')||'',txt=(t.textContent||'').trim();
    return /(?:finishModule|PROG\.finish|PROG\.goNext|goNextModule)\s*\(/.test(oc) ||
      new RegExp('(?:Terminer|Marquer)[^\\n]{0,40}'+esc(cfg.module),'i').test(txt);
  }
  function wantsNext(t){
    const oc=t.getAttribute?.('onclick')||'',txt=(t.textContent||'').trim();
    return /(?:goNextModule|PROG\.goNext)\s*\(/.test(oc)||/^Continuer\b/i.test(txt)||/Module suivant/i.test(txt);
  }
  function gateStatus(){
    inferStorage();
    const d=frame.contentDocument;if(d){activeSection(d);scoreFromDom(d)}
    const missing=required.filter(s=>!gate.visited[s]);
    return {ok:missing.length===0&&gate.quizPassed,missing};
  }
  function toast(d,msg,ok){
    let x=d.getElementById('course-gate-toast');
    if(!x){x=d.createElement('div');x.id='course-gate-toast';x.style.cssText='position:fixed;right:16px;bottom:16px;z-index:99999;max-width:520px;padding:13px 16px;border-radius:9px;font:13px/1.5 system-ui,sans-serif;box-shadow:0 8px 28px #0003';d.body.appendChild(x)}
    x.style.background=ok?'#E7F5EC':'#FEF3D8';x.style.color=ok?'#1f5d3b':'#684600';x.style.border='1px solid '+(ok?'#8DC7A2':'#dfbf70');x.textContent=msg;
    clearTimeout(x._t);x._t=setTimeout(()=>x.remove(),7000);
  }
  function finalize(d,next){
    gate.done=true;save();
    try{const x=JSON.parse(localStorage.getItem(DASH)||'{}');x[cfg.module]='done';localStorage.setItem(DASH,JSON.stringify(x))}catch(e){}
    toast(d,cfg.module+' validé : toutes les sections ont été parcourues et le QCM a atteint au moins 75 %.',true);
    if(next&&cfg.next)setTimeout(()=>{window.top.location.href=cfg.next},250);
  }
  function applyTextReplacements(d,repls){
    const walker=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT);
    let n;while((n=walker.nextNode())){
      let v=n.nodeValue||'',nv=v;
      repls.forEach(([a,b])=>{if(nv.includes(a))nv=nv.split(a).join(b)});
      if(nv!==v)n.nodeValue=nv;
    }
  }
  function legalPatch(d){
    if(cfg.module==='M01'){
      d.querySelectorAll('.vocab-card').forEach(c=>{
        const k=c.querySelector('.vfr')?.textContent.trim(),def=c.querySelector('.vdef');
        if(!def)return;
        if(k==='TVA / Taxe sur la valeur ajoutée')def.textContent='Impôt fédéral général sur la consommation. Le système vise la neutralité pour l’entreprise dans la mesure où elle dispose effectivement du droit à la déduction de l’impôt préalable.';
        if(k==='Impôt préalable (DIP)')def.textContent='TVA grevant certaines acquisitions, déductible dans la mesure où les conditions des art. 28 ss LTVA sont remplies et selon l’affectation.';
        if(k==='Opération exclue')def.textContent='Prestation exclue de l’impôt selon l’art. 21 LTVA. À distinguer d’une prestation localisée hors de Suisse. Sans option ou droit spécial, pas de TVA de sortie et pas de DIP sur les coûts directement affectés.';
        if(k==='Décompte TVA')def.textContent='Déclaration TVA selon la période de décompte applicable : en principe trimestrielle (effective/TaF) ou semestrielle (TDFN), avec décompte annuel possible sur demande sous les conditions de l’art. 35a LTVA.';
        if(k==='Méthode effective')def.textContent='TVA due réelle moins DIP déductible réel. Période de décompte en principe trimestrielle; décompte annuel possible sur demande si les conditions légales sont réunies.';
        if(k==='TDFN / Taux de la dette fiscale nette')def.textContent='Méthode simplifiée : TDFN appliqué au chiffre d’affaires déterminant TVA comprise, sous les limites actuelles. Décompte en principe semestriel; décompte annuel possible sur demande sous conditions.';
      });
      applyTextReplacements(d,[
        ['Les opérations exclues sont hors champ.','Les prestations exclues selon l’art. 21 ne sont pas comprises dans le chiffre d’affaires déterminant de l’art. 10; elles ne doivent pas être confondues avec des prestations localisées hors de Suisse.'],
        ['Hors champ/exclu =','Prestation exclue art. 21 ='],
        ['Taux normal 2024','Taux normal actuel (depuis 01.01.2024)'],
        ['Taux réduit 2024','Taux réduit actuel (depuis 01.01.2024)'],
        ['Taux hébergement 2024','Taux hébergement actuel (depuis 01.01.2024)']
      ]);
    }
    if(cfg.module==='M03'){
      applyTextReplacements(d,[
        ['Engagement minimum 1 an','Changement de méthode : possible après une période fiscale complète, sous réserve des délais et conditions applicables'],
        ["Dépassement de seuil = passage à effective dès l'exercice suivant + notification 30 jours + correction d'entrée stocks (art. 32).",'Dépassement des limites : appliquer les règles actuelles de sortie de la méthode TDFN. Depuis 2025, tout changement de méthode exige aussi d’analyser les corrections sur la valeur résiduelle des biens et prestations.']
      ]);
    }
    if(cfg.module==='M08'){
      d.querySelectorAll('.vocab-card').forEach(c=>{
        const k=c.querySelector('.vfr')?.textContent.trim(),def=c.querySelector('.vdef'),art=c.querySelector('.vart');if(!def)return;
        if(k==="Option d'imposition immobilière"||k==='Option d’imposition immobilière'){def.textContent='Droit de soumettre volontairement une opération immobilière exclue à la TVA lorsque l’art. 22 le permet. Vérifier l’usage du bien, les exclusions à l’option et la modalité/timing d’exercice; il n’existe pas une irrévocabilité générale pour toute la durée du contrat.';if(art)art.textContent='art. 22 LTVA · art. 39 OTVA · pratique AFC Immobilier'}
        if(k==='Immeuble mixte'){def.textContent='Immeuble affecté à des usages donnant et ne donnant pas droit au DIP. Procéder d’abord à l’affectation directe des coûts, puis appliquer une clé objective uniquement aux vrais coûts communs.';if(art)art.textContent='art. 30 LTVA · pratique AFC'}
        if(k==='Clé de répartition DIP'){def.textContent='Méthode objective pour les coûts réellement communs après affectation directe. La clé doit refléter l’utilisation effective; surface, recettes ou autre critère ne sont pas des clés légales universelles.';if(art)art.textContent='art. 30 LTVA · méthode objective documentée'}
        if(k==="Changement d'affectation"){def.textContent='Passage d’un usage donnant droit au DIP à un usage n’y donnant plus droit, ou inversement. Analyser correction/dégrèvement sur la valeur résiduelle; pour l’immobilier, la dépréciation forfaitaire est de 5 % par année (logique 1/20) selon les conditions légales.';if(art)art.textContent='art. 31–32 LTVA · art. 70–73 OTVA'}
        if(k==="Imposition à l'acquisition (travaux)"){def.textContent='Pour un entrepreneur étranger intervenant sur un immeuble suisse, qualifier d’abord le flux et le lieu, puis vérifier son éventuelle obligation d’inscription en Suisse, l’importateur et la TVA à l’importation. L’impôt sur les acquisitions n’intervient que si les conditions de l’art. 45 sont remplies.';if(art)art.textContent='art. 8 · 10 · 45 · 50 ss LTVA'}
      });
    }
  }
  function attach(){
    const d=frame.contentDocument;if(!d)return;
    inferStorage();activeSection(d);legalPatch(d);
    d.querySelectorAll('a[href]').forEach(a=>{
      const h=a.getAttribute('href')||'';
      if(h&&!h.startsWith('#')&&!/^https?:/i.test(h)&&!h.startsWith('javascript:')&&!h.startsWith('mailto:')&&!h.startsWith('tel:'))a.target='_top';
    });
    d.addEventListener('click',e=>{
      const t=e.target.closest('button,a');if(!t)return;
      const s=sectionFromTarget(t);if(s)mark(s);
      if(completionTarget(t)){
        e.preventDefault();e.stopImmediatePropagation();
        setTimeout(()=>{
          legalPatch(d);scoreFromDom(d);
          const st=gateStatus();
          if(!st.ok){toast(d,'Validation refusée : '+(st.missing.length?'sections à parcourir : '+st.missing.join(', ')+'. ':'')+(!gate.quizPassed?'QCM ≥ 75 % requis.':''),false);return}
          finalize(d,wantsNext(t));
        },0);
      }else setTimeout(()=>{activeSection(d);scoreFromDom(d);legalPatch(d)},0);
    },true);
    d.addEventListener('change',e=>{const v=e.target?.value;if(required.includes(v))mark(v);setTimeout(()=>activeSection(d),0)},true);
    const mo=new MutationObserver(()=>{clearTimeout(mo._t);mo._t=setTimeout(()=>{activeSection(d);scoreFromDom(d);legalPatch(d)},80)});
    mo.observe(d.body,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['class','style']});
  }
  frame.addEventListener('load',attach);
  frame.src=cfg.src;
})();