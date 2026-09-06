from pathlib import Path
import re
p=Path('m05-deduction-impot-prealable-dip.html')
t=p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label,required=False):
    global t
    n=t.count(old)
    if not n:
        print('WARN missing',label)
        if required: raise SystemExit('missing '+label)
        return
    t=t.replace(old,new)
    changes.append((label,n))

def sub(pattern,repl,label,count=0,required=False):
    global t
    t2,n=re.subn(pattern,repl,t,count=count,flags=re.S)
    if not n:
        print('WARN regex missing',label)
        if required: raise SystemExit('missing regex '+label)
        return
    t=t2; changes.append((label,n))

# Progress must become 100% after explicit completion.
rep("  const pct=Math.round(done/total*100);","  const pct=state.completed?100:Math.round(done/total*100);",'completion progress',True)

# Q07 import proof: remove legacy e-dec-specific wording.
rep("Justificatif : quittance e-dec OFDF (Office fédéral de la douane et de la sécurité des frontières, anciennement AFD).",
    "Justificatif : décision / quittance OFDF ou preuve électronique disponible dans le système douanier applicable.",
    'q07 import proof')

# Q15 — vehicle private share must depend on legal form.
sub(r"\{ id:'m05-q15'.*?\n  \},",'''{ id:'m05-q15', diff:'med', art:'art. 31 + pratique AFC Parts privées',
    q:'Véhicule d’entreprise utilisé à titre privé : quelle question vient AVANT le calcul du forfait 0,9% ?',
    opts:['Le taux de TVA du carburant','La forme juridique et le statut de l’utilisateur : indépendant / raison individuelle ou collaborateur-détenteur d’une personne morale','Le canton du garage','La couleur du véhicule'],
    correct:1,
    expl:'La pratique AFC distingue la correction / prestation à soi-même chez l’indépendant et la part privée déclarée comme chiffre d’affaires chez une personne morale. Le forfait de 0,9% est applicable en TVA depuis 2022, mais on ne peut pas envoyer automatiquement tout véhicule privé au ch. 415.'
  },''','q15 legal form vehicle',count=1,required=True)

# Q16 — loss of deduction belongs to art.31; make elapsed years explicit.
sub(r"\{ id:'m05-q16'.*?\n  \},",'''{ id:'m05-q16', diff:'med', art:'art. 31 LTVA',
    q:'Machine : IP initial CHF 8’100. Après deux années complètes d’utilisation donnant droit au DIP, elle est définitivement affectée à une activité exclue. Quelle correction sur valeur résiduelle ?',
    opts:['CHF 8’100','CHF 4’860 (= 8’100 × 3/5)','CHF 3’240','CHF 0'],
    correct:1,
    expl:'Lorsque les conditions du DIP cessent d’être remplies, l’art. 31 s’applique. Pour un bien mobilier, l’IP est réduit de 1/5 par année écoulée. Après deux années complètes, la valeur résiduelle est 3/5 : CHF 4’860. Le ch. 415 accueille la correction correspondante.'
  },''','q16 art31 residual',count=1,required=True)

# Q17 — subsidy allocation, no universal ratio.
sub(r"\{ id:'m05-q17'.*?\n  \},",'''{ id:'m05-q17', diff:'med', art:'art. 33 LTVA + art. 75 OTVA',
    q:'Subvention CHF 100k + CA imposable CHF 400k + IP total CHF 32’400 : peut-on calculer immédiatement la réduction art. 33 ?',
    opts:['Oui : 20% dans tous les cas','Non : il faut d’abord connaître l’affectation de la subvention et des dépenses concernées','Oui : CHF 32’400 intégralement','Aucune réduction n’existe jamais'],
    correct:1,
    expl:'L’art. 75 OTVA distingue notamment le financement d’un domaine déterminé et la couverture d’un déficit d’exploitation. Les trois montants ne suffisent pas à eux seuls pour choisir la méthode et la base de réduction. Le calcul doit suivre l’imputabilité réelle et être documenté au ch. 420.'
  },''','q17 subsidy allocation',count=1,required=True)

# Flashcards — align every memory anchor with the audited theory.
sub(r"\{ id:'fc01'.*?\},",'''{ id:'fc01', cat:'Principe DIP', term:'DIP (Déduction de l’impôt préalable)',
    art:'art. 28 LTVA',
    def:'Droit de l’assujetti de déduire certains impôts préalables dans le cadre de son activité entrepreneuriale, sous réserve notamment des art. 29 et 33. Toujours distinguer existence de l’IP, droit matériel, affectation et preuve.' },''','fc01',count=1,required=True)
sub(r"\{ id:'fc03'.*?\},",'''{ id:'fc03', cat:'Principe DIP', term:'Fardeau de la preuve',
    art:'art. 81 al. 3 LTVA',
    def:'La preuve du DIP n’est pas enfermée dans un document unique. L’AFC apprécie l’ensemble des moyens de preuve, mais l’assujetti supporte les conséquences d’une preuve insuffisante pour un fait qui diminue l’impôt.' },''','fc03',count=1,required=True)
sub(r"\{ id:'fc04'.*?\},",'''{ id:'fc04', cat:'Conditions', term:'Test professionnel DIP',
    art:'art. 26, 28–30, 33, 40, 81',
    def:'1) source de l’impôt ; 2) activité / affectation ; 3) exclusions ou réductions ; 4) moment du droit ; 5) preuve. Une facture conforme aide à prouver le dossier mais ne remplace pas les conditions matérielles.' },''','fc04',count=1,required=True)
sub(r"\{ id:'fc05'.*?\},",'''{ id:'fc05', cat:'Conditions', term:'Ticket de caisse — simplification',
    art:'art. 26 al. 3 LTVA',
    def:'Jusqu’au seuil réglementaire, le destinataire peut ne pas être mentionné sur un ticket de caisse. Cette simplification de facturation ne supprime pas le droit matériel ni le fardeau de la preuve du DIP.' },''','fc05',count=1,required=True)
sub(r"\{ id:'fc06'.*?\},",'''{ id:'fc06', cat:'Double affectation', term:'Art. 30 LTVA',
    art:'art. 30 + OTVA 65–68',
    def:'L’IP est corrigé en proportion de l’utilisation. Pour les coûts communs, choisir une méthode appropriée et documentée : utilisation effective, méthode forfaitaire AFC ou calcul propre économiquement compréhensible.' },''','fc06',count=1,required=True)
sub(r"\{ id:'fc07'.*?\},",'''{ id:'fc07', cat:'Double affectation', term:'Clé de chiffre d’affaires',
    art:'art. 30 + OTVA 65–68',
    def:'Le chiffre d’affaires est une clé possible, pas une règle universelle. Il faut vérifier qu’il reflète effectivement l’utilisation des prestations préalables communes et tester sa plausibilité.' },''','fc07',count=1,required=True)
sub(r"\{ id:'fc09'.*?\},",'''{ id:'fc09', cat:'Subventions', term:'Art. 33 — Fonds réducteurs',
    art:'art. 33 LTVA + art. 75 OTVA',
    def:'Seuls certains fonds de l’art. 18 al. 2 let. a à c entraînent une réduction. La méthode dépend de leur affectation : domaine / objet déterminé, domaine sans DIP ou couverture d’un déficit d’exploitation. Pas de prorata universel.' },''','fc09',count=1,required=True)
sub(r"\{ id:'fc11'.*?\},",'''{ id:'fc11', cat:'Soi-même', term:'Véhicule — part privée',
    art:'art. 31 + pratique AFC Parts privées',
    def:'Avant le calcul, distinguer raison individuelle / indépendant et personne morale. Le forfait 0,9% est applicable en TVA depuis 2022, mais la qualification de la part privée et sa rubrique de décompte dépendent notamment de la forme juridique.' },''','fc11',count=1,required=True)
sub(r"\{ id:'fc13'.*?\},",'''{ id:'fc13', cat:'Soi-même', term:'Fin d’assujettissement',
    art:'art. 31 al. 2 let. d',
    def:'Lorsque l’assujettissement cesse, analyser les biens et prestations encore disponibles dont le DIP a été déduit. Si les conditions cessent, la correction se calcule selon la valeur résiduelle de l’art. 31; ne pas remplacer ce calcul par une formule comptable improvisée.' },''','fc13',count=1,required=True)
sub(r"\{ id:'fc14'.*?\},",'''{ id:'fc14', cat:'Art. 32', term:'Valeur résiduelle',
    art:'art. 31 al. 3 / 32 al. 2',
    def:'Réduction linéaire de l’IP par année écoulée : 1/5 pour biens mobiliers et prestations de services, 1/20 pour biens immobiliers. L’amortissement comptable ne détermine pas la valeur TVA.' },''','fc14',count=1,required=True)
sub(r"\{ id:'fc15'.*?\},",'''{ id:'fc15', cat:'Art. 32', term:'Art. 31 vs art. 32',
    art:'art. 31–32 LTVA',
    def:'Art. 31 : les conditions du DIP cessent → correction / prestation à soi-même. Art. 32 : les conditions sont remplies plus tard → dégrèvement ultérieur. Dans les deux cas, suivre la valeur résiduelle lorsque le bien/service a déjà été utilisé.' },''','fc15',count=1,required=True)
sub(r"\{ id:'fc16'.*?\},",'''{ id:'fc16', cat:'Art. 32', term:'Dégrèvement ultérieur',
    art:'art. 32 LTVA',
    def:'Si le droit au DIP apparaît ultérieurement, la part encore résiduelle peut être déduite. En immobilier, vérifier aussi les conditions de l’option et l’affectation effective avant tout calcul.' },''','fc16',count=1,required=True)
sub(r"\{ id:'fc18'.*?\}\n\];",'''{ id:'fc18', cat:'Méthodes', term:'Contre-prestations reçues',
    art:'art. 39–40 LTVA',
    def:'Sur autorisation AFC : TVA due à l’encaissement et DIP né au paiement. Le mode choisi s’applique pendant au moins une période fiscale. Les transitions doivent être documentées pour éviter doubles déclarations ou omissions.' }
];''','fc18',count=1,required=True)

# Error 1 prevention: do not hard-block a deductible fact solely because VAT number is missing.
rep('(2) Configuration ERP : <strong>blocage automatique</strong> si N° TVA manquant.',
    '(2) Configuration ERP : <strong>alerte</strong> si le statut / N° TVA du fournisseur est manquant ou incohérent, avec contrôle avant déduction.',
    'error1 ERP alert')
rep('(4) Refus pré-paiement de toute facture non conforme — exiger rectification immédiate.',
    '(4) Demander une facture rectifiée lorsque nécessaire et conserver les preuves complémentaires ; ne pas faire dépendre le DIP d’un seul document.',
    'error1 proof')

# Error 2: no invented turnover ratio / old case-law slogan.
sub(r'<div class="error-block">\n<div class="error-head">\n<div class="error-num">02</div>.*?<!-- Erreur 3 -->',
'''<div class="error-block">
<div class="error-head"><div class="error-num">02</div><div class="error-title">Double affectation traitée avec une clé automatique</div><div class="error-impact">Impact : correction du DIP potentiellement significative</div></div>
<div class="error-body"><div class="error-section"><span class="error-section-title">Mécanisme</span><div class="error-text">Une entreprise mixte déduit 100% des coûts communs ou applique mécaniquement un prorata de chiffre d’affaires sans vérifier si la clé reflète l’utilisation réelle.</div></div><div class="error-section"><span class="error-section-title">Conséquences</span><div class="error-text">L’AFC peut corriger le DIP si la méthode ne conduit pas à un résultat approprié. L’impact dépend des coûts concernés, des périodes ouvertes et de la clé finalement défendable ; M05 n’utilise pas une fourchette chiffrée inventée comme « risque type ».</div></div><div class="error-section"><span class="error-section-title">Prévention</span><div class="error-text">Affecter directement les dépenses lorsque possible, isoler les coûts réellement communs, choisir une méthode conforme aux art. 65–68 OTVA et documenter le test de plausibilité.</div></div></div>
</div>
<!-- Erreur 3 -->''','error2 rebuild',count=1,required=True)

# Error 3 subsidy — art75 allocation, no rigid five-year/example amount.
sub(r'<div class="error-block">\n<div class="error-head">\n<div class="error-num">03</div>.*?<!-- Erreur 4 -->',
'''<div class="error-block">
<div class="error-head"><div class="error-num">03</div><div class="error-title">Subvention identifiée mais mal imputée au DIP</div><div class="error-impact">Impact : ch. 420 incorrect</div></div>
<div class="error-body"><div class="error-section"><span class="error-section-title">Mécanisme</span><div class="error-text">Le fonds public est correctement classé hors contre-prestation mais la réduction art. 33 est soit oubliée, soit calculée avec une clé universelle sans examiner l’objet, le domaine financé ou la couverture d’un déficit.</div></div><div class="error-section"><span class="error-section-title">Conséquences</span><div class="error-text">Le DIP peut être sur- ou sous-déduit. La correction doit être reconstruite période par période selon les faits et l’art. 75 OTVA; intérêts et procédure sont ensuite analysés séparément.</div></div><div class="error-section"><span class="error-section-title">Prévention</span><div class="error-text">Conserver décision / convention de subvention, identifier les coûts financés, distinguer domaine sans DIP / domaine déterminé / déficit d’exploitation et archiver la note de calcul ch. 420.</div></div></div>
</div>
<!-- Erreur 4 -->''','error3 rebuild',count=1,required=True)

# Error 4 vehicle — legal form first.
sub(r'<div class="error-block">\n<div class="error-head">\n<div class="error-num">04</div>.*?<!-- Erreur 5 -->',
'''<div class="error-block">
<div class="error-head"><div class="error-num">04</div><div class="error-title">Part privée véhicule traitée sans distinguer la forme juridique</div><div class="error-impact">Impact : mauvaise rubrique / mauvais mécanisme TVA</div></div>
<div class="error-body"><div class="error-section"><span class="error-section-title">Mécanisme</span><div class="error-text">Le cabinet applique automatiquement art. 31 et ch. 415 à toute voiture de société, ou inversement traite toute utilisation privée comme chiffre d’affaires.</div></div><div class="error-section"><span class="error-section-title">Conséquences</span><div class="error-text">La pratique AFC distingue notamment l’indépendant / raison individuelle et la personne morale. Une mauvaise qualification peut produire une déclaration TVA incohérente même si le forfait de 0,9% a été calculé correctement.</div></div><div class="error-section"><span class="error-section-title">Prévention</span><div class="error-text">Identifier la forme juridique, l’utilisateur, le mode de calcul (forfait ou effectif) et la rubrique TVA applicable; documenter la cohérence avec la paie / part privée lorsqu’une personne morale est concernée.</div></div></div>
</div>
<!-- Erreur 5 -->''','error4 rebuild',count=1,required=True)

# Error 6 — negative change is art31, positive change art32; register not a statutory template.
sub(r'<div class="error-block">\n<div class="error-head">\n<div class="error-num">06</div>.*?<!-- Erreur 7 -->',
'''<div class="error-block">
<div class="error-head"><div class="error-num">06</div><div class="error-title">Art. 31 et art. 32 inversés lors d’un changement d’usage</div><div class="error-impact">Impact : correction / dégrèvement mal calculé</div></div>
<div class="error-body"><div class="error-section"><span class="error-section-title">Mécanisme</span><div class="error-text">Le droit au DIP cesse mais le dossier applique art. 32, ou le droit apparaît plus tard mais le dossier traite l’opération comme prestation à soi-même. Autre erreur : utiliser l’amortissement comptable au lieu de la valeur résiduelle TVA.</div></div><div class="error-section"><span class="error-section-title">Conséquences</span><div class="error-text">Art. 31 = correction lorsque les conditions cessent; art. 32 = dégrèvement ultérieur lorsqu’elles sont remplies plus tard. La valeur résiduelle diminue de 1/5 par année pour mobilier/services et de 1/20 pour immobilier.</div></div><div class="error-section"><span class="error-section-title">Prévention</span><div class="error-text">Tenir un suivi des immobilisations / prestations significatives avec IP initial, date, affectation et années écoulées. Un registre structuré est une bonne pratique de preuve, mais la loi n’impose pas un modèle Excel unique.</div></div></div>
</div>
<!-- Erreur 7 -->''','error6 rebuild',count=1,required=True)

# Error 7 — no market-value shortcut for all assets at deregistration.
sub(r'<div class="error-block">\n<div class="error-head">\n<div class="error-num">07</div>.*?<!-- Erreur 8 -->',
'''<div class="error-block">
<div class="error-head"><div class="error-num">07</div><div class="error-title">Fin d’assujettissement — actifs résiduels non analysés</div><div class="error-impact">Impact : correction art. 31 omise</div></div>
<div class="error-body"><div class="error-section"><span class="error-section-title">Mécanisme</span><div class="error-text">À la fin de l’assujettissement, l’entreprise conserve des biens ou prestations sur lesquels un DIP a été déduit, sans examiner si les conditions cessent au sens de l’art. 31 al. 2 let. d.</div></div><div class="error-section"><span class="error-section-title">Conséquences</span><div class="error-text">La correction dépend du DIP initial et, lorsque le bien / service a déjà été utilisé, de sa valeur résiduelle TVA selon art. 31 al. 3. Il faut éviter les raccourcis « valeur comptable × taux » ou « valeur de marché × taux » appliqués indistinctement à tous les actifs.</div></div><div class="error-section"><span class="error-section-title">Prévention</span><div class="error-text">Inventorier stocks, biens et prestations encore disponibles, retrouver le DIP initial, documenter les années d’utilisation et préparer le calcul final avec les justificatifs correspondants.</div></div></div>
</div>
<!-- Erreur 8 -->''','error7 rebuild',count=1,required=True)

# Error 8 — remove invented monetary range and stale generic annex requirement.
rep('<div class="error-impact">Impact : CHF 10\'000 – 50\'000 + rejet méthode</div>',
    '<div class="error-impact">Impact : méthode / valeur résiduelle / premier décompte incohérents</div>','error8 impact')
rep('Recalcul intégral du DIP sur la période concernée avec différence parfois substantielle. Pour une entreprise passée prématurément de TDFN à effective : <strong>perte de l\'avantage</strong> du changement (10\'000-30\'000/an récupération DIP indue) + risque procédural à analyser pour fausse déclaration. <strong>Rétroactif sur toute la période</strong> de changement non autorisé.',
    'Un changement mal daté ou mal documenté peut affecter la méthode applicable, les corrections sur valeur résiduelle et le premier décompte sous la nouvelle méthode. Quantifier l’effet sur les faits du dossier au lieu d’utiliser une fourchette de risque générique.',
    'error8 consequence')

# Cheat: wording of the art.30 card if the old formula survived in another shape.
rep('<p><strong>Prorata = CA imposable (+ exonéré art. 23) / CA total</strong></p>',
    '<p><strong>Clé possible</strong> : chiffre d’affaires si elle reflète correctement l’utilisation des coûts communs ; sinon surfaces, heures, unités ou autre méthode appropriée.</p>',
    'cheat art30 residual')

# General terminology and visible pedagogy.
rep('Calibration examen professionnel','Validation interne du module','quiz title wording')
rep('niveau examen TVA spécialiste','niveau attendu dans ce module de formation','quiz intro wording')
rep('Vous maîtrisez le DIP au niveau attendu pour la évaluation TVA professionnelle. Continuez avec le M06 (Territorialité) pour approfondir.',
    'Vous avez atteint le seuil interne de M05. Continuez avec M06 — Territorialité & TVA internationale. Cette validation de module n’est pas un diplôme officiel.',
    'quiz result wording')

p.write_text(t,encoding='utf-8')
print('Residual M05 changes',len(changes))
for c in changes: print(' -',c)
