from pathlib import Path
import re

p=Path('m08-immobilier-construction-tva.html')
t=p.read_text(encoding='utf-8')

# Repair a few legacy QCM/card formulations that became misleading after removing
# misattributed case-law references.
t=t.replace(
    "q:'L\\'art. 30 LTVA · pratique AFC concerne :'",
    "q:'Pour un immeuble à usage mixte, quel ordre est le plus professionnel pour traiter le DIP ?'"
)
t=t.replace(
    "o:['L\\'imposition a l\\'acquisition pour travaux etrangers','La cle de repartition DIP à vérifier pour immeubles mixtes','L\\'option d\\'imposition art. 22','Les travaux propres art. 31']",
    "o:['Affecter directement les charges identifiables puis appliquer une clé objective aux vrais coûts communs','Appliquer automatiquement un prorata de surface à toutes les factures','Déduire 100% dès qu’une partie est optionnée','Refuser tout DIP dès qu’une partie est résidentielle']"
)
t=t.replace(
    "e:'art. 30 LTVA · pratique AFC (TF 2014) : repere jurisprudentiel sur la cle de repartition DIP des immeubles mixtes. La cle doit etre objective (surface ou recettes), stable dans le temps et documentee. L\\'AFC peut rejeter une cle arbitraire.'",
    "e:'Art. 30 LTVA : commencer par l’affectation directe. Une clé objective n’intervient que pour les coûts réellement communs et doit refléter l’utilisation.'"
)
t=t.replace(
    "t:'art. 30 LTVA · pratique AFC - principe fondateur'",
    "t:'Immeuble mixte — méthode DIP'"
)
t=t.replace(
    "d:'Cle de repartition DIP immeuble mixte doit etre objective (surface ou recettes) et stable. L\\'AFC refuse les cles arbitraires maximisant la deduction. Arret de reference 2014.'",
    "d:'Affecter d’abord directement les charges aux activités concernées. Pour les coûts réellement communs, utiliser une clé objective et économiquement appropriée, documentée et cohérente.'"
)

# Replace blanket foreign-contractor reflexes in remaining QCM/cards.
t=re.sub(
    r"\{a:'art\. 45 LTVA',q:'Un sous-traitant etranger non inscrit CH realise des travaux en Suisse\. Qui declare la TVA \?',o:\[.*?\],c:\d+,e:'.*?'\}",
    "{a:'art. 45 LTVA · pratique AFC',q:'Entreprise étrangère sur un chantier suisse : quel est le premier réflexe ?',o:['Déclarer automatiquement l’impôt sur les acquisitions','Qualifier le contrat, vérifier l’assujettissement suisse du fournisseur et l’importation éventuelle de matériel','Ignorer la TVA si la facture est sans TVA suisse','Retenir 8,1% sur le paiement'],c:1,e:'Avant tout calcul, vérifier le statut TVA du fournisseur étranger, la nature de la prestation et le matériel importé. L’impôt à l’importation ou l’impôt sur les acquisitions dépend de cette qualification.'}",
    t, flags=re.S
)
t=re.sub(
    r"\{cat:'Construction & Travaux',t:'Acquisition sous-traitant etranger',d:'.*?',a:'art\. 45 \+ art\. 8 al\. 2 let\. f LTVA'\}",
    "{cat:'Construction & Travaux',t:'Entreprise étrangère sur chantier suisse',d:'Arbre de décision : 1) tester l’assujettissement suisse du fournisseur ; 2) vérifier si du matériel est importé et l’impôt à l’importation ; 3) tester l’impôt sur les acquisitions lorsque ses conditions sont remplies ; 4) déterminer le DIP selon l’affectation.',a:'art. 45 LTVA · pratique AFC'}",
    t, flags=re.S
)

# Append five current-law QCM so the advertised 35-question test is real.
if 'M08-AUDIT-Q31' not in t:
    m=re.search(r'(var\s+QS\s*=\s*\[)(.*?)(\n\];\s*\nvar\s+QUIZ\s*=)',t,re.S)
    if not m:
        raise SystemExit('QS block not found')
    extra=""",
  {a:'M08-AUDIT-Q31 · art. 21 al. 2 ch. 21 let. c LTVA',q:'Une place de parc privée est louée indépendamment de tout appartement ou local exclu. Quel traitement de principe ?',o:['Exclue et optionnable','Imposable au taux normal','Toujours exonérée','Hors champ TVA'],c:1,e:'La location de places de parc ne relevant pas du domaine public est imposable de plein droit. Elle peut suivre une location immobilière exclue seulement lorsqu’elle en constitue une prestation accessoire.'},
  {a:'M08-AUDIT-Q32 · art. 22 LTVA',q:'Comment l’assujetti peut-il exercer l’option pour une prestation immobilière optionnable ?',o:['Uniquement par clause notariale','Uniquement après autorisation AFC','Par indication claire de la TVA sur la facture/quittance ou par déclaration de l’imposition dans le décompte TVA','Uniquement si le destinataire possède un numéro TVA'],c:2,e:'L’option s’exerce par une manifestation claire : TVA indiquée sur la facture/quittance ou imposition déclarée dans le décompte. Pour l’immobilier, l’usage exclusivement d’habitation bloque l’option.'},
  {a:'M08-AUDIT-Q33 · pratique AFC · art. 45 LTVA',q:'Une entreprise étrangère non inscrite en Suisse apporte ses propres matériaux pour exécuter des travaux sur un immeuble suisse. Quel réflexe est correct ?',o:['Acquisition art. 45 automatique dans tous les cas','Vérifier notamment l’assujettissement suisse du fournisseur et l’impôt à l’importation sur la prestation avant de conclure à une acquisition','Aucune TVA suisse possible','Le client retient automatiquement 8,1%'],c:1,e:'Lorsque le fournisseur étranger importe du matériel pour exécuter les travaux, l’impôt à l’importation peut porter sur la valeur totale de la prestation. Il faut aussi tester son éventuel assujettissement suisse.'},
  {a:'M08-AUDIT-Q34 · art. 71 OTVA',q:'Une phase de rénovation dépasse 5% de la valeur d’assurance du bâtiment avant rénovation. Quelle conséquence méthodologique ?',o:['Seules les dépenses augmentant la valeur comptent','L’analyse de correction porte sur l’ensemble des coûts de la phase selon les règles OTVA, y compris les dépenses de maintien de valeur','Aucune conséquence TVA','La période résiduelle passe de 20 à 10 ans'],c:1,e:'Le seuil de 5% déclenche l’application de la règle OTVA à l’ensemble des coûts de la phase de rénovation, sans limiter l’analyse aux seules dépenses augmentant la valeur.'},
  {a:'M08-AUDIT-Q35 · art. 24 al. 6 let. c LTVA',q:'Dans la contre-prestation d’une livraison immobilière, comment traiter la part afférente à la valeur du sol ?',o:['La taxer toujours à 8,1%','L’exclure de la base de calcul de la TVA et la ventiler séparément','Appliquer 2,6%','La traiter comme un subside'],c:1,e:'La part de la contre-prestation afférente à la valeur du sol n’entre pas dans la base de calcul de la TVA. Le dossier doit donc permettre une ventilation défendable sol/bâtiment.'}"""
    t=t[:m.start(3)] + extra + t[m.start(3):]

# Restore completion panel after reload if M08 was already completed.
if "if(state.completed){const box=document.getElementById('m08-complete')" not in t:
    # Insert immediately after the final initial progress update when available.
    candidates=["PROG.update();\nNAV.go('theory');", "NAV.go('theory');\nPROG.update();"]
    inserted=False
    for old in candidates:
        if old in t:
            if old.startswith('PROG.update'):
                new=old+"\nif(state.completed){const box=document.getElementById('m08-complete');if(box)box.style.display='flex';syncDashboardDone();}"
            else:
                new=old+"\nif(state.completed){const box=document.getElementById('m08-complete');if(box)box.style.display='flex';syncDashboardDone();}"
            t=t.replace(old,new,1)
            inserted=True
            break
    if not inserted:
        print('WARN completion reload hook not inserted')

p.write_text(t,encoding='utf-8')
print('M08 quiz fix applied; audit QCM markers:',t.count('M08-AUDIT-Q'))
