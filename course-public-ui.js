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

  function normalizeLegacySections(doc){
    if(!doc?.body)return;
    const content=doc.querySelector('.content');
    const sections=[...doc.querySelectorAll('.section[id^="sec-"]')];
    if(!content||sections.length<2)return;

    for(let pass=0;pass<4;pass++){
      let moved=false;
      [...sections].reverse().forEach(sec=>{
        const parentSection=sec.parentElement?.closest?.('.section[id^="sec-"]');
        if(parentSection&&parentSection!==sec){
          parentSection.parentNode.insertBefore(sec,parentSection.nextSibling);
          moved=true;
        }
      });
      if(!moved)break;
    }

    const force=id=>{
      const target=doc.getElementById('sec-'+id);
      if(!target)return;
      sections.forEach(sec=>{
        const on=sec===target;
        sec.classList.toggle('active',on);
        sec.style.display=on?'block':'none';
      });
    };

    const activeNav=doc.querySelector('.nav-item.active[data-section]');
    const activeSection=doc.querySelector('.section.active[id^="sec-"]');
    const initial=activeNav?.dataset.section || activeSection?.id?.replace(/^sec-/,'');
    if(initial)force(initial);

    if(!doc.documentElement.dataset.courseSectionGuard){
      doc.documentElement.dataset.courseSectionGuard='1';
      doc.addEventListener('click',e=>{
        const nav=e.target.closest?.('.nav-item[data-section]');
        if(!nav)return;
        const id=nav.dataset.section;
        setTimeout(()=>force(id),0);
        setTimeout(()=>force(id),80);
      },true);
    }
  }

  function clean(doc,addFloating){
    if(!doc||!doc.body)return;
    normalizeLegacySections(doc);
    removeEstimatedDurations(doc);
    removeDeveloperLinks(doc);
    normalizeHomeLinks(doc);
    if(addFloating)addHomeButton(doc,true);
  }

  function init(){
    const frame=document.getElementById('module');
    if(frame){
      addHomeButton(document,false);
      const apply=()=>{try{clean(frame.contentDocument,false)}catch(e){console.warn('course-public-ui',e)}};
      frame.addEventListener('load',apply);
      apply();
      return;
    }
    clean(document,true);
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});
  else init();
})();
