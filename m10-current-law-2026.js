'use strict';
(()=>{
  const f=document.getElementById('module');if(!f)return;
  const repl=[
    ['L’OFDF ne perçoit pas les montants d’impôt à l’importation inférieurs à CHF 5.','L’OFDF ne perçoit pas les montants d’impôt à l’importation n’excédant pas CHF 5.'],
    ['(< CHF 5)','(≤ CHF 5)'],
    ['pour un impôt inférieur à CHF 5','pour un impôt n’excédant pas CHF 5'],
    ['actuellement <5 CHF','actuellement ≤5 CHF'],
    ['< CHF 5 d’impôt import','≤ CHF 5 d’impôt import'],
    ['Impôt import < CHF5','Impôt import ≤ CHF5']
  ];
  function patchText(d){
    const w=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT);let n;
    while((n=w.nextNode())){let v=n.nodeValue||'',nv=v;for(const [a,b] of repl)if(nv.includes(a))nv=nv.split(a).join(b);if(nv!==v)n.nodeValue=nv}
  }
  function patch(){
    const d=f.contentDocument;if(!d?.body)return;
    patchText(d);
    d.querySelectorAll('a[href]').forEach(a=>{const h=a.getAttribute('href')||'';if(h&&!h.startsWith('#')&&!/^https?:/i.test(h)&&!h.startsWith('javascript:')&&!h.startsWith('mailto:')&&!h.startsWith('tel:'))a.target='_top'});
    const mo=new MutationObserver(()=>{clearTimeout(mo._t);mo._t=setTimeout(()=>patchText(d),0)});mo.observe(d.body,{subtree:true,childList:true,characterData:true});
    document.documentElement.dataset.m10CurrentLawReady='1';
  }
  f.addEventListener('load',patch);
  f.src=window.M10_CORE||'m10-digital-plateformes-ecommerce-core.html';
  window.finishModule=()=>new Promise((resolve,reject)=>{let n=0;const t=setInterval(()=>{n++;try{const fn=f.contentWindow?.finishModule;if(typeof fn==='function'){clearInterval(t);fn.call(f.contentWindow);resolve();return}}catch(e){}if(n>200){clearInterval(t);reject(new Error('M10 core finishModule unavailable'))}},10)});
})();
