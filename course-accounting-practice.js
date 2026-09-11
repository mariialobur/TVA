'use strict';
(()=>{
  const cfg=window.COURSE_GATE_CONFIG||{},f=document.getElementById('module');
  if(!f||!cfg.module)return;

  function note(d){
    if(d.getElementById('course-accounting-note'))return;
    const heads=[...d.querySelectorAll('h2,h3,h4')];
    const h=heads.find(x=>/Plan comptable suisse PME|Comptes TVA essentiels/i.test(x.textContent||''));
    if(!h)return;
    const box=d.createElement('div');box.id='course-accounting-note';box.className='box info';
    box.innerHTML='<div class="box-icon">ℹ️</div><div class="box-body"><div class="box-title">Lecture fiduciaire</div><p>Les numéros de comptes présentés dans ce module sont des <strong>exemples pédagogiques inspirés d’un plan comptable PME</strong>. Ils ne constituent pas des numéros imposés par la LTVA. En pratique, reprendre le plan de comptes, les codes TVA et la logique de l’ERP du mandat, puis réconcilier ces paramètres avec le décompte AFC.</p></div>';
    const holder=h.closest('.theory-block,.block')||h.parentElement;
    if(holder&&holder.parentNode)holder.parentNode.insertBefore(box,holder.nextSibling);
  }

  function patchM05(d){
    const ex=d.getElementById('m5c1s2-expl');
    if(ex&&!ex.dataset.accountingAccuracy){
      ex.innerHTML='Dans le <strong>plan comptable utilisé pour cet exercice</strong>, l’écriture illustrée est : Débit 6500 Loyer atelier CHF 18\'000 + Débit 1170 TVA déductible CHF 1\'458 / Crédit 2000 Créanciers CHF 19\'458. <strong>Ces numéros de comptes ne sont pas imposés par la LTVA</strong> et peuvent différer selon le mandat ou l’ERP. Le montant porté en charge dépend aussi du droit au DIP : si la TVA n’est pas entièrement déductible, la part non déductible doit être comptabilisée selon le traitement applicable au coût/actif. Le réflexe à retenir est donc : qualifier la dépense → vérifier le droit au DIP → appliquer les comptes et codes TVA du mandat.<div class="art-ref">📋 art. 28–30 LTVA · écriture comptable illustrative</div>';
      ex.dataset.accountingAccuracy='1';
    }
  }

  function apply(){
    const d=f.contentDocument;if(!d?.body)return;
    if(cfg.module==='M04'||cfg.module==='M05')note(d);
    if(cfg.module==='M05')patchM05(d);
  }
  f.addEventListener('load',apply);
  try{apply()}catch(e){}
})();
