'use strict';
(()=>{
  const PAIRS=[
    ['Red-team Legal QA · 09.09.2026','Droit vérifié au 09.09.2026'],
    ['Red-team Legal QA · 11.09.2026','Droit vérifié au 11.09.2026'],
    ['Legal QA · version 09.09.2026','Droit vérifié au 09.09.2026'],
    ['M10 · Legal QA 09.09.2026','M10 · Repères juridiques au 09.09.2026'],
    ['M11 · Red-team Legal QA · 09.09.2026','M11 · Repères juridiques au 09.09.2026'],
    ['M11 · Red-team Legal QA · 11.09.2026','M11 · Repères juridiques au 11.09.2026'],
    ['Audit juridique : 09.09.2026','Droit vérifié : 09.09.2026'],
    ['Audit juridique : 11.09.2026','Droit vérifié : 11.09.2026'],
    ['Théorie & truth map','Théorie & méthode'],
    ['Truth map M10 — ordre de travail','Méthode de raisonnement — ordre de travail'],
    ['Truth map M11 — ordre professionnel','Méthode de travail — ordre professionnel'],
    ['Anti-erreurs · 14','Erreurs fréquentes · 14'],
    ['Cheatsheet & validation','Synthèse & validation'],
    ['Cheatsheet','Synthèse'],
    ['issue list','tableau de suivi'],
    ['Issue list','Tableau de suivi']
  ];
  function cleanDoc(d){
    if(!d?.body)return;
    const walk=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT);let n;
    while((n=walk.nextNode())){
      const p=n.parentElement;if(!p||/^(SCRIPT|STYLE|NOSCRIPT)$/i.test(p.tagName))continue;
      let v=n.nodeValue||'',x=v;
      for(const [a,b] of PAIRS)if(x.includes(a))x=x.split(a).join(b);
      if(x!==v)n.nodeValue=x;
    }
    d.querySelectorAll('a.home').forEach(a=>{if(/Tableau de bord/i.test(a.textContent||''))a.textContent='← Accueil du parcours'});
  }
  function install(){
    cleanDoc(document);
    const frame=document.getElementById('module');
    if(!frame)return;
    const apply=()=>{try{cleanDoc(frame.contentDocument)}catch(e){}};
    frame.addEventListener('load',()=>setTimeout(apply,0));
    setTimeout(apply,200);
    setTimeout(apply,800);
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',install);else install();
})();