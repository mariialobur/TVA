'use strict';
(()=>{
  const f=document.getElementById('module');if(!f)return;
  const repl=[
    ['Faux. 5 ans est le délai relatif; actes interruptifs, nouveau délai de 2 ans et plafond absolu de 10 ans doivent être distingués.','Faux. 5 ans est le délai relatif. Si l’interruption vient de l’assujetti, un nouveau délai de 5 ans recommence à courir; si elle vient de l’AFC ou d’une instance de recours, le nouveau délai est de 2 ans. Le délai absolu reste 10 ans.'],
    ['5 ans relatif; annonce contrôle interrompt; nouveau délai 2 ans après interruption AFC/recours; 10 ans absolu.','5 ans relatif; interruption par l’assujetti → nouveau délai 5 ans; interruption par l’AFC/recours → nouveau délai 2 ans; 10 ans absolu.'],
    ['Red-team Legal QA · 09.09.2026','Red-team Legal QA · 11.09.2026'],
    ['Audit juridique : 09.09.2026','Audit juridique : 11.09.2026']
  ];
  function patchText(d){const w=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT);let n;while((n=w.nextNode())){let v=n.nodeValue||'',nv=v;for(const [a,b] of repl)if(nv.includes(a))nv=nv.split(a).join(b);if(nv!==v)n.nodeValue=nv}}
  function addPrescriptionRow(d){
    if(d.getElementById('m11-assujetti-interruption-row'))return;
    const rows=[...d.querySelectorAll('#sec-theory table tbody tr')];
    const target=rows.find(r=>r.cells?.[0]?.textContent.includes('Après interruption par AFC/instance de recours'));
    if(!target)return;
    const tr=d.createElement('tr');tr.id='m11-assujetti-interruption-row';tr.innerHTML='<td>Après interruption par l’assujetti</td><td>Nouveau délai de 5 ans (art. 42 al. 2).</td>';target.parentNode.insertBefore(tr,target);
  }
  function patch(){const d=f.contentDocument;if(!d?.body)return;patchText(d);addPrescriptionRow(d);d.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href')||'';if(h&&!h.startsWith('#')&&!/^https?:/i.test(h)&&!h.startsWith('javascript:')&&!h.startsWith('mailto:')&&!h.startsWith('tel:'))a.target='_top'});const mo=new MutationObserver(()=>{clearTimeout(mo._t);mo._t=setTimeout(()=>{patchText(d);addPrescriptionRow(d)},0)});mo.observe(d.body,{subtree:true,childList:true,characterData:true});document.documentElement.dataset.m11CurrentLawReady='1'}
  f.addEventListener('load',patch);f.src=window.M11_CORE||'m11-controle-afc-tva-core.html';
  window.finishModule=()=>new Promise((resolve,reject)=>{let n=0;const t=setInterval(()=>{n++;try{const fn=f.contentWindow?.finishModule;if(typeof fn==='function'){clearInterval(t);fn.call(f.contentWindow);resolve();return}}catch(e){}if(n>200){clearInterval(t);reject(new Error('M11 core finishModule unavailable'))}},10)});
})();
