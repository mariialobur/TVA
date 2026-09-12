'use strict';
(()=>{
  const cfg=window.COURSE_GATE_CONFIG||{},frame=document.getElementById('module');
  const DATA={
    M04:{
      title:'Clôture TVA, ERP et concordance — note au senior',
      subtitle:'Comptabilité · méthode effective · clôture annuelle · risque élevé',
      scenario:"Une PME vaudoise clôture sa TVA 2026 selon la méthode effective et les contre-prestations convenues. Le grand-livre contient des ventes suisses à 8,1 %, des exportations documentées, des notes de crédit sur ventes suisses et un abonnement SaaS acheté à un fournisseur américain. Les comptes TVA de l’ERP ne concordent pas exactement avec les décomptes déjà déposés et le collaborateur précédent a utilisé plusieurs codes TVA pour des opérations similaires.",
      prompts:[
        'Décrivez l’ordre de vos contrôles avant toute écriture de correction.',
        'Expliquez comment vous rapprochez chiffre d’affaires, comptes TVA, codes ERP et décomptes AFC.',
        'Qualifiez le traitement des exportations, notes de crédit et du SaaS étranger.',
        'Indiquez quelles écritures ou corrections vous passez seulement après validation des écarts.',
        'Listez les pièces que vous conservez dans le dossier de clôture et la manière de documenter la finalisation.'
      ],
      model:[
        ['1. Cartographier les flux','Reconstituer d’abord les flux par nature et par période : ventes suisses imposables, exportations, réductions de contre-prestation et achats de services étrangers. Ne pas corriger le grand-livre avant d’avoir identifié la cause de chaque écart.'],
        ['2. Rapprocher comptabilité et décomptes','Rapprocher les comptes de chiffre d’affaires et de TVA avec les chiffres déclarés, puis contrôler les codes TVA de l’ERP. Les numéros de comptes sont une convention du mandat : la LTVA impose surtout une comptabilité permettant de constater avec sûreté les faits déterminants.'],
        ['3. Qualifier les opérations','Les exportations de biens peuvent être exonérées avec droit au DIP si les conditions et preuves de l’art. 23 sont réunies. Les notes de crédit réduisent la contre-prestation concernée. Le SaaS étranger reçu en Suisse doit être examiné sous l’angle de l’impôt sur les acquisitions de l’art. 45, avec traitement séparé de la TVA due et du DIP éventuel.'],
        ['4. Corriger et finaliser','Une fois l’écart expliqué, passer les écritures de régularisation dans les comptes/codes du mandat et utiliser la rectification ou la finalisation prévue par l’art. 72 lorsque nécessaire. Une neutralité nette sur une acquisition ne justifie pas de supprimer les écritures ou la déclaration correspondante.'],
        ['5. Dossier de preuve','Conserver grand-livre, rapprochement TVA, mapping des codes ERP, factures, notes de crédit, preuves d’exportation, factures du prestataire étranger, calculs et note de clôture signée/datée.']
      ],
      sources:'art. 70 et 72 LTVA · art. 23 LTVA · art. 45 LTVA · pratique AFC'
    },
    M05:{
      title:'DIP d’une activité mixte — méthode de travail défendable',
      subtitle:'DIP · affectation directe · activité exclue · subvention · usage privé',
      scenario:"Une société exploite une activité de conseil imposable et une activité de formation exclue. Elle reçoit aussi une subvention cantonale pour un projet utilisant des locaux et outils communs. Les factures 2026 comprennent des coûts directement liés au conseil, d’autres directement liés à la formation, des coûts communs de locaux/logiciels et un véhicule utilisé partiellement à titre privé. Le client propose d’appliquer un seul pourcentage de chiffre d’affaires à tout le DIP.",
      prompts:[
        'Séparez les catégories de dépenses avant tout calcul de correction du DIP.',
        'Expliquez la différence entre affectation directe et clé de répartition des coûts communs.',
        'Traitez séparément activité exclue, subvention et usage privé.',
        'Indiquez pourquoi un ratio unique appliqué à toutes les charges peut être indéfendable.',
        'Décrivez la documentation minimale permettant de soutenir la méthode choisie lors d’un contrôle AFC.'
      ],
      model:[
        ['1. Affectation directe d’abord','Attribuer directement les coûts qui peuvent l’être. Le DIP grevant les coûts affectés exclusivement à l’activité entrepreneuriale donnant droit à déduction suit les art. 28 ss; les coûts directement liés à une activité exclue sans droit au DIP ne doivent pas être noyés dans une clé globale.'],
        ['2. Coûts réellement communs','Pour les charges réellement communes, appliquer une méthode objective qui reflète l’utilisation économique. L’art. 30 exige une correction lorsque des biens ou services sont utilisés à la fois pour des activités ouvrant et n’ouvrant pas droit à déduction.'],
        ['3. Subvention et privé','Analyser la subvention séparément : elle n’est pas transformée en chiffre d’affaires taxable par le seul fait qu’elle finance un projet, mais l’art. 33 peut imposer une réduction du DIP selon les coûts financés et l’affectation. L’usage privé doit lui aussi être traité séparément selon les règles de correction applicables.'],
        ['4. Pas de clé universelle','Un ratio chiffre d’affaires peut parfois être objectif pour certains coûts communs, mais il ne remplace ni l’affectation directe ni l’analyse des coûts financés par une subvention. La méthode doit être économiquement défendable et appliquée de manière cohérente.'],
        ['5. Preuve','Conserver la matrice d’affectation, factures, centres de coûts, convention de subvention, calcul de la clé, justification de son choix, éléments d’usage privé et rapprochement avec le décompte TVA.']
      ],
      sources:'art. 28–30 et 33 LTVA · pratique AFC sur la réduction du DIP'
    },
    M06:{
      title:'Cartographie TVA d’un dossier international',
      subtitle:'Export · services B2B · acquisitions · importation · preuves',
      scenario:"AlpTech SA, établie à Lausanne, vend une machine à un client allemand; la marchandise quitte la Suisse et les documents d’exportation sont disponibles. Elle fournit aussi du conseil à une société française identifiée comme entreprise, achète un abonnement SaaS à un fournisseur américain sans établissement en Suisse et importe des composants italiens en étant elle-même importateur selon les documents douaniers.",
      prompts:[
        'Qualifiez séparément chacune des quatre opérations avant de parler de taux.',
        'Déterminez le lieu ou le type d’impôt pertinent pour chaque flux.',
        'Expliquez les conditions de l’exonération de l’exportation et les preuves à conserver.',
        'Traitez le SaaS étranger et l’importation des composants sans confondre impôt sur les acquisitions et impôt à l’importation.',
        'Préparez une courte check-list de décompte et de dossier justificatif pour la fiduciaire.'
      ],
      model:[
        ['1. Machine exportée','La livraison de la machine doit d’abord être localisée selon les règles de livraison. Si l’exportation depuis la Suisse est établie et les conditions remplies, l’art. 23 permet l’exonération avec droit au DIP; la preuve de sortie reste déterminante.'],
        ['2. Conseil B2B à l’étranger','Pour un service relevant de la règle générale B2B de l’art. 8 al. 1, le lieu est chez le destinataire. Une prestation à l’entreprise française est donc à analyser comme prestation localisée à l’étranger, sous réserve d’une exception spécifique.'],
        ['3. SaaS américain','Le service reçu par AlpTech SA en Suisse doit être examiné sous l’angle de l’impôt sur les acquisitions de l’art. 45. Si les conditions du DIP sont remplies, la TVA due sur acquisition et le DIP peuvent se neutraliser économiquement, mais les deux traitements doivent rester traçables.'],
        ['4. Composants importés','L’impôt à l’importation relève du régime d’importation et des documents OFDF. Le droit au DIP dépend notamment de la qualité de l’importateur/destinataire et de l’affectation entrepreneuriale; il ne faut pas confondre cet impôt avec l’impôt sur les acquisitions.'],
        ['5. Dossier','Conserver contrat/factures, preuve du statut B2B lorsque pertinente, documents de transport et d’exportation, factures du fournisseur étranger, décisions/documents d’importation OFDF et mapping vers les chiffres du décompte.']
      ],
      sources:'art. 7, 8, 23, 45 et 50 ss LTVA · pratique AFC/OFDF'
    },
    M08:{
      title:'Immeuble mixte — option, DIP et changement d’affectation',
      subtitle:'Immobilier · habitation · option · affectation directe · correction ultérieure',
      scenario:"ImmoRiviera SA rénove un immeuble à usage mixte. Le rez-de-chaussée est loué comme bureaux à une entreprise, tandis que les étages sont loués exclusivement comme logements. Les factures de rénovation comprennent des travaux directement attribuables aux bureaux, d’autres aux logements et des coûts communs pour toiture, ascenseur et parties techniques. Deux ans plus tard, une partie des bureaux est transformée en logement.",
      prompts:[
        'Qualifiez les locations commerciales et résidentielles et dites où une option est envisageable.',
        'Expliquez le traitement du DIP sur les travaux directement attribuables et sur les coûts communs.',
        'Proposez une clé de répartition défendable pour les coûts réellement communs et expliquez pourquoi elle doit refléter l’utilisation.',
        'Analysez la conséquence TVA de la transformation ultérieure d’une surface de bureaux en logement.',
        'Listez les documents qu’un dossier immobilier TVA professionnel doit contenir.'
      ],
      model:[
        ['1. Location et option','La location immobilière est en principe exclue selon l’art. 21. L’option peut être examinée pour les surfaces commerciales, mais l’art. 22 al. 2 let. b exclut l’option lorsque le destinataire affecte ou compte affecter l’objet exclusivement à des fins d’habitation. Les logements restent donc à traiter séparément.'],
        ['2. DIP direct et commun','Affecter directement les factures propres aux surfaces commerciales ou résidentielles. Les coûts communs doivent faire l’objet d’une correction/répartition objective lorsque l’immeuble sert à la fois des activités ouvrant et n’ouvrant pas droit au DIP.'],
        ['3. Clé objective','La surface peut être une clé pertinente si elle reflète réellement la consommation des coûts communs; pour certains équipements, une autre clé peut être plus fidèle. Le dossier doit expliquer le choix plutôt que d’appliquer mécaniquement un pourcentage unique.'],
        ['4. Changement ultérieur','Le passage d’une surface jusque-là utilisée pour une activité ouvrant droit au DIP à une utilisation résidentielle exclue constitue un changement d’affectation à analyser selon les règles de correction de l’impôt préalable, notamment l’art. 31 et la valeur résiduelle applicable aux immeubles.'],
        ['5. Preuve immobilière','Conserver plans/surfaces, baux et affectation réelle, décisions d’option, factures de travaux, ventilation directe, calcul des clés, historique des changements d’usage et rapprochement annuel du DIP.']
      ],
      sources:'art. 21, 22, 30–32 LTVA · pratique AFC Immobilier'
    }
  };
  if(!frame||!cfg.module||!DATA[cfg.module])return;
  const MODULE=cfg.module,d=DATA[MODULE],KEY='tvaLegacyCapstoneV1_'+MODULE,MIN_WORDS=80,MIN_CHARS=500;
  const read=()=>{try{return JSON.parse(localStorage.getItem(KEY)||'{}')}catch(e){return {}}};
  const write=v=>{try{localStorage.setItem(KEY,JSON.stringify(v))}catch(e){}};
  const words=s=>(String(s||'').trim().match(/\S+/g)||[]).length;
  const ready=s=>String(s||'').trim().length>=MIN_CHARS&&words(s)>=MIN_WORDS;
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const completionTarget=t=>{const oc=t.getAttribute?.('onclick')||'',txt=(t.textContent||'').trim();return /(?:finishModule|PROG\.finish|PROG\.goNext|goNextModule)\s*\(/.test(oc)||new RegExp('(?:Terminer|Marquer)[^\\n]{0,40}'+MODULE,'i').test(txt)};

  function addStyles(doc){
    if(doc.getElementById('legacy-capstone-style'))return;
    const st=doc.createElement('style');st.id='legacy-capstone-style';st.textContent=`
      .legacy-capstone{background:#fff;border:2px solid rgba(201,168,76,.68);border-radius:12px;margin:24px 0 18px;overflow:hidden;box-shadow:0 8px 24px rgba(11,37,69,.07)}
      .legacy-capstone-head{background:#0B2545;padding:18px 22px}.legacy-capstone-kicker{font-size:10.5px;font-weight:800;letter-spacing:.09em;text-transform:uppercase;color:#C9A84C;margin-bottom:6px}.legacy-capstone-title{font-size:17px;font-weight:700;color:#fff;line-height:1.35}.legacy-capstone-sub{font-size:12px;color:rgba(255,255,255,.58);margin-top:5px}
      .legacy-capstone-body{padding:20px 22px}.legacy-capstone-scenario{background:#F8F5EE;border:1px solid #EDE8DC;border-radius:9px;padding:15px 16px;font-size:13.5px;line-height:1.72;color:#2C2C3E;margin-bottom:16px}.legacy-capstone-body h4{margin:0 0 8px;color:#0B2545;font-size:15px}.legacy-capstone-prompts{padding-left:22px;margin:8px 0 16px}.legacy-capstone-prompts li{margin:7px 0;font-size:13.2px;line-height:1.55}
      .legacy-capstone textarea{width:100%;min-height:250px;resize:vertical;border:1px solid #C9C1AF;border-radius:9px;background:#fff;padding:13px;font:13.5px/1.55 Arial,Helvetica,sans-serif;color:#1A1A2E}.legacy-capstone textarea:focus{outline:2px solid rgba(31,77,140,.22);border-color:#1F4D8C}.legacy-capstone-meta{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:7px 0 12px;font-size:11.5px;color:#667085}.legacy-capstone-actions{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.legacy-capstone-btn{border:0;border-radius:8px;padding:10px 14px;background:#0B2545;color:#fff;font-weight:800;cursor:pointer}.legacy-capstone-btn:disabled{opacity:.45;cursor:not-allowed}.legacy-capstone-saved{font-size:11.5px;color:#2A6B48;font-weight:700}.legacy-capstone-model{display:none;margin-top:16px;padding:16px;border-left:4px solid #2A6B48;background:#E7F5EC;border-radius:9px}.legacy-capstone-model.show{display:block}.legacy-capstone-model h4{margin:0 0 10px}.legacy-capstone-model-item{margin:11px 0}.legacy-capstone-model-item strong{color:#0B2545}.legacy-capstone-model-item p{margin:4px 0;line-height:1.58}.legacy-capstone-source{margin-top:12px;font-size:11.5px;color:#52606d}.legacy-capstone-toast{position:fixed;right:16px;bottom:16px;z-index:99999;max-width:520px;padding:13px 16px;border-radius:9px;background:#FEF3D8;color:#684600;border:1px solid #dfbf70;font:13px/1.5 system-ui,sans-serif;box-shadow:0 8px 28px #0003}
      @media(max-width:700px){.legacy-capstone textarea{min-height:290px}.legacy-capstone-meta{display:block}}
    `;doc.head.appendChild(st);
  }
  function modelHtml(){return d.model.map((x,i)=>`<div class="legacy-capstone-model-item"><strong>${i+1}. ${esc(x[0])}</strong><p>${esc(x[1])}</p></div>`).join('')}
  function toast(doc,msg){let x=doc.getElementById('legacy-capstone-toast');if(!x){x=doc.createElement('div');x.id='legacy-capstone-toast';x.className='legacy-capstone-toast';doc.body.appendChild(x)}x.textContent=msg;clearTimeout(x._t);x._t=setTimeout(()=>x.remove(),7000)}
  function bindGuard(doc,card){
    if(doc.documentElement.dataset.legacyCapstoneGuard===MODULE)return;
    doc.documentElement.dataset.legacyCapstoneGuard=MODULE;
    doc.addEventListener('click',e=>{
      const t=e.target.closest?.('button,a');if(!t||!completionTarget(t))return;
      const s=read();if(s.modelShown===true)return;
      e.preventDefault();e.stopImmediatePropagation();
      try{if(typeof doc.defaultView.goto==='function')doc.defaultView.goto('cases')}catch(err){}
      toast(doc,'Validation refusée : terminez le dossier professionnel à réponse libre et comparez votre analyse avec le modèle.');
      setTimeout(()=>card.scrollIntoView({behavior:'smooth',block:'center'}),50);
    },true);
  }
  function build(doc){
    if(!doc?.body)return false;addStyles(doc);
    let card=doc.getElementById('legacy-capstone-'+MODULE);
    if(card){bindGuard(doc,card);return true}
    const sec=doc.getElementById('sec-cases');if(!sec)return false;
    const saved=read();
    card=doc.createElement('div');card.id='legacy-capstone-'+MODULE;card.className='legacy-capstone';
    card.innerHTML=`<div class="legacy-capstone-head"><div class="legacy-capstone-kicker">Dossier professionnel · réponse libre · obligatoire</div><div class="legacy-capstone-title">${esc(d.title)}</div><div class="legacy-capstone-sub">${esc(d.subtitle)}</div></div><div class="legacy-capstone-body"><div class="legacy-capstone-scenario">${esc(d.scenario)}</div><h4>Votre mission</h4><p style="font-size:13px;line-height:1.6;color:#475467">Rédigez une note structurée comme pour une revue senior. La conclusion seule ne suffit pas : exposez qualification, base juridique, traitement TVA, preuve et action recommandée.</p><ol class="legacy-capstone-prompts">${d.prompts.map(x=>`<li>${esc(x)}</li>`).join('')}</ol><label><strong>Votre analyse</strong></label><textarea class="legacy-capstone-draft" spellcheck="true" placeholder="Rédigez votre note professionnelle ici…">${esc(saved.draft||'')}</textarea><div class="legacy-capstone-meta"><span class="legacy-capstone-count"></span><span>Minimum : ${MIN_WORDS} mots et ${MIN_CHARS} caractères avant comparaison.</span></div><div class="legacy-capstone-actions"><button type="button" class="legacy-capstone-btn">Comparer avec le modèle</button><span class="legacy-capstone-saved"></span></div><div class="legacy-capstone-model"><h4>Modèle de contrôle</h4><p style="font-size:12.5px;line-height:1.55">Comparez la structure du raisonnement, les réserves et la preuve, pas seulement la conclusion.</p>${modelHtml()}<div class="legacy-capstone-source"><strong>Références :</strong> ${esc(d.sources)}</div></div></div>`;
    const nav=[...sec.children].find(x=>x.classList?.contains('section-nav'));
    if(nav)sec.insertBefore(card,nav);else sec.appendChild(card);
    const ta=card.querySelector('.legacy-capstone-draft'),count=card.querySelector('.legacy-capstone-count'),btn=card.querySelector('.legacy-capstone-btn'),model=card.querySelector('.legacy-capstone-model'),msg=card.querySelector('.legacy-capstone-saved');
    const refresh=()=>{const s=read(),v=ta.value;count.textContent=words(v)+' mots · '+v.trim().length+' caractères';btn.disabled=!ready(v)&&s.modelShown!==true;btn.textContent=s.modelShown?'✓ Modèle affiché':'Comparer avec le modèle';model.classList.toggle('show',s.modelShown===true);msg.textContent=s.modelShown?'Dossier validé sur ce navigateur.':(v.trim()?'Brouillon enregistré.':'')};
    ta.addEventListener('input',()=>{const s=read();s.draft=ta.value;s.updatedAt=Date.now();write(s);refresh()});
    btn.addEventListener('click',()=>{const s=read();if(!ready(ta.value)&&s.modelShown!==true)return;s.draft=ta.value;s.modelShown=true;s.completedAt=Date.now();write(s);refresh();model.scrollIntoView({behavior:'smooth',block:'nearest'})});
    bindGuard(doc,card);refresh();return true;
  }
  function apply(){try{return build(frame.contentDocument)}catch(e){return false}}
  frame.addEventListener('load',()=>{setTimeout(apply,0);setTimeout(apply,180)});
  let n=0;const t=setInterval(()=>{n++;if(apply()||n>120)clearInterval(t)},50);
})();
