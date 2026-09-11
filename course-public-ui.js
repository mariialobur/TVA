'use strict';
(()=>{
  const HOME='index.html';
  const TIME_RE=/(?:[~≈]\s*)?\d+(?:[.,]\d+)?\s*(?:[-–—]\s*\d+(?:[.,]\d+)?)?\s*(?:h(?:eures?)?|heures?|min(?:utes?)?)(?:\s*\d+\s*min)?/i;

  function addHomeButton(doc,targetTop=true){
    if(!doc||!doc.body||doc.getElementById('course-home-fixed'))return;
    const a=doc.createElement('a');
    a.id='course-home-fixed';
    a.href=HOME;
    if(targetTop)a.target='_top';
    a.textContent='⌂ Accueil du parcours';
    a.setAttribute('aria-label','Retour à la page principale de la formation');
    a.style.cssText='position:fixed;right:18px;bottom:18px;z-index:2147483000;display:inline-flex;align-items:center;gap:7px;padding:10px 14px;border-radius:999px;background:#0B2545;color:#fff;border:1px solid #C9A84C;text-decoration:none;font:700 12px/1.2 system-ui,-apple-system,Segoe UI,sans-serif;box-shadow:0 8px 24px rgba(11,37,69,.24)';
    doc.body.appendChild(a);
  }

  function removeEstimatedDurations(doc){
    if(!doc||!doc.body)return;
    doc.querySelectorAll('.tb-time,.hours-badge,.duration-badge,.time-badge,.module-duration').forEach(el=>el.remove());
    doc.querySelectorAll('.chip,.meta-chip,.hero-chip').forEach(el=>{
      const t=(el.textContent||'').trim();
      if((/[⏱🕐]/.test(t)||/[~≈]/.test(t))&&TIME_RE.test(t))el.remove();
    });
    doc.querySelectorAll('.sb-sub,.sidebar-sub').forEach(el=>{
      let t=(el.textContent||'').trim();
      if(!TIME_RE.test(t))return;
      t=t.replace(TIME_RE,'').replace(/^\s*[·•|—–-]+\s*/,'').replace(/\s*[·•|—–-]+\s*$/,'').trim();
      if(t)el.textContent=t;else el.remove();
    });
    doc.querySelectorAll('.box-title,h3,h4').forEach(title=>{
      if(!/durée\s+(?:réaliste|estimée)|temps\s+estimé/i.test(title.textContent||''))return;
      const holder=title.closest('.box,.card,.theory-block,.block');
      if(holder)holder.remove();
    });
  }

  function removeDeveloperLinks(doc){
    if(!doc)return;
    doc.querySelectorAll('a[href]').forEach(a=>{
      const href=(a.getAttribute('href')||'').trim();
      const text=(a.textContent||'').trim();
      if(/github\.com/i.test(href)||/^github\b/i.test(text))a.remove();
    });
  }

  function normalizeHomeLinks(doc){
    if(!doc)return;
    doc.querySelectorAll('a[href="index.html"],a.home,a.btn-home').forEach(a=>{
      const txt=(a.textContent||'').trim();
      if(/retour|tableau de bord|accueil|cours/i.test(txt)){
        a.textContent='← Accueil du parcours';
        a.target='_top';
        a.setAttribute('aria-label','Retour à la page principale de la formation');
      }
    });
  }

  function clean(doc,addFloating){
    if(!doc||!doc.body)return;
    removeEstimatedDurations(doc);
    removeDeveloperLinks(doc);
    normalizeHomeLinks(doc);
    if(addFloating)addHomeButton(doc,true);
  }

  function init(){
    const frame=document.getElementById('module');
    if(frame){
      addHomeButton(document,false);
      const apply=()=>{try{clean(frame.contentDocument,false)}catch(e){}};
      frame.addEventListener('load',apply);
      apply();
      return;
    }
    clean(document,true);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
