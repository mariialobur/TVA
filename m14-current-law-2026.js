'use strict';
(()=>{
  const q=window.M14_POOL_1?.find(x=>x.id===19);
  if(!q)throw new Error('M14 Q19 unavailable for current-law patch');
  q.question='Pour une location d’un logement que le destinataire affecte ou compte affecter exclusivement à des fins d’habitation :';
  q.options=['l’option pour l’imposition est en principe exclue','l’option est toujours obligatoire','l’option dépend uniquement du souhait du locataire','le taux réduit s’applique automatiquement'];
  q.correct=0;
  q.explanation='Art. 22 al. 2 let. b LTVA: pour les prestations immobilières visées, l’option est exclue lorsque le destinataire affecte ou compte affecter l’objet exclusivement à des fins d’habitation. Le critère actuel n’est plus formulé comme une utilisation exclusivement «privée».';
})();
