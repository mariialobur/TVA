'use strict';
(()=>{
  const cfg=window.COURSE_GATE_CONFIG||{},frame=document.getElementById('module');
  if(!frame||!cfg.module)return;
  const setText=(el,text)=>{if(el&&el.textContent.trim()!==text.trim())el.textContent=text};
  function replaceText(d,pairs){
    const w=d.createTreeWalker(d.body,NodeFilter.SHOW_TEXT);let n;
    while((n=w.nextNode())){let v=n.nodeValue||'',x=v;for(const [a,b] of pairs)if(x.includes(a))x=x.split(a).join(b);if(x!==v)n.nodeValue=x}
  }
  function portalLinks(d){
    d.querySelectorAll('a[href*="eportal.admin.ch"]').forEach(a=>{a.href='https://www.estv.admin.ch/fr/services-en-ligne-afc';if(/ePortal/i.test(a.textContent||''))a.textContent='Portail AFC ↗'});
  }
  function patchM01(d){
    d.querySelectorAll('.vocab-card').forEach(c=>{const k=c.querySelector('.vfr')?.textContent.trim(),def=c.querySelector('.vdef');if(k==='Décompte TVA'&&def)setText(def,'Déclaration TVA selon la période applicable. Depuis le 11.05.2026, la remise se fait dans Décompte TVA pro sur le Portail AFC; le délai ordinaire de remise et paiement reste de 60 jours après la fin de la période de décompte.')});
    replaceText(d,[['Via ePortal dans les 60 jours','Via Décompte TVA pro sur le Portail AFC, dans le délai applicable'],['via ePortal AFC','via le Portail AFC'],['Via ePortal AFC','Via le Portail AFC'],['Via ePortal','Via le Portail AFC'],['formulaires, ePortal et jurisprudence','formulaires, Portail AFC / Décompte TVA pro et jurisprudence']]);portalLinks(d);
  }
  function patchM03(d){
    replaceText(d,[
      ['ePortal AFC obligatoire dès 2025 (art. 71a LTVA)','Procédure électronique obligatoire dès 2025 — Décompte TVA pro sur le Portail AFC'],
      ['Depuis le 1er janvier 2025, le dépôt du décompte TVA par voie électronique via ePortal AFC (eportal.admin.ch) est obligatoire en principe.','Depuis le 1er janvier 2025, la procédure électronique est obligatoire en principe. Depuis le 11 mai 2026, les décomptes sont remis dans Décompte TVA pro sur le Portail AFC; Décompte TVA easy a été supprimé.'],
      ['Depuis le 1er janvier 2025, dépôt obligatoire via ePortal AFC (eportal.admin.ch).','Depuis le 1er janvier 2025, dépôt électronique obligatoire; depuis le 11 mai 2026, utilisation de Décompte TVA pro sur le Portail AFC.'],
      ["L'assujetti doit, dans les 240 jours suivant la fin de l'exercice commercial, corriger les inexactitudes constatées dans la concordance des décomptes périodiques avec la comptabilité annuelle.","L’art. 72 LTVA impose la correction au plus tard dans la période de décompte au cours de laquelle tombe le 180e jour suivant la fin de l’exercice. Le repère de 240 jours est une présomption pratique de l’AFC pour la finalisation de la concordance, et non le délai légal formulé par l’art. 72."],
      ['ePortal AFC','Portail AFC / Décompte TVA pro'],['ePortal','Portail AFC']
    ]);portalLinks(d);
  }
  function patchM04(d){replaceText(d,[['AFC ePortal','AFC via Portail AFC / Décompte TVA pro'],['Décompte TVA pro ou ePortal','Décompte TVA pro sur le Portail AFC'],['via export AFC ePortal','via export Décompte TVA pro / Portail AFC']]);portalLinks(d)}
  function patchM06(d){
    replaceText(d,[['publiés sur ePortal AFC','publiés par l’AFC'],['publié sur ePortal AFC','publié par l’AFC'],['formulaire en ligne sur ePortal AFC','inscription en ligne via le Portail AFC'],['Inscription dans 30 jours après dépassement du seuil.','S’annoncer dans les 30 jours dès le début de l’assujettissement; déterminer d’abord cette date selon l’art. 14 et les faits.'],['— annule l’amende','— effet pénal favorable uniquement si toutes les conditions de l’art. 102 sont remplies'],["— annule l'amende","— effet pénal favorable uniquement si toutes les conditions de l’art. 102 sont remplies"]]);
    const s1=d.getElementById('m6c11s1'),block=s1?.closest('.case-block');
    if(block){const sc=block.querySelector('.case-scenario');if(sc&&!sc.dataset.currentLaw){sc.innerHTML='<strong>Contexte :</strong> StartupTech SA (Lausanne) démarre son activité en 2026. Au lancement, son business plan, ses contrats déjà signés et son pipeline rendent objectivement prévisible, pour les douze mois suivants, un chiffre d’affaires mondial déterminant de <strong>CHF 180\'000</strong> provenant de prestations non exclues : CHF 65\'000 de prestations à des clients suisses, CHF 80\'000 de services B2B à des clients UE/US et CHF 35\'000 à des clients asiatiques. La direction pense à tort que seul le CA suisse compte pour le seuil.';sc.dataset.currentLaw='1'}
      const opts=s1.querySelectorAll('.step-opt');if(opts[1])setText(opts[1],"B) Oui dès le début de l’activité : les circonstances rendent prévisible un CA mondial déterminant > CHF 100'000 sur les 12 mois suivants");
      const ex=d.getElementById('m6c11s1-expl');if(ex&&!ex.dataset.currentLaw){ex.innerHTML='<strong>Deux questions distinctes :</strong> (1) pour le seuil de CHF 100\'000, on retient le chiffre d’affaires mondial provenant de prestations qui ne sont pas exclues de l’impôt; des services localisés à l’étranger selon l’art. 8 peuvent donc compter. (2) il faut ensuite déterminer <strong>quand</strong> l’assujettissement commence. Pour une entreprise suisse qui débute son activité, il commence dès le début si les circonstances permettent de prévoir que le seuil sera atteint dans les douze mois suivants. Pour une entreprise suisse déjà existante et jusque-là libérée, le simple franchissement en cours d’exercice ne signifie pas automatiquement assujettissement rétroactif au 1er janvier; en principe, l’assujettissement commence à l’expiration de l’exercice au cours duquel le seuil a été atteint, sous réserve des règles applicables aux faits.<div class="art-ref">📋 art. 10 et 14 LTVA · pratique AFC Assujettissement</div>';ex.dataset.currentLaw='1'}}
    const s3=d.getElementById('m6c11s3');if(s3){const opts=s3.querySelectorAll('.step-opt');if(opts[1])setText(opts[1],'B) S’annoncer dans les 30 jours dès le début de l’assujettissement; déterminer d’abord cette date selon l’art. 14 et les faits');const ex=d.getElementById('m6c11s3-expl');if(ex&&!ex.dataset.currentLaw){ex.innerHTML='<strong>Art. 66 LTVA :</strong> l’annonce doit intervenir dans les <strong>30 jours dès le début de l’assujettissement</strong>. Il ne faut donc pas mémoriser «30 jours après le dépassement du seuil». Dans ce cas précis, le seuil était suffisamment prévisible au démarrage: le début de l’assujettissement coïncide avec le début de l’activité. Pour une entreprise déjà existante et auparavant libérée, la date peut être différente et doit être déterminée avant de compter les 30 jours. Un retard peut entraîner rappel et intérêts; une conséquence pénale dépend des faits et de la faute. Une dénonciation spontanée ne supprime pas automatiquement une amende: l’effet favorable suppose que toutes les conditions de l’art. 102 soient remplies, tandis que l’impôt et les intérêts restent en principe dus.<div class="art-ref">📋 art. 14 · 66 · 87 · 96 · 102 LTVA</div>';ex.dataset.currentLaw='1'}}
    portalLinks(d);
  }
  function apply(){const d=frame.contentDocument;if(!d?.body)return;if(cfg.module==='M01')patchM01(d);if(cfg.module==='M03')patchM03(d);if(cfg.module==='M04')patchM04(d);if(cfg.module==='M06')patchM06(d)}
  frame.addEventListener('load',()=>{apply();const d=frame.contentDocument;if(!d?.body)return;const mo=new MutationObserver(()=>{clearTimeout(mo._t);mo._t=setTimeout(apply,90)});mo.observe(d.body,{subtree:true,childList:true,characterData:true})});
})();
