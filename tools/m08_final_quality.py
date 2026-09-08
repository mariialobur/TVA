from pathlib import Path
import re

p=Path('m08-immobilier-construction-tva.html')
t=p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label):
    global t
    n=t.count(old)
    if n:
        t=t.replace(old,new)
        changes.append((label,n))
    else:
        print('WARN',label)

# --- QCM: remove residual blanket rules and fix answer indexes ---
rep(
"{a:'art. 30 LTVA + art. 30 LTVA · pratique AFC',q:'Pour un immeuble mixte (40% commercial + 60% residentiel), clef DIP correcte ?',o:['100% - tout est deductible avec option','40% de DIP deductible (surface commerciale)','50% forfait','0% - immeuble mixte exclut tout DIP'],c:1,e:'Art. 30 LTVA + art. 30 LTVA · pratique AFC : cle surface objective. 40% commercial = 40% DIP deductible. Les 60% residentiels = DIP definitiement perdu.'}",
"{a:'art. 30 LTVA',q:'Des travaux réellement communs concernent un immeuble dont 40% des surfaces servent à une activité optionnée et 60% à des logements. Si la surface reflète correctement l’utilisation, quelle part du DIP commun est déductible ?',o:['100%','40%','50% forfaitaire','0%'],c:1,e:'Après affectation directe des coûts spécifiques, une clé de surface peut être utilisée pour les coûts réellement communs lorsqu’elle reflète l’utilisation. Ici, la part déductible du DIP commun est 40%.'}",
'qcm mixed use scoped')
rep(
"{a:'art. 30 LTVA · pratique AFC',q:'Pour un immeuble à usage mixte, quel ordre est le plus professionnel pour traiter le DIP ?',o:['Affecter directement les charges identifiables puis appliquer une clé objective aux vrais coûts communs','Appliquer automatiquement un prorata de surface à toutes les factures','Déduire 100% dès qu’une partie est optionnée','Refuser tout DIP dès qu’une partie est résidentielle'],c:1,e:'Art. 30 LTVA : commencer par l’affectation directe. Une clé objective n’intervient que pour les coûts réellement communs et doit refléter l’utilisation.'}",
"{a:'art. 30 LTVA · pratique AFC',q:'Pour un immeuble à usage mixte, quel ordre est le plus professionnel pour traiter le DIP ?',o:['Affecter directement les charges identifiables puis appliquer une clé objective aux vrais coûts communs','Appliquer automatiquement un prorata de surface à toutes les factures','Déduire 100% dès qu’une partie est optionnée','Refuser tout DIP dès qu’une partie est résidentielle'],c:0,e:'Art. 30 LTVA : commencer par l’affectation directe. Une clé objective n’intervient que pour les coûts réellement communs et doit refléter l’utilisation.'}",
'qcm mixed answer index')
rep(
"{a:'art. 45 LTVA',q:'Construction SA paie CHF 120\\'000 HT a un sous-traitant roumain non inscrit CH pour un chantier residentiel. Acquisition à vérifier ?',o:['Oui - CHF 9\\'720 a declarer et deduire (DIP recuperable)','Oui - CHF 9\\'720 a declarer mais 0 DIP (residentiel exclu)','Non - < seuil CHF 200\\'000','Non - chantier residentiel hors champ'],c:1,e:'Art. 45 : acquisition à appliquer si les conditions sont remplies = CHF 9\\'720 (120\\'000 x 8,1%) a declarer. Mais chantier residentiel = exclu = 0% DIP. Impact net = CHF 9\\'720 de cout TVA definitif + obligation de declarer.'}",
"{a:'art. 45 LTVA · pratique AFC',q:'Un prestataire étranger facture CHF 120\\'000 pour un chantier résidentiel suisse. Avant de calculer une acquisition, que faut-il faire ?',o:['Appliquer automatiquement 8,1%','Qualifier le contrat, vérifier l’assujettissement suisse du fournisseur, le matériel importé et le régime applicable','Ignorer la TVA parce que le chantier est résidentiel','Appliquer un seuil de CHF 200\\'000'],c:1,e:'La qualité étrangère du fournisseur ne suffit pas. Il faut d’abord déterminer s’il doit être immatriculé en Suisse et si le flux relève de l’impôt à l’importation ou de l’impôt sur les acquisitions. Si un impôt est dû, le droit au DIP dépend ensuite de l’affectation.'}",
'qcm foreign contractor scoped')

# --- Flashcards: legal rule vs practical evidence ---
rep(
"{cat:'Vente & Location',t:'Option art. 22 - 3 conditions',d:'(1) Operation dans champ de l\\'option (liste art. 22 al.1) + (2) Usage non exclusivement résidentiel / non privé et option clairement exercée + (3) Usage commercial confirme. Option claire, documentée et cohérente pendant la durée du contrat.',a:'art. 22 LTVA + OTVA art. 27-29'}",
"{cat:'Vente & Location',t:'Option art. 22 — exercice et limite habitation',d:'L’option doit porter sur une prestation optionnable et être exercée clairement, par indication de la TVA sur la facture/quittance ou par déclaration dans le décompte. En immobilier, elle est exclue lorsque le destinataire affecte ou compte affecter l’objet exclusivement à l’habitation. Bail, usage et piste comptable servent de preuves.',a:'art. 22 LTVA'}",
'card option rule')
rep(
"{cat:'Vente & Location',t:'Option location : coherence du bail',d:'L\\'option art. 22 pour un bail est à maintenir de manière claire et cohérente pendant la durée du bail ; en cas de changement d usage ou de conditions, une correction peut intervenir. Si locataire perd l\\'assujettissement en cours de bail => informer AFC => correction affectation possible.',a:'art. 22 LTVA + art. 31 LTVA'}",
"{cat:'Vente & Location',t:'Option location — suivre l’usage réel',d:'Le statut TVA du locataire n’est pas la condition légale générale de l’option. Surveiller surtout l’usage : si l’objet devient affecté exclusivement à l’habitation ou si l’affectation du bailleur change, réexaminer l’option et les éventuelles corrections d’impôt préalable.',a:'art. 22 + art. 31 LTVA'}",
'card tenant status')
rep(
"{cat:'Vente & Location',t:'Droit de superficie (DDP)',d:'Redevance periodique = assimilee a loyer => exclu avec option possible si superficiaire assujetti. Le terrain reste propriete du constituant = pas de vente TVA.',a:'art. 21 al. 2 ch. 20/21 LTVA + CC art. 779'}",
"{cat:'Vente & Location',t:'Droit de superficie (DDP)',d:'Qualifier séparément la constitution/transmission du droit, la redevance périodique et l’usage immobilier. Une option éventuelle dépend des conditions de l’art. 22, notamment de l’absence d’affectation exclusive à l’habitation, et non du seul statut TVA du superficiaire.',a:'art. 21–22 LTVA · pratique AFC immobilier'}",
'card ddp')
rep(
"{cat:'DIP Immeuble Mixte',t:'Clef DIP - surface (m2)',d:'Cle prioritaire : m2 imposable / m2 total = % DIP deductible. Objective, verifiable, acceptee AFC. Documenter avec plan et tableau. Stable chaque annee.',a:'art. 30 LTVA + art. 30 LTVA · pratique AFC'}",
"{cat:'DIP Immeuble Mixte',t:'Clé de surface — quand l’utiliser',d:'La surface n’est pas une clé obligatoire ni automatiquement prioritaire. Après affectation directe, elle peut convenir aux coûts communs si elle reflète l’utilisation réelle. Documenter plans, surfaces et justification de la méthode.',a:'art. 30 LTVA · pratique AFC'}",
'card surface key')
rep(
"{cat:'DIP Immeuble Mixte',t:'DIP charge directe vs commune',d:'Charge directement affectee a la partie commerciale = DIP 100%. Charge directement affectee a la partie residentielle = DIP 0%. Charge commune = DIP x cle surface.',a:'art. 28 + 30 LTVA'}",
"{cat:'DIP Immeuble Mixte',t:'DIP charge directe vs commune',d:'Une charge directement affectée à une activité donnant droit au DIP suit cette affectation ; une charge directement liée à une activité exclue n’ouvre pas le même droit. Pour un vrai coût commun, appliquer une méthode objective représentant l’utilisation — pas automatiquement la surface.',a:'art. 28–30 LTVA'}",
'card common cost')
rep(
"{cat:'DIP Immeuble Mixte',t:'Documentation DIP immeuble mixte',d:'Preparer systematiquement : plan avec m2 par usage + tableau cle annuelle + liste charges ventilees. L\\'AFC demande ce tableau lors du controle. Sans doc = cle AFC appliquee (defavorable).',a:'art. 30 LTVA + Pratique AFC'}",
"{cat:'DIP Immeuble Mixte',t:'Documentation DIP immeuble mixte',d:'Conserver plans, surfaces/affectations, factures ventilées, calcul de la méthode et justification de sa pertinence. Lors d’un contrôle, le dossier doit permettre de reconstituer le droit au DIP et toute correction.',a:'art. 30 LTVA · pratique AFC'}",
'card documentation')
rep(
"{cat:'DIP Immeuble Mixte',t:'Cle recettes vs surface',d:'Cle recettes (loyers commercial / loyers totaux) acceptable si plus representative que surface (ex. RDC commercial avec loyers tres eleves). Les deux methodes acceptees si objectives et stables.',a:'art. 30 LTVA + OTVA art. 65'}",
"{cat:'DIP Immeuble Mixte',t:'Recettes vs surface',d:'Ni la surface ni les recettes ne sont universelles. Choisir une clé seulement pour les coûts communs et seulement si elle restitue l’utilisation de manière appropriée ; documenter pourquoi cette clé est pertinente pour le poste concerné.',a:'art. 30 LTVA · pratique AFC'}",
'card revenue vs area')
rep(
"{cat:'Construction & Travaux',t:'Concordance CA construction',d:'Chantiers : concilier CA comptable (acomptes, avancement, retenues garantie) avec CA TVA declare. Premiere verification AFC. Fardeau preuve sur l\\'assujetti (art. 70–72 LTVA · concordance).',a:'art. 71-72 LTVA + art. 70–72 LTVA · concordance'}",
"{cat:'Construction & Travaux',t:'Concordance du chiffre d’affaires',d:'Réconcilier la comptabilité et les décomptes TVA, notamment acomptes, factures partielles, avoirs et régularisations. La documentation doit permettre d’expliquer les écarts ; ne pas attribuer cette règle à une jurisprudence non vérifiée.',a:'art. 70–72 LTVA'}",
'card concordance')
rep(
"{cat:'Restructurations',t:'principe de substance économique et interdiction de l’abus - option artificielle',d:'Option art. 22 exercee uniquement pour optimiser le DIP sans activite commerciale reelle = evasion fiscale (3 criteres). L\\'AFC peut contester l\\'option. Substance economique à vérifier.',a:'principe de substance économique et interdiction de l’abus + art. 22 LTVA'}",
"{cat:'Restructurations',t:'Option et substance du dossier',d:'Une option doit correspondre à une opération réellement optionnable et à l’usage documenté. Éviter les montages artificiels et séparer la règle légale de l’art. 22 d’une éventuelle analyse d’abus fondée sur les faits et la jurisprudence pertinente.',a:'art. 22 LTVA · principe d’interdiction de l’abus'}",
'card abuse')
rep(
"{cat:'Restructurations',t:'art. 21–22 LTVA · pratique AFC immobilier - DDP',d:'La redevance periodique d\\'un droit de superficie (DDP) est assimilee a un loyer. Exclue art. 21 al. 2 ch. 20/21. Option possible si usage non exclusivement résidentiel et option claire ; le statut TVA du superficiaire influence l’intérêt économique. Terrain = propriete du constituant.',a:'art. 21–22 LTVA · pratique AFC immobilier + art. 21 LTVA'}",
"{cat:'Restructurations',t:'Droit de superficie — qualification',d:'Analyser le contrat DDP, la redevance et l’usage du bien selon art. 21–22 et la pratique AFC en vigueur. Le statut TVA de l’autre partie peut influencer l’intérêt économique, mais ne remplace pas les conditions légales de l’option.',a:'art. 21–22 LTVA · pratique AFC immobilier'}",
'card ddp clean')
rep(
"{cat:'Restructurations',t:'Interets moratoires AFC',d:'taux DFF applicable, sans automatisme de taux fixe depuis le lendemain de l\\'echeance (art. 87 LTVA). Sur CHF 20\\'000 de DIP indu pendant 3 ans = CHF 3\\'000 d\\'interets supplementaires. Corriger tot = economiser.',a:'art. 87 LTVA'}",
"{cat:'Restructurations',t:'Intérêts moratoires AFC',d:'Appliquer le taux fixé par le DFF pour la période concernée et les règles d’exigibilité applicables. Un support evergreen ne doit pas convertir automatiquement un rappel en un montant d’intérêts avec un taux historique supposé.',a:'art. 87 LTVA · taux DFF applicable'}",
'card interest')

# --- Case 4: the seller/taxable person exercises the option; buyer VAT status is not the legal condition. ---
rep("L'acheteur exerce l'option art. 22.","Le promoteur, en tant que vendeur assujetti, exerce clairement l'option art. 22. L'acheteur prévoit un usage de bureaux, donc non exclusivement d'habitation.",'case4 option actor')
rep("Option art. 22 valide (usage commercial non résidentiel, option claire ; acheteur assujetti donc neutralité économique probable) → DIP intégral CHF 340\\'200 récupérable sur les coûts de construction.","Option art. 22 clairement exercée par le vendeur et usage non exclusivement d'habitation → les coûts de construction affectés à cette vente imposée peuvent ouvrir le droit au DIP selon les conditions générales. Dans le cas simplifié, CHF 340'200 sont déductibles. Le statut TVA de l'acheteur influence surtout la neutralité économique pour lui, pas la condition légale de l'option.",'case4 answer')
rep("Option art. 22 valide → DIP intégral CHF 340'200 récupérable. La TVA de vente (CHF 486'000) est collectée et reversée à l'AFC. L'acheteur SA la déduit comme DIP → opération neutre pour elle.","Dans ce cas simplifié, l'option transforme la vente en opération imposée et les coûts de construction qui lui sont directement affectés ouvrent le droit au DIP. TVA de vente : CHF 486'000 ; DIP de construction : CHF 340'200, sous réserve des conditions générales de déduction. L'acheteur ne peut déduire la TVA que dans la mesure de son propre droit au DIP.",'case4 explanation')
rep("Si Dubois vendait à un particulier SANS option, quel serait le DIP récupérable sur la construction ?","Si Dubois vendait le même immeuble SANS option, la vente restant exclue, quel serait le traitement du DIP directement lié à cette opération dans ce cas simplifié ?",'case4 q2')
rep("Sans option (vente résidentielle à particulier) = exclu art. 21 al. 2 ch. 20/21 → DIP = 0%.","Sans option, la vente immobilière reste exclue selon l'art. 21 al. 2 ch. 20 ; les coûts directement affectés à cette opération exclue n'ouvrent pas le droit au DIP dans ce cas simplifié.",'case4 q2 answer')
rep("Sans option (acheteur particulier non assujetti) : vente exclue art. 21 al. 2 ch. 20/21 → DIP construction = 0%.","Sans option : vente immobilière exclue selon l'art. 21 al. 2 ch. 20. Dans ce cas simplifié, le DIP directement lié à la construction destinée à cette vente n'est pas déductible.",'case4 q2 expl')

# Theory wording: avoid adding a broader 'private-use' prohibition not found in the real-estate option rule.
rep("confirmer l’usage non exclusivement résidentiel / non privé prévu","confirmer que le destinataire n’affecte pas et ne compte pas affecter l’objet exclusivement à l’habitation",'theory option habitation')

# Flashcard/UI counters.
rep("Toutes les 25 cartes vues !","Toutes les 30 cartes vues !",'flash counter')

# Restore completion panel after page reload when state.completed was already saved.
old="""document.addEventListener('DOMContentLoaded',function(){
  SECS.forEach(function(s){var el=document.getElementById('sec-'+s);if(el)el.style.display=s==='theory'?'block':'none';});
  PROG.update();
});"""
new="""document.addEventListener('DOMContentLoaded',function(){
  SECS.forEach(function(s){var el=document.getElementById('sec-'+s);if(el)el.style.display=s==='theory'?'block':'none';});
  PROG.update();
  if(state.completed){
    const box=document.getElementById('m08-complete');
    if(box)box.style.display='flex';
    syncDashboardDone();
  }
});"""
rep(old,new,'completion reload')

p.write_text(t,encoding='utf-8')
print('M08 final quality changes',sum(n for _,n in changes))
for c in changes: print(' -',c)
