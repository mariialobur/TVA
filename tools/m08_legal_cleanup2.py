from pathlib import Path

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

# Theory: do not attribute a generic allocation rule to an unidentified TF case.
rep(
"Le TF confirme : la répartition DIP d'un immeuble mixte doit se faire selon une clé <strong>objective et économiquement justifiée</strong> (surface ou recettes). L'AFC rejette les clés arbitraires maximisant la déduction. La méthode doit être stable d'une année à l'autre et documentée.",
"L'art. 30 LTVA impose une correction en fonction de l'utilisation. Après l'affectation directe, une clé appliquée aux coûts réellement communs doit donc être <strong>objective et économiquement appropriée</strong>. Surface, recettes ou une autre clé peuvent convenir selon les faits ; la méthode doit être justifiée et documentée.",
'b4 unidentified TF claim')
rep(
"Mais si le propriétaire a déduit le DIP sur des travaux liés à ce bail non optionné → rappel de DIP sur toute la période non prescrite (5 ans).",
"Mais si le propriétaire a déduit du DIP sur des travaux liés à un bail exclu non optionné, il faut reconstituer le droit à déduction, tester une éventuelle correction d'affectation et appliquer les règles de prescription effectivement pertinentes au dossier.",
'b3 fixed prescription')

# QCM: option prohibition is exclusive habitation, not any loss of entrepreneurial/DIP status by the tenant.
rep(
"{a:'art. 22 + art. 31 LTVA',q:'Un propriétaire loue avec option art. 22 à une entreprise. Le locataire cesse ensuite toute activité entrepreneuriale et utilise les locaux pour un usage privé/résidentiel. Bon réflexe ?',o:['Rien - l option reste toujours acquise','Analyser immédiatement la validité de l option, l usage réel et une éventuelle correction d affectation','Renégocier seulement le loyer hors TVA','Rembourser automatiquement le locataire de toute la TVA'],c:1,e:'Le point décisif n est pas seulement le numéro TVA du locataire : il faut vérifier l usage réel. Si l objet devient utilisé exclusivement pour l habitation ou hors activité donnant droit au DIP, l option peut ne plus être défendable et une correction art. 31 doit être analysée.'}",
"{a:'art. 22 + art. 31 LTVA',q:'Un propriétaire a valablement opté pour la location de bureaux. Le locataire transforme ensuite réellement les locaux en logement utilisé exclusivement à l’habitation. Bon réflexe ?',o:['Rien - l option reste toujours acquise','Réexaminer immédiatement l option, la facturation et les éventuelles conséquences sur le DIP du bailleur','Conserver la TVA uniquement parce que le locataire était auparavant une entreprise','Appliquer automatiquement le taux hôtelier'],c:1,e:'En immobilier, l’affectation exclusive à l’habitation bloque l’option. Le changement d’usage doit donc être documenté et ses conséquences sur la facturation et l’impôt préalable du bailleur analysées. Le simple statut TVA du locataire n’est pas le critère légal.'}",
'qcm option change')

# QCM: seller exercises option; buyer's VAT registration does not create the option.
rep(
"{a:'art. 22 LTVA',q:'Promoteur vend un immeuble de bureaux CHF 5\\'000\\'000 HT a une SA assujettie avec option. TVA facturee ?',o:['CHF 0 - vente toujours exclue','CHF 405\\'000 (5\\'000\\'000 x 8,1%)','CHF 130\\'000 (5\\'000\\'000 x 2,6%)','TVA sur la plus-value uniquement'],c:1,e:'Option art. 22 valide (acheteur SA assujettie, immeuble commercial) : TVA = CHF 5\\'000\\'000 x 8,1% = CHF 405\\'000. La SA acheteur deduit comme DIP -> neutre pour elle. Le promoteur recover son DIP construction.'}",
"{a:'art. 22 LTVA',q:'Un promoteur assujetti vend pour CHF 5\\'000\\'000 un immeuble de bureaux que l’acheteur destine à un usage non résidentiel. Le vendeur exerce clairement l’option. TVA au taux normal ?',o:['CHF 0 - vente toujours exclue','CHF 405\\'000 (5\\'000\\'000 x 8,1%)','CHF 130\\'000 (5\\'000\\'000 x 2,6%)','TVA sur la plus-value uniquement'],c:1,e:'Dans ce cas simplifié, l’option est exercée par le vendeur et l’usage n’est pas exclusivement d’habitation. TVA : CHF 5\\'000\\'000 × 8,1% = CHF 405\\'000. L’acheteur ne déduit cette TVA que dans la mesure de son propre droit au DIP.'}",
'qcm sale option actor')

# QCM: revenue/surface keys are not pre-approved universally.
rep(
"{a:'art. 30 LTVA',q:'Pour un immeuble mixte, la cle de repartition DIP \"recettes\" est :',o:['Jamais acceptable','Acceptable si loyers commerciaux tres differents des loyers residentiels','Toujours preferee a la cle surface','Imposee par l\\'AFC'],c:1,e:'La cle recettes (CA commercial/CA total) est acceptable quand elle est plus representative que la cle surface - par exemple si le RDC commercial a des loyers tres eleves proportionnellement. Les deux methodes sont validees par l\\'AFC si objectivement justifiees.'}",
"{a:'art. 30 LTVA',q:'Pour des coûts réellement communs d’un immeuble mixte, quand une clé fondée sur les recettes peut-elle être retenue ?',o:['Jamais','Lorsqu’elle reflète de manière appropriée l’utilisation des coûts concernés et que la méthode est documentée','Toujours à la place de la surface','Uniquement sur autorisation préalable de l’AFC'],c:1,e:'Aucune clé n’est universelle. Les recettes peuvent servir d’indicateur si elles représentent l’utilisation des inputs concernés ; la justification économique et la documentation de la méthode sont déterminantes.'}",
'qcm revenue key')

# QCM: keep acquisition-tax arithmetic only after the legal qualification has already been established.
rep(
"{a:'art. 45 + art. 8 al. 2 let. f LTVA',q:'Un EG suisse (assujetti) confie les travaux de peinture a un sous-traitant polonais non inscrit CH. Facture CHF 45\\'000 HT. Chantier commercial (DIP 100%). Impact net AFC ?',o:['CHF 3\\'645 de cout TVA','CHF 0 net (acquisition declaree + dip deduit)','CHF 1\\'822,50 (50%)','CHF 3\\'645 - applicable seulement si > CHF 100\\'000'],c:1,e:'Acquisition : CHF 45\\'000 x 8,1% = CHF 3\\'645 declaree. DIP (chantier commercial 100%) = CHF 3\\'645 deduit. Impact net = CHF 0. Obligation procedurale mais pas de cout financier pour chantier 100% commercial.'}",
"{a:'art. 45 LTVA · art. 28 LTVA',q:'Après vérification du statut du fournisseur, du matériel importé et du contrat, une prestation étrangère de CHF 45\\'000 est effectivement soumise à l’impôt sur les acquisitions à 8,1%. Elle sert exclusivement à une activité donnant droit au DIP. Impact TVA net, sous réserve des conditions de déduction ?',o:['CHF 3\\'645 de coût TVA','CHF 0 : CHF 3\\'645 d’impôt sur les acquisitions et DIP correspondant de CHF 3\\'645','CHF 1\\'822,50','Aucun montant à déclarer'],c:1,e:'Une fois la qualification art. 45 établie, CHF 45\\'000 × 8,1% = CHF 3\\'645 sont déclarés. Si les conditions du DIP sont intégralement remplies, le même montant est déductible ; l’impact net est alors nul mais l’obligation déclarative subsiste.'}",
'qcm acquisition arithmetic')

# QCM: accessory parking requires an actual link to the excluded residential letting.
rep(
"q:'La location d\\'une place de parking dans un immeuble residentiel (au sous-sol) a un habitant de l\\'immeuble :'",
"q:'Une place de parc est louée avec l’appartement du même locataire et constitue l’accessoire de cette location résidentielle exclue. Quel traitement ?'",
'qcm accessory parking scenario')

# QCM: scope the surface calculation to a justified key.
rep(
"q:'Immeuble mixte : 300 m2 commercial (option) + 700 m2 residentiel. Travaux communs CHF 50\\'000 HT (TVA CHF 4\\'050). DIP deductible ?'",
"q:'Immeuble mixte : 300 m2 commercial optionné + 700 m2 résidentiel. Pour des travaux réellement communs, la clé de surface est ici documentée et appropriée. TVA CHF 4\\'050 : DIP déductible ?'",
'qcm surface scoped')
rep(
"e:'Cle surface : 300/1000 = 30%. DIP deductible : CHF 4\\'050 x 30% = CHF 1\\'215. DIP perdu (partie residentielle) : CHF 2\\'835.'",
"e:'Dans ce cas où la clé de surface est justifiée : 300/1000 = 30%. DIP déductible sur le coût commun = CHF 4\\'050 × 30% = CHF 1\\'215.'",
'qcm surface explanation')

# QCM: art. 38 - state the test, do not claim an automatic full-value sanction in every failure mode.
rep(
"e:'art. 38 LTVA · Info TVA 11 : art. 38 LTVA = à appliquer si les conditions sont remplies (les deux parties assujetties, rapport TVA indiscutable). Non-respect = TVA sur la totalite du transfert.'",
"e:'La procédure de déclaration doit être examinée et appliquée lorsqu’elle est obligatoire selon l’art. 38. Le dossier doit vérifier les conditions légales, la qualité des parties, l’objet transféré et le formulaire 764 ; les conséquences d’une erreur dépendent du traitement effectivement appliqué.'",
'qcm art38 nuance')

# Flashcard: ATF 145 II 130 concerns prescription recognition, not the conditions of voluntary disclosure under art. 102.
rep(
"{cat:'Restructurations',t:'Denonciation spontanee - immobilier',d:'Signaler spontanement une erreur avant controle annonce peut reduire ou eviter une sanction si les conditions art. 102 sont remplies. Le rappel TVA et les interets selon taux DFF applicable restent dus.',a:'art. 102 LTVA + ATF 145 II 130'}",
"{cat:'Restructurations',t:'Dénonciation spontanée — immobilier',d:'Une correction spontanée peut avoir des effets sur la sanction seulement si les conditions de l’art. 102 LTVA sont effectivement remplies. L’impôt dû et les intérêts applicables ne disparaissent pas pour autant. Vérifier la procédure et les faits avant toute promesse au client.',a:'art. 102 LTVA'}",
'card spontaneous disclosure')

p.write_text(t,encoding='utf-8')
print('M08 legal cleanup 2 changes',sum(n for _,n in changes))
for c in changes: print(' -',c)
