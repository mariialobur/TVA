'use strict';
(()=>{
  const C=window.M13_CASES,Q=window.M13_QS,F=window.M13_FC;
  if(!Array.isArray(C)||!Array.isArray(Q)||!Array.isArray(F))throw new Error('M13 core data missing');

  const c4=C.find(x=>String(x.title||'').startsWith('04'));
  if(c4?.steps?.[0]){
    c4.steps[0][1][1]='Sécuriser le pouvoir de représentation et les droits dans le Portail AFC / Décompte TVA pro; l’autorité peut exiger une procuration écrite et communique en principe avec le représentant jusqu’à révocation.';
    c4.steps[0][3]='Dans la procédure administrative, l’art. 11 PA régit la représentation ordinaire. Les autorisations et rôles du Portail AFC / Décompte TVA pro ainsi que l’adresse de correspondance doivent être configurés séparément selon le besoin.';
  }

  const qp=Q.find(x=>x[1]==='Le renseignement interrompt prescription ?');
  if(qp){
    qp[0]='Art.42/69';
    qp[1]='Le renseignement juridique donné par l’AFC interrompt-il, à lui seul, la prescription ?';
    qp[2]=['Oui','Non; mais il faut analyser séparément si la demande ou communication de l’assujetti constitue un acte interruptif au sens de l’art. 42','Toujours 2 ans','Seulement pour le passé'];
    qp[3]=1;
    qp[4]='La page AFC sur l’art. 69 indique que les renseignements n’interrompent pas la prescription. Cela ne signifie pas que toute demande du contribuable est neutre: l’art. 42 peut donner un effet interruptif à une déclaration écrite visant à fixer ou corriger une créance déterminée. Ne jamais compter sur un ruling pour sécuriser un délai sans analyse art. 42.';
  }

  const qPortal=Q.find(x=>x[0]==='ePortal'&&x[1]==='Fiduciaire ?');
  if(qPortal){
    qPortal[0]='Portail AFC';
    qPortal[1]='Fiduciaire dans Décompte TVA pro ?';
    qPortal[2]=['Aucun rôle','Peut recevoir les rôles «remplir uniquement» ou «remplir et soumettre» selon l’autorisation accordée','Doit être administrateur de la SA','Seulement papier'];
    qPortal[4]='L’AFC prévoit des rôles distincts dans Décompte TVA pro et un mécanisme d’invitation/autorisation pour la fiduciaire.';
  }

  const fc=F.find(x=>x[1]==='Prescription');
  if(fc){
    fc[0]='Art.42/69';
    fc[2]='Le renseignement juridique donné par l’AFC n’interrompt pas à lui seul la prescription. Analyser séparément si la demande/communication de l’assujetti remplit les conditions interruptives de l’art. 42.';
  }

  if(typeof document!=='undefined'){
    const mini=[...document.querySelectorAll('.mini')].find(x=>x.querySelector('strong')?.textContent.trim()==='Pas de tolling');
    if(mini){
      const s=mini.querySelector('strong'),t=mini.querySelector('span');
      if(s)s.textContent='Prescription — art. 42';
      if(t)t.textContent='Le renseignement juridique donné par l’AFC n’interrompt pas à lui seul la prescription. Pour la demande ou communication de l’assujetti, analyser séparément si elle vise à fixer ou corriger une créance déterminée au sens de l’art. 42; ne jamais compter sur un ruling pour sauver un délai.';
    }
    const h=[...document.querySelectorAll('h3')].find(x=>x.textContent.includes('Représentation : mandat, procuration, ePortal'));
    if(h)h.textContent='3 — Représentation : mandat, procuration, Portail AFC';
    const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);let n;
    while((n=walker.nextNode())){
      if(n.nodeValue?.includes('autorisation ePortal'))n.nodeValue=n.nodeValue.replaceAll('autorisation ePortal','autorisation / rôle dans le Portail AFC');
    }
  }
})();
