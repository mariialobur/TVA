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
  function patchM02(d){
    replaceText(d,[["Hiérarchie : Loi (LTVA) > Ordonnance (OTVA) > Jurisprudence TF/TAF > Doctrine AFC. Lors d'un litige, invoquer la jurisprudence prévaut sur la doctrine AFC.","Méthode des sources : partir de la LTVA et de l’OTVA applicables, puis vérifier la jurisprudence pertinente qui interprète ces normes. La pratique publiée de l’AFC est essentielle pour comprendre l’application administrative, mais elle n’est pas une source législative et ne lie pas les tribunaux comme une loi. En cas de litige, ne pas réciter une hiérarchie mécanique : confronter texte légal, ordonnance, jurisprudence et pratique AFC aux faits du dossier."]]);
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

    const us1=d.getElementById('m6c1s3');
    if(us1&&!us1.dataset.currentLaw){
      const q=us1.querySelector('.step-question');if(q)q.innerHTML='<span class="step-q-num">Q3</span>Et les taxes à l’arrivée aux États-Unis ?';
      const o=us1.querySelectorAll('.step-opt');
      if(o[0])setText(o[0],'A) La LTVA impose à Watch Manufacture de collecter automatiquement la sales tax US');
      if(o[1])setText(o[1],'B) La TVA suisse ne tranche pas les obligations US : vérifier séparément droits de douane, sales tax, rôle de l’importateur et Incoterms selon le droit local');
      if(o[2])setText(o[2],'C) Une exportation TVA suisse signifie qu’aucune taxe étrangère ne peut exister');
      if(o[3])setText(o[3],'D) L’AFC rembourse les taxes américaines au client');
      const ex=d.getElementById('m6c1s3-expl');if(ex)ex.innerHTML='Le raisonnement TVA suisse s’arrête à la qualification et à la preuve de l’opération suisse. Les droits de douane et taxes de vente américaines dépendent du droit fédéral/étatique, du rôle contractuel des parties et des Incoterms. Il est donc incorrect d’enseigner qu’une sales tax est toujours «à la charge de l’importateur NY» ou qu’un taux d’État donné résout le cas. Pour un dossier réel, documenter l’exportation suisse puis faire vérifier séparément les obligations américaines.<div class="art-ref">📋 LTVA suisse : qualification export · fiscalité US : analyse locale séparée</div>';
      us1.dataset.currentLaw='1';
    }

    const us8=d.getElementById('m6c8s3');
    if(us8&&!us8.dataset.currentLaw){
      const q=us8.querySelector('.step-question');if(q)q.innerHTML='<span class="step-q-num">Q3</span>Que peut-on conclure pour les clients situés aux États-Unis ?';
      const o=us8.querySelectorAll('.step-opt');
      if(o[0])setText(o[0],'A) Aucune obligation fiscale étrangère n’est jamais possible');
      if(o[1])setText(o[1],'B) Le traitement TVA suisse ne suffit pas : les éventuelles obligations US doivent être analysées séparément selon les États, les faits et le modèle de vente');
      if(o[2])setText(o[2],'C) Une TVA fédérale américaine de 10 % s’applique automatiquement');
      if(o[3])setText(o[3],'D) La TVA suisse détermine elle-même la sales tax US');
      const ex=d.getElementById('m6c8s3-expl');if(ex)ex.innerHTML='Une opération peut être correctement traitée du point de vue de la TVA suisse tout en créant des obligations dans le pays du client. Le module ne doit pas transformer des règles étrangères variables en raccourci. Pour les États-Unis, vérifier séparément les obligations locales avec une source ou un conseil compétent; dans le dossier TVA suisse, conserver surtout les preuves permettant de localiser correctement la prestation.<div class="art-ref">📋 art. 8 LTVA · obligations étrangères à vérifier séparément</div>';
      us8.dataset.currentLaw='1';
    }

    const p1=d.getElementById('m6c10s1');
    if(p1&&!p1.dataset.currentLaw){
      const o=p1.querySelectorAll('.step-opt');if(o[1])setText(o[1],'B) SwissMarket SA — si les conditions de l’art. 20a sont remplies, la plateforme est réputée fournisseur de la livraison envers l’acheteur');
      const ex=d.getElementById('m6c10s1-expl');if(ex)ex.innerHTML='<strong>Art. 20a LTVA</strong> crée, pour la TVA, deux livraisons successives : vendeur sous-jacent → plateforme et plateforme → acheteur. La plateforme n’est toutefois réputée fournisseur que si les conditions de l’art. 20a sont remplies; il faut encore vérifier lieu de la livraison, assujettissement, importation, taux applicable et éventuelles exceptions. Le vendeur sous-jacent ne devient pas «invisible» : ses données et la première livraison restent pertinentes pour le traitement TVA et le contrôle. Ne pas attribuer à la réforme un montant de recettes fiscales non sourcé.<div class="art-ref">📋 art. 20a LTVA · Info TVA 27 Plateformes numériques</div>';
      p1.dataset.currentLaw='1';
    }

    const p2=d.getElementById('m6c10s2');
    if(p2&&!p2.dataset.currentLaw){
      const q=p2.querySelector('.step-question');if(q)q.innerHTML='<span class="step-q-num">Q2</span>Quel montant ne faut-il pas double compter dans ce scénario ?';
      const o=p2.querySelectorAll('.step-opt');
      if(o[0])setText(o[0],"A) CHF 1'275'000 seulement, car la plateforme ne déclare jamais les ventes facilitées");
      if(o[1])setText(o[1],"B) La commission de CHF 1'275'000 ne s’ajoute pas automatiquement une seconde fois aux CHF 8'500'000 de ventes réputées : dans le mécanisme art. 20a, elle représente en principe la marge économique de la plateforme");
      if(o[2])setText(o[2],"C) CHF 8'500'000 doivent être ignorés dans tous les cas");
      if(o[3])setText(o[3],'D) Aucun montant ne doit être documenté');
      const ex=d.getElementById('m6c10s2-expl');if(ex)ex.innerHTML='Dans le mécanisme de fournisseur réputé, la plateforme doit déclarer les transactions qui lui sont attribuées selon l’art. 20a. La <strong>commission retenue sur le prix n’est pas à additionner mécaniquement une deuxième fois</strong> comme une prestation imposable distincte : la pratique des plateformes la traite en principe comme la marge économique entre les deux livraisons fictives. Une prestation réellement distincte devrait être identifiée et qualifiée séparément. Le montant de TVA ne peut pas non plus être calculé avec un taux unique sans connaître la nature des biens et la base applicable.<div class="art-ref">📋 art. 20a · art. 24 LTVA · Info TVA 27</div>';
      p2.dataset.currentLaw='1';
    }

    const p3=d.getElementById('m6c10s3');
    if(p3&&!p3.dataset.currentLaw){
      const o=p3.querySelectorAll('.step-opt');if(o[1])setText(o[1],'B) Adapter facturation/ERP, cartographier vendeurs et flux, documenter les transactions art. 20a, coordonner importation et conserver les pièces selon les règles applicables');
      const ex=d.getElementById('m6c10s3-expl');if(ex)ex.innerHTML='Les enjeux opérationnels sont principalement fiscaux et documentaires :<br>(1) paramétrer facturation et taux selon les biens ;<br>(2) distinguer ventes propres et ventes facilitées, vendeurs et destinations ;<br>(3) pouvoir produire un état des transactions attribuées à la plateforme et le réconcilier avec les décomptes vendeurs ;<br>(4) coordonner UID TVA, importateur, déclaration douanière et impôt à l’importation ;<br>(5) conserver les pièces conformément aux règles de l’art. 70 LTVA.<br><strong>À ne pas déduire de l’art. 20a :</strong> la fiction TVA ne transforme pas à elle seule la plateforme en interlocuteur civil obligatoire pour garanties/retours, et aucun «coût typique de compliance» de CHF 100k–500k ne doit être enseigné sans source et sans faits.<div class="art-ref">📋 art. 20a · 70 LTVA · Info TVA 27</div>';
      p3.dataset.currentLaw='1';
    }

    const s1=d.getElementById('m6c11s1'),block=s1?.closest('.case-block');
    if(block){const sc=block.querySelector('.case-scenario');if(sc&&!sc.dataset.currentLaw){sc.innerHTML='<strong>Contexte :</strong> StartupTech SA (Lausanne) démarre son activité en 2026. Au lancement, son business plan, ses contrats déjà signés et son pipeline rendent objectivement prévisible, pour les douze mois suivants, un chiffre d’affaires mondial déterminant de <strong>CHF 180\'000</strong> provenant de prestations non exclues : CHF 65\'000 de prestations à des clients suisses, CHF 80\'000 de services B2B à des clients UE/US et CHF 35\'000 à des clients asiatiques. La direction pense à tort que seul le CA suisse compte pour le seuil.';sc.dataset.currentLaw='1'}
      const opts=s1.querySelectorAll('.step-opt');if(opts[1])setText(opts[1],"B) Oui dès le début de l’activité : les circonstances rendent prévisible un CA mondial déterminant > CHF 100'000 sur les 12 mois suivants");
      const ex=d.getElementById('m6c11s1-expl');if(ex&&!ex.dataset.currentLaw){ex.innerHTML='<strong>Deux questions distinctes :</strong> (1) pour le seuil de CHF 100\'000, on retient le chiffre d’affaires mondial provenant de prestations qui ne sont pas exclues de l’impôt; des services localisés à l’étranger selon l’art. 8 peuvent donc compter. (2) il faut ensuite déterminer <strong>quand</strong> l’assujettissement commence. Pour une entreprise suisse qui débute son activité, il commence dès le début si les circonstances permettent de prévoir que le seuil sera atteint dans les douze mois suivants. Pour une entreprise suisse déjà existante et jusque-là libérée, l’assujettissement obligatoire commence à l’expiration de l’exercice au cours duquel le seuil a été atteint.<div class="art-ref">📋 art. 10 et 14 LTVA · pratique AFC Assujettissement</div>';ex.dataset.currentLaw='1'}}

    const s2=d.getElementById('m6c11s2');
    if(s2&&!s2.dataset.currentLaw){
      const o=s2.querySelectorAll('.step-opt');if(o[1])setText(o[1],'B) Droit au DIP sur les dépenses qui remplissent les conditions légales et sont affectées à une activité donnant droit à déduction; l’effet de trésorerie dépend du dossier');
      const ex=d.getElementById('m6c11s2-expl');if(ex)ex.innerHTML='L’inscription peut permettre de récupérer l’impôt préalable sur des dépenses qui remplissent les conditions des art. 28 ss LTVA et sont affectées à une activité donnant droit à déduction. Il faut toutefois distinguer TVA suisse facturée, impôt à l’importation et impôt sur les acquisitions; toutes les dépenses d’une startup ne portent pas automatiquement une TVA déductible. <strong>Aucune position créditrice ou remboursement ne doit être promis à partir d’un profil «startup SaaS»</strong> : le résultat dépend des opérations, des taux, de l’affectation et des pièces. Une inscription volontaire sous le seuil peut être pertinente, mais doit être comparée aux coûts administratifs, à la clientèle et au cash-flow.<br><br>Si, plus tard, le chiffre d’affaires déterminant passe sous le seuil et qu’il est vraisemblable qu’il restera sous le seuil pendant la période fiscale suivante, la radiation peut être demandée au plus tôt pour la fin de la première période fiscale sous le seuil; la demande doit être déposée dans le délai prévu par l’AFC. Il n’existe pas une règle simpliste «un an minimum sous CHF 100\'000».<div class="art-ref">📋 art. 11 · 14 al. 5 · 28 ss LTVA · pratique AFC Radiation</div>';
      s2.dataset.currentLaw='1';
    }

    const s3=d.getElementById('m6c11s3');if(s3){const opts=s3.querySelectorAll('.step-opt');if(opts[1])setText(opts[1],'B) S’annoncer dans les 30 jours dès le début de l’assujettissement; déterminer d’abord cette date selon l’art. 14 et les faits');const ex=d.getElementById('m6c11s3-expl');if(ex&&!ex.dataset.currentLaw){ex.innerHTML='<strong>Art. 66 LTVA :</strong> l’annonce doit intervenir dans les <strong>30 jours dès le début de l’assujettissement</strong>. Il ne faut donc pas mémoriser «30 jours après le dépassement du seuil». Dans ce cas précis, le seuil était suffisamment prévisible au démarrage: le début de l’assujettissement coïncide avec le début de l’activité. Pour une entreprise déjà existante et auparavant libérée, la date peut être différente et doit être déterminée avant de compter les 30 jours. Un retard peut entraîner rappel et intérêts; une conséquence pénale dépend des faits et de la faute. Une dénonciation spontanée ne supprime pas automatiquement une amende: l’effet favorable suppose que toutes les conditions de l’art. 102 soient remplies, tandis que l’impôt et les intérêts restent en principe dus.<div class="art-ref">📋 art. 14 · 66 · 87 · 96 · 102 LTVA</div>';ex.dataset.currentLaw='1'}}
    portalLinks(d);
  }
  function apply(){const d=frame.contentDocument;if(!d?.body)return;if(cfg.module==='M01')patchM01(d);if(cfg.module==='M02')patchM02(d);if(cfg.module==='M03')patchM03(d);if(cfg.module==='M04')patchM04(d);if(cfg.module==='M06')patchM06(d)}
  frame.addEventListener('load',()=>{apply();const d=frame.contentDocument;if(!d?.body)return;const mo=new MutationObserver(()=>{clearTimeout(mo._t);mo._t=setTimeout(apply,90)});mo.observe(d.body,{subtree:true,childList:true,characterData:true})});
})();
