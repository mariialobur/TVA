from pathlib import Path
p=Path('m04-tva-comptabilite-suisse.html')
t=p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label,required=True):
    global t
    n=t.count(old)
    if not n:
        if required: raise RuntimeError('MISSING '+label)
        print('WARN missing',label); return
    t=t.replace(old,new)
    changes.append((label,n))

def section(start,end,new,label):
    global t
    a=t.find(start)
    if a<0: raise RuntimeError('MISSING START '+label)
    b=t.find(end,a)
    if b<0: raise RuntimeError('MISSING END '+label)
    t=t[:a]+new+'\n'+t[b:]
    changes.append((label,1))

# Theory: foreign acquisition tax is based on qualification, not vendor nationality.
rep("""<p>L'acquisition d'un service étranger (AWS, Adobe, Stripe US) génère une <strong>double écriture TVA</strong> : (1) compte 2202 crédité de la impôt sur les acquisitions calculé par le destinataire qui aurait été facturée si le prestataire était suisse (= ch. 383 du décompte). En parallèle, l'impôt préalable peut être déduit via les lignes 400/405 selon la nature de la dépense, si les conditions de l'art. 28 LTVA sont remplies. <strong>Effet net financier souvent nul</strong> pour activité 100% imposable, mais l'<strong>obligation déclarative</strong> reste entière. Voir M03 cas 10 (SaaS Cloud).</p>""",
"""<p>Lorsqu'une prestation étrangère entre dans le champ de l'<strong>impôt sur les acquisitions</strong>, l'entreprise comptabilise la taxe due (ch. 383 dans le décompte actuel) et examine séparément le DIP correspondant selon les art. 28 ss. Il faut d'abord <strong>qualifier la prestation</strong> : le seul fait que le fournisseur soit étranger ne suffit pas, et une prestation exclue ou exonérée ne déclenche pas l'impôt sur les acquisitions. Pour un service cloud/SaaS typique soumis au principe du destinataire, l'écriture miroir présentée ci-dessus illustre la mécanique; les frais financiers ou de paiement doivent être analysés selon leur nature.</p>""",
'acquisition theory qualification')

# CO legal cards: use the actual Swiss statutory framing.
rep('<div class="leg-title">Principe de présentation fidèle (image fidèle)</div>\n<div class="leg-desc">Les comptes doivent présenter une <strong>image fidèle</strong> de la situation économique de l\'entreprise. Tout document comptable trompeur ou incomplet contrevient à l\'art. 958 OR. Application TVA : ventilation correcte des recettes par taux et activité.</div>',
'<div class="leg-title">But de la présentation des comptes</div>\n<div class="leg-desc">L\'art. 958 al. 1 CO exige que les comptes présentent la situation économique de l\'entreprise de façon qu\'un tiers puisse s\'en faire une <strong>opinion fondée</strong>. Application TVA : les soldes, ventilations et rapprochements doivent être compréhensibles et traçables; il ne faut pas transformer cette formulation en concept IFRS de « true and fair view ».</div>',
'art958 legal card')
rep('<div class="leg-title">Principes de l\'établissement des comptes</div>\n<div class="leg-desc">Principes : (1) <strong>continuité d\'exploitation</strong>, (2) <strong>cohérence</strong> dans la présentation et l\'évaluation, (3) <strong>prudence</strong>, (4) <strong>comparabilité</strong> dans le temps et entre entreprises. Application TVA : méthode TVA (effective/TDFN) doit rester cohérente d\'une année à l\'autre.</div>',
'<div class="leg-title">Principe de régularité des comptes</div>\n<div class="leg-desc">L\'art. 958c CO vise notamment la <strong>clarté et l\'intelligibilité</strong>, l\'intégralité, la fiabilité, l\'importance relative, la permanence de la présentation et des méthodes d\'évaluation ainsi que l\'interdiction de compensation. La continuité d\'exploitation relève de l\'art. 958a. Application TVA : documenter les changements comptables ou fiscaux qui modifient la lecture des comptes.</div>',
'art958c legal card')
rep('<div class="leg-desc">L\'évaluation doit être <strong>prudente</strong> mais sans empêcher l\'image fidèle. Pour la TVA : la dette TVA (compte 2200) est évaluée à la <strong>valeur nominale</strong> (montant exact dû) ; la créance TVA (en cas de crédit) à la valeur nominale également.</div>',
'<div class="leg-desc">L\'art. 960 CO encadre l\'évaluation des actifs et dettes, avec une appréciation prudente et vérifiable selon les règles applicables. Pour la TVA, le point pratique est de rapprocher la dette ou créance comptabilisée du montant fiscal effectivement dû ou récupérable, plutôt que de mémoriser une règle d\'évaluation isolée.</div>',
'art960 legal card')

# Control paragraph: avoid presumption of evasion from accounting defects.
rep("""<p>L'AFC <strong>exige la production complète de la comptabilité</strong> lors d'un contrôle TVA : (1) Grand-livre des comptes TVA (2200, 2201, 1170, 1171, etc.), (2) Journaux des ventes et des achats détaillés, (3) Pièces justificatives (factures émises et reçues), (4) Rapprochement décomptes ↔ comptabilité. Une comptabilité non conforme OR = présomption d'erreur ou de soustraction → fixation par voie d’estimation possible (art. 79 LTVA).</p>""",
"""<p>Lors d'un contrôle TVA, l'AFC peut demander les livres, journaux, pièces et rapprochements nécessaires pour vérifier les décomptes. Une comptabilité lacunaire ou non vérifiable n'établit pas automatiquement une soustraction : elle <strong>affaiblit la preuve</strong> et oblige à reconstituer les faits. Si les bases fiscales ne peuvent pas être déterminées de façon fiable, l'art. 79 LTVA permet une fixation par voie d'estimation.</p>""",
'control evidence nuance')

# Concordance theory: anchor the legal deadline to the 180th-day period.
rep("Au-delà de 240 jours sans correction : risque AFC élevé.",
    "Les différences doivent être corrigées selon l'art. 72 dans la période contenant le 180e jour; le repère pratique AFC de 240 jours ne remplace pas cette règle légale.",
    'concordance theory deadline')

# Rebuild Case 5 around gross ch. 200 + separate ch. 235 and correct art. 72 timing.
case5='''<!-- CAS 5 — Concordance annuelle pratique -->
<div class="case-block">
<div class="case-header"><div class="case-num">05</div><div class="case-meta"><div class="case-title">Mode Élégance SA — Concordance annuelle et finalisation</div><div class="case-subtitle">Commerce vêtements · Genève · Clôture 31.12.2025 · 🟡 Risque moyen</div></div></div>
<div class="case-body">
<div class="case-scenario"><strong>Contexte :</strong> Mode Élégance SA, méthode effective selon les contre-prestations convenues. <strong>Données 2025 :</strong><br/>• ventes suisses avant escomptes : <strong>CHF 1'445'000</strong><br/>• escomptes accordés : <strong>CHF 25'000</strong><br/>• ch. 200 cumulé des décomptes : <strong>CHF 1'445'000</strong><br/>• ch. 235 cumulé : <strong>CHF 25'000</strong><br/>• aucune prestation exonérée/exclue dans ce cas</div>
<div class="case-context">📚 <strong>Objectif :</strong> comprendre le rapprochement entre chiffre d'affaires brut, déductions et finalisation art. 72.</div>
<div class="case-step" id="m4c5s1">
<div class="step-question"><span class="step-q-num">Q1</span>Quel contrôle faut-il faire sur le ch. 200 ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m4c5s1',this,false)">A) Le comparer directement au CA après escomptes de CHF 1'420'000</button><button class="step-opt" onclick="caseAnswer('m4c5s1',this,true)">B) Le rapprocher aux contre-prestations avant les déductions : CHF 1'445'000 ↔ CHF 1'445'000</button><button class="step-opt" onclick="caseAnswer('m4c5s1',this,false)">C) Ajouter les escomptes au ch. 200 une seconde fois</button><button class="step-opt" onclick="caseAnswer('m4c5s1',this,false)">D) Ignorer le grand-livre</button></div>
<div class="step-explanation" id="m4c5s1-expl">Le ch. 200 représente le total des contre-prestations avant les déductions du bloc chiffre d'affaires. Ici, le rapprochement brut est <strong>CHF 1'445'000 = CHF 1'445'000</strong>. Si la comptabilité présente des produits directement nets, il faut construire un pont permettant de revenir au montant déclaré au ch. 200. <div class="art-ref">📋 Décompte TVA pro · art. 72 LTVA</div></div>
</div>
<div class="case-step" id="m4c5s2">
<div class="step-question"><span class="step-q-num">Q2</span>Comment contrôler les CHF 25'000 d'escomptes ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m4c5s2',this,false)">A) Les déduire du ch. 200 avant de faire la concordance</button><button class="step-opt" onclick="caseAnswer('m4c5s2',this,true)">B) Les rapprocher séparément au ch. 235; la base après réduction est CHF 1'420'000</button><button class="step-opt" onclick="caseAnswer('m4c5s2',this,false)">C) Les déclarer au ch. 383</button><button class="step-opt" onclick="caseAnswer('m4c5s2',this,false)">D) Les ignorer car ils sont comptables</button></div>
<div class="step-explanation" id="m4c5s2-expl">Les escomptes sont des diminutions ultérieures de la contre-prestation (art. 41) et sont contrôlés séparément dans le bloc des déductions, notamment au ch. 235. Dans ce cas : CHF 1'445'000 − CHF 25'000 = <strong>CHF 1'420'000</strong> de base après réduction. Les deux contrôles — ch. 200 brut et ch. 235 — doivent être cohérents. <div class="art-ref">📋 art. 41 LTVA · ch. 235</div></div>
</div>
<div class="case-step" id="m4c5s3">
<div class="step-question"><span class="step-q-num">Q3</span>Quand une différence constatée lors de la concordance annuelle doit-elle être corrigée ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m4c5s3',this,false)">A) Toujours exactement 240 jours après la clôture</button><button class="step-opt" onclick="caseAnswer('m4c5s3',this,true)">B) Au plus tard dans le décompte de la période pendant laquelle tombe le 180e jour après la fin de l'exercice</button><button class="step-opt" onclick="caseAnswer('m4c5s3',this,false)">C) Seulement lors d'un contrôle AFC</button><button class="step-opt" onclick="caseAnswer('m4c5s3',this,false)">D) Il n'existe aucun délai</button></div>
<div class="step-explanation" id="m4c5s3-expl">C'est la règle de <strong>finalisation de l'art. 72 LTVA</strong>. Le repère pratique de 240 jours utilisé par l'AFC ne doit pas être présenté comme le délai légal unique. Si le rapprochement ne révèle aucune différence, aucun décompte rectificatif annuel n'est requis; le tableau de concordance reste au dossier. <div class="art-ref">📋 art. 72 LTVA · période contenant le 180e jour</div></div>
</div>
<div class="calc-box"><div class="calc-title">📊 Concordance Mode Élégance 2025</div><div class="calc-row"><span class="calc-label">Ch. 200 / ventes avant déductions</span><span class="calc-val">CHF 1'445'000</span></div><div class="calc-row"><span class="calc-label">Ch. 235 / escomptes</span><span class="calc-val">CHF 25'000</span></div><div class="calc-row total"><span class="calc-label">Base après réduction</span><span class="calc-val">CHF 1'420'000</span></div><div class="calc-row highlight"><span class="calc-label">Écart documenté</span><span class="calc-val">CHF 0 ✓</span></div></div>
</div>
</div>'''
section('<!-- CAS 5 — Concordance annuelle pratique -->','<!-- CAS 6 —',case5,'rebuild case5 concordance')

# Error 1 timing and vendor-code language.
rep("Vérifier le paramétrage des codes TVA dans l'ERP (UN1 pour 3000, ESP pour 3200). Reclasser les écritures erronées via journal général. Si correction porte sur exercice clos : <strong>concordance annuelle / décompte rectificatif art. 72</strong> dans les 240 jours.",
    "Vérifier le mapping réel des codes TVA dans l'ERP et reclasser les écritures erronées. Si l'erreur concerne un décompte déjà remis, corriger la période concernée; lors de la finalisation annuelle, respecter l'art. 72 et la période contenant le 180e jour.",
    'error1 correction timing')

# Vocabulary finalisation.
rep('Rapprochement annuel CA TVA déclaré vs CA comptable. concordance annuelle / décompte rectificatif art. 72 dans les 240 jours.',
    'Rapprochement annuel entre comptabilité et décomptes. Les différences sont corrigées selon l’art. 72 au plus tard dans la période contenant le 180e jour; le contrôle est conservé au dossier même si aucun rectificatif n’est requis.',
    'vocab annual reconciliation')

# Cheatsheet: make account numbering explicitly pedagogical.
rep('<div class="cheat-title">3 — Comptes TVA standards</div>', '<div class="cheat-title">3 — Convention de comptes utilisée dans M04</div>', 'cheat account convention')
rep('<p><strong>1171</strong> TVA déductible investissements</p>', '<p><strong>1171</strong> sous-compte investissements <em>(convention possible)</em></p>', 'cheat 1171 convention')

# QCM: account conventions, balance reconciliation, art.106 transition, estimation art.79.
rep("Compte 1170 — TVA déductible (impôt préalable / Vorsteuer). C'est un actif courant représentant une créance envers l'AFC. Solde normalement débiteur. Le compte 1171 est réservé aux investissements (pour la traçabilité art. 32 LTVA — corrections d'affectation).",
    "Dans la convention comptable de M04, le compte 1170 suit le DIP déductible et présente normalement un solde débiteur. Un sous-compte 1171 peut être utilisé pour les investissements afin d'améliorer la traçabilité, mais ce numéro n'est pas imposé par la LTVA.",
    'q07 account convention')

oldq15="""  { id:'m04-q15', diff:'med', art:'compte 2200',
    q:'Au 31.12, le compte 2200 affiche un solde créditeur de CHF 50\\'000. Le décompte Q4 montre TVA collectée Q4 de CHF 20\\'000. Quelle interprétation ?',
    opts:[
      'Normal — montant standard',
      'Anomalie : solde 2200 devrait être ≈ 20\\'000 (TVA Q4 seulement) → enquête nécessaire',
      'Trop bas — TVA non déclarée',
      'Aucune information n\\'est exploitable'
    ],
    correct:1,
    expl:'Anomalie comptable. Au 31.12 (après les écritures de solde Q1-Q3 vers 2201), le compte 2200 devrait refléter uniquement la TVA collectée Q4 (à régulariser au décompte Q4 déposé en février N+1). Solde anormalement élevé = factures probablement non déclarées dans le décompte ou écritures de solde manquantes. Enquête : extraire grand-livre 2200 sur 12 mois, identifier écritures sans contrepartie 2201.'
  },"""
newq15="""  { id:'m04-q15', diff:'med', art:'rapprochement des comptes TVA',
    q:'Au 31.12, un compte technique TVA affiche CHF 50\\'000 alors que le décompte du dernier trimestre suggère CHF 20\\'000. Quel est le bon réflexe ?',
    opts:[
      'Conclure immédiatement à une soustraction',
      'Rapprocher le compte avec périodes ouvertes, écritures de régularisation, paiements/remboursements en transit et décomptes avant de conclure',
      'Forcer le solde à CHF 20\\'000 sans pièce',
      'Ignorer la différence'
    ],
    correct:1,
    expl:'Un solde inhabituel est un signal de rapprochement, pas une règle automatique « le 2200 doit égaler Q4 ». L’organisation comptable peut varier selon l’ERP. Extraire le grand-livre, identifier les périodes et mouvements ouverts et expliquer chaque différence jusqu’au décompte TVA.'
  },"""
rep(oldq15,newq15,'q15 VAT balance')

rep("Le changement de mode exige une transition documentée. Le professionnel identifie les factures et paiements déjà pris en compte sous l’ancien mode, vérifie les règles LTVA/OTVA et la pratique AFC applicables au changement, puis contrôle le premier décompte sous le nouveau mode. M04 n’enseigne pas une « correction d’entrée art. 40 al. 2 » générique.",
    "Le changement de mode exige une transition documentée. Pour la méthode effective, l'art. 106 OTVA règle le passage entre contre-prestations convenues et reçues; le professionnel identifie les débiteurs/créanciers ouverts et contrôle le premier décompte afin d'éviter doubles déclarations ou omissions. L'art. 40 règle ensuite les effets temporels du mode choisi.",
    'q16 art106 precision')

oldq25="""  { id:'m04-q25', diff:'hard', art:'art. 32 LTVA + comptes',
    q:'Pourquoi est-il recommandé de séparer les comptes 1170 (TVA achats courants) et 1171 (TVA investissements) ?',
    opts:[
      'Pour réduire les impôts',
      'Pour gérer les corrections d\\'affectation art. 32 LTVA (20 ans immobilier, 5 ans mobilier) en cas de changement d\\'usage',
      'Pour simplifier le décompte',
      'Sans utilité réelle'
    ],
    correct:1,
    expl:'L\\'art. 32 LTVA prévoit des corrections d\\'affectation sur les biens d\\'investissement quand leur usage change (passage d\\'usage imposable à exclu ou inversement). Période de régularisation : 20 ans pour immobilier, 5 ans pour mobilier. Avoir un compte 1171 distinct facilite radicalement le suivi de chaque acquisition d\\'investissement (date, montant, IP déduit) et permet d\\'appliquer correctement les corrections. Sans cette séparation : tableau de suivi externe lourd et erreurs probables.'
  },"""
newq25="""  { id:'m04-q25', diff:'hard', art:'art. 31-32 LTVA · traçabilité',
    q:'Quel contrôle est indispensable pour les investissements susceptibles de corrections d’affectation ?',
    opts:[
      'Utiliser obligatoirement le numéro de compte 1171',
      'Pouvoir reconstituer par investissement la date, la TVA initiale, le droit au DIP, l’affectation et les changements ultérieurs — via sous-compte ou registre auxiliaire fiable',
      'Conserver seulement le total annuel du compte 1170',
      'Aucun suivi après la première déduction'
    ],
    correct:1,
    expl:'Les art. 31-32 LTVA peuvent imposer des corrections lorsque l’affectation change. La loi n’impose pas un numéro de compte 1171 : l’important est un suivi fiable permettant de reconstituer l’investissement et son historique. Un sous-compte distinct est une option de contrôle interne, pas une condition légale.'
  },"""
rep(oldq25,newq25,'q25 investment tracking')

oldq26="""  { id:'m04-q26', diff:'hard', art:'art. 79 + ATAF A-3098/2020',
    q:'L\\'AFC estime le CA réel à 110% du CA déclaré (taxation d\\'office). Quelle est la base juridique et le recours possible ?',
    opts:[
      'Aucune base — l\\'AFC ne peut pas estimer',
      'Art. 86 al. 2 LTVA + ATAF A-3098/2020. Recours : démontrer que la comptabilité est suffisante OU que l\\'estimation est manifestement excessive. Délai 30 jours réclamation (art. 83 LTVA)',
      'L\\'AFC peut imposer ce qu\\'elle veut sans recours',
      'Recours uniquement après 5 ans'
    ],
    correct:1,
    expl:'Cadre juridique : art. 79 LTVA (taxation d\\'office en cas de comptabilité défaillante) + jurisprudence ATAF A-3098/2020 (l\\'estimation doit reposer sur des éléments objectifs raisonnables). Voies de recours : (1) Réclamation auprès de l\\'AFC dans les 30 jours (art. 83 LTVA), (2) Recours TAF si réclamation rejetée, (3) Recours TF en dernière instance. Stratégie : (a) Prouver que la comptabilité a une force probante suffisante (ATF 138 II 465), (b) Critiquer la méthode d\\'estimation (ratios non comparables, échantillon biaisé), (c) Proposer méthode alternative reconstitutive (CA bancaire, déclarations sociales).'
  },"""
newq26="""  { id:'m04-q26', diff:'hard', art:'art. 79 + art. 83 LTVA',
    q:'Si les bases fiscales ne peuvent pas être établies de façon fiable, sur quelle base l’AFC peut-elle procéder par estimation et quel est le réflexe de défense ?',
    opts:[
      'Art. 86 al. 2 uniquement; aucun recours possible',
      'Art. 79 LTVA; reconstituer les faits, examiner la méthode d’estimation et utiliser les voies de droit/délais indiqués dans l’acte reçu',
      'L’AFC peut fixer n’importe quel montant sans motivation',
      'Attendre cinq ans avant de répondre'
    ],
    correct:1,
    expl:'L’art. 79 LTVA est la base de la fixation par voie d’estimation lorsque les bases ne peuvent pas être déterminées de manière fiable. La défense consiste à reconstituer les pièces et flux, vérifier les comparables/ratios utilisés et contester, si nécessaire, selon la voie de droit et le délai applicables à l’acte de l’AFC (notamment art. 83 pour la réclamation lorsqu’elle est ouverte).'
  },"""
rep(oldq26,newq26,'q26 estimation art79')

# Table wording: consequences are not automatic sanctions.
rep('<th>Sanction si défaut</th>','<th>Conséquence / contrôle à prévoir</th>','cross table consequence heading',required=False)
rep("<tr><td>Tenue d'une comptabilité</td><td class=\"acc-num\">art. 957 OR</td><td class=\"acc-num\">art. 70 al. 1</td><td>Amende OR + fixation par voie d’estimation TVA</td></tr>",
    "<tr><td>Tenue d'une comptabilité</td><td class=\"acc-num\">art. 957 OR</td><td class=\"acc-num\">art. 70 al. 1</td><td>Reconstitution des bases; estimation art. 79 si elles restent indéterminables</td></tr>",
    'cross table accounting consequence',required=False)
rep('<tr><td>Bilan — dettes TVA</td><td class="acc-num">art. 959a OR</td><td>—</td><td>Image faussée</td></tr>',
    '<tr><td>Bilan — position TVA</td><td class="acc-num">art. 959a OR</td><td>—</td><td>Solde à rapprocher et présenter selon sa nature</td></tr>',
    'cross table balance wording',required=False)

p.write_text(t,encoding='utf-8')
print('Applied polish changes:',sum(n for _,n in changes))
for x in changes: print(' -',x)
