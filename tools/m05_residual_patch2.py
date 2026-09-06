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
    t=t.replace(old,new); changes.append((label,n))

def sub(pattern,repl,label,count=0,required=False):
    global t
    t2,n=re.subn(pattern,repl,t,count=count,flags=re.S)
    if not n:
        print('WARN regex missing',label)
        if required: raise SystemExit('missing regex '+label)
        return
    t=t2; changes.append((label,n))

# Case 9: losing the right is art. 31; art. 32 is the reverse (later entitlement).
rep('<div class="case-title">Immeuble Mixte SA — Changement d\'affectation 2026</div>',
    '<div class="case-title">Immeuble Mixte SA — Changement d’affectation : art. 31 puis art. 32</div>','case9 title')
rep('<span class="step-q-num">Q2</span>Quelle est la régularisation due (40% de l\'immeuble passe à l\'exclu) ?',
    '<span class="step-q-num">Q2</span>Quelle correction art. 31 est due si 40% de l’immeuble cesse de donner droit au DIP ?','case9 q2')
rep('<strong>Formule art. 32 al. 3</strong> : Régularisation = IP initial × % passant à l\'exclu × Années restantes / Période totale.',
    '<strong>Art. 31 al. 3</strong> : lorsque les conditions du DIP cessent d’être remplies, la correction porte sur la valeur résiduelle de l’impôt préalable. Pour l’immobilier, cette valeur diminue de 1/20 par année écoulée.','case9 q2 explanation')
rep('<div class="art-ref">📋 art. 32 al. 3 LTVA</div>','<div class="art-ref">📋 art. 31 al. 1–3 LTVA</div>','case9 q2 ref')
rep('<strong>L\'art. 32 est symétrique</strong> : changement d\'affectation dans un sens (imposable→exclu) = régularisation négative ; changement dans l\'autre sens (exclu→imposable) = <strong>dégrèvement ultérieur</strong>.',
    '<strong>Les art. 31 et 32 forment les deux sens du changement</strong> : art. 31 lorsque les conditions du DIP cessent ; art. 32 lorsque les conditions sont remplies ultérieurement et qu’un <strong>dégrèvement ultérieur</strong> devient possible.','case9 symmetry')

# Case 10: remove old-law jurisprudence slogan, distinguish vehicle treatment by legal form, and remove invented global reminder amount.
rep('(3) <strong>CHF 15\'500 d\'IP contestés</strong> : achats sans lien avec activité (frais "représentation" non justifiés — ATF 132 II 353)',
    '(3) <strong>CHF 15\'500 d’IP contestés</strong> : frais de représentation dont l’affectation entrepreneuriale et la réalité doivent être prouvées','case10 scenario proof')
rep('Total rappel envisagé : <strong>CHF 35\'900 + intérêts 4,0% sur 5 ans en moyenne ~ CHF 4\'200</strong>',
    'Montant contesté brut : <strong>CHF 35’900</strong>. Le rappel effectif ne peut être chiffré qu’après analyse point par point ; les intérêts se calculent ensuite selon chaque période et le taux applicable.','case10 scenario amount')
sub(r'<div class="case-step" id="m5c10s2">.*?</div>\n</div>',
'''<div class="case-step" id="m5c10s2">
<div class="step-question"><span class="step-q-num">Q2</span>Point (2) : véhicule d’une SA utilisé à titre privé — quel réflexe avant de calculer un rappel ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c10s2',this,false)">A) Appliquer automatiquement art. 31 / ch. 415</button><button class="step-opt" onclick="caseAnswer('m5c10s2',this,true)">B) Identifier l’utilisateur et la forme juridique : pour une personne morale, la part privée est en principe traitée comme chiffre d’affaires selon la pratique AFC ; reconstituer ensuite forfait ou méthode effective période par période</button><button class="step-opt" onclick="caseAnswer('m5c10s2',this,false)">C) Refuser tout le DIP véhicule</button><button class="step-opt" onclick="caseAnswer('m5c10s2',this,false)">D) Appliquer une amende fixe</button></div>
<div class="step-explanation" id="m5c10s2-expl">PME Consulting est une <strong>SA</strong>. La pratique AFC sur les parts privées distingue la personne morale de l’indépendant : la part privée du collaborateur / détenteur n’est pas traitée automatiquement comme prestation à soi-même au ch. 415. Le dossier doit reconstituer l’usage, la méthode appliquée (forfait 0,9% ou méthode effective si pertinente), les périodes concernées et la rubrique correcte. <div class="art-ref">📋 pratique AFC Parts privées · art. 31 selon situation</div></div>
</div>''','case10 vehicle legal form',count=1,required=True)
sub(r'<div class="case-step" id="m5c10s3">.*?</div>\n</div>',
'''<div class="case-step" id="m5c10s3">
<div class="step-question"><span class="step-q-num">Q3</span>Point (3) : frais de représentation insuffisamment justifiés — quelle défense ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c10s3',this,false)">A) Aucune preuve complémentaire n’est admise</button><button class="step-opt" onclick="caseAnswer('m5c10s3',this,true)">B) Produire un faisceau de preuves : factures détaillées, participants / bénéficiaires, contexte commercial, contrats ou correspondances, paiement et affectation entrepreneuriale</button><button class="step-opt" onclick="caseAnswer('m5c10s3',this,false)">C) Réduire automatiquement le DIP de moitié</button><button class="step-opt" onclick="caseAnswer('m5c10s3',this,false)">D) Recourir directement au Tribunal fédéral</button></div>
<div class="step-explanation" id="m5c10s3-expl"><strong>Défense par la preuve</strong> : l’assujetti doit établir que la dépense existe et relève de son activité entrepreneuriale. L’art. 81 al. 3 consacre la liberté des moyens de preuve : aucune pièce unique n’est exclusive. Un dossier cohérent peut combiner facture, liste de participants, invitation / agenda, contrat, e-mails, paiement et résultat commercial. Une part privée ou non entrepreneuriale reste non déductible. <div class="art-ref">📋 art. 28–30 + art. 81 al. 3 LTVA</div></div>
</div>''','case10 proof current law',count=1,required=True)
rep('B) Demander délai 30j, constituer dossier défense, négocier point par point avec inspecteur, ne pas hésiter à recourir si désaccord persistant',
    'B) Identifier l’acte reçu et son délai, constituer le dossier de preuve, répondre point par point et utiliser la voie de droit appropriée si le désaccord persiste','case10 procedure option')
rep('jurisprudence applicable','bases légales et pratique applicables','case10 procedure sources')

# Case 12: the subsidy cannot be reduced to a universal turnover formula. Rebuild Q2-Q3 accordingly.
sub(r'<div class="case-step" id="m5c12s2">.*?</div>\n</div>\n<div class="case-step" id="m5c12s3">.*?</div>\n</div>',
'''<div class="case-step" id="m5c12s2">
<div class="step-question"><span class="step-q-num">Q2</span>La subvention Innosuisse de CHF 300’000 permet-elle, à elle seule, de calculer la réduction art. 33 ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c12s2',this,false)">A) Oui : 300 / 4’200 = 7,14% dans tous les cas</button><button class="step-opt" onclick="caseAnswer('m5c12s2',this,true)">B) Non : il faut connaître son affectation (projet / domaine / déficit) et identifier les dépenses effectivement financées avant de calculer le ch. 420</button><button class="step-opt" onclick="caseAnswer('m5c12s2',this,false)">C) Oui : appliquer 8,1% à la subvention</button><button class="step-opt" onclick="caseAnswer('m5c12s2',this,false)">D) Les dividendes doivent être ajoutés automatiquement au prorata art. 33</button></div>
<div class="step-explanation" id="m5c12s2-expl">L’art. 75 OTVA impose de regarder l’<strong>imputabilité du financement</strong>. Une subvention de projet peut appeler une réduction sur les dépenses de ce projet ; une contribution couvrant un déficit d’exploitation peut conduire à une clé globale. Les dividendes ne déclenchent pas automatiquement l’art. 33. Sans convention de subvention et ventilation des coûts, le montant du ch. 420 n’est pas défendable. <div class="art-ref">📋 art. 33 LTVA + art. 75 OTVA</div></div>
</div>
<div class="case-step" id="m5c12s3">
<div class="step-question"><span class="step-q-num">Q3</span>Quel livrable professionnel produire avant de calculer le DIP net final ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c12s3',this,false)">A) Une formule unique basée uniquement sur les recettes</button><button class="step-opt" onclick="caseAnswer('m5c12s3',this,true)">B) Un tableau d’affectation : IP direct de la ligne de production, IP commun, dépenses du projet subventionné, prestations étrangères ouvrant droit au DIP, dividendes / participations et note de calcul art. 33</button><button class="step-opt" onclick="caseAnswer('m5c12s3',this,false)">C) Déduire immédiatement CHF 81’000</button><button class="step-opt" onclick="caseAnswer('m5c12s3',this,false)">D) Refuser tout le DIP à cause de la subvention</button></div>
<div class="step-explanation" id="m5c12s3-expl">Le DIP final résulte d’une <strong>chaîne d’affectation</strong>, pas d’un ratio magique. L’investissement directement affecté à une activité donnant droit au DIP est analysé séparément ; les coûts communs sont ventilés selon une méthode appropriée ; le projet financé par la subvention est traité selon art. 33 / art. 75 ; les participations sont analysées selon art. 29. Une fois ces blocs documentés, les ch. 400/405/420 et le solde TVA peuvent être calculés. <div class="art-ref">📋 art. 28–33 LTVA · art. 75 OTVA</div></div>
</div>''','case12 subsidy rebuild',count=1,required=True)
rep('B) Factures + grand-livre + registre biens d\'investissement + calculs prorata art. 33 + convention subvention Innosuisse + documentation comptable groupe',
    'B) Factures + grand-livre + suivi des immobilisations + note d’affectation / calcul art. 33 + convention de subvention Innosuisse + documentation des prestations et participations','case12 docs option')
rep('(3) <strong>Registre des biens d\'investissement</strong> (machine 300\'000) pour application art. 32 sur 5 ans',
    '(3) <strong>Suivi des immobilisations TVA</strong> (machine 300’000) avec IP initial, date et affectation pour les éventuels art. 31–32','case12 docs register')
rep('(4) <strong>Calculs détaillés du prorata art. 33</strong> par période + méthode appliquée',
    '(4) <strong>Note d’imputation art. 33 / art. 75 OTVA</strong> par période : nature du fonds, projet / domaine / déficit, dépenses concernées et méthode appliquée','case12 docs art33')
rep('(8) <strong>Décomptes TVA + concordance 550_03</strong> (ePortal AFC).',
    '(8) <strong>Décomptes TVA et travaux de concordance / corrections</strong> via le Portail AFC, avec les papiers de travail correspondants.','case12 obsolete form')

# Error 1 product wording: no invented risk range and no hard-formalism.
rep('<div class="error-impact">Impact : CHF 500 – 50\'000/an</div>','<div class="error-impact">Impact : DIP contesté si le droit ou la preuve ne sont pas sécurisés</div>','error1 impact')

# q05/q06: remove mnemonic absolutes where option / allocation can matter.
sub(r"\{ id:'m05-q05'.*?\n  \},",'''{ id:'m05-q05', diff:'easy', art:'art. 21 + 22 + 29 LTVA',
    q:'Une dépense est directement affectée à une prestation exclue art. 21 non optée. Quel impact en principe sur le DIP ?',
    opts:['DIP intégral','Pas de DIP pour cette affectation, sous réserve d’une option valable ou d’une règle spéciale','Toujours 50%','Aucun contrôle nécessaire'],
    correct:1,
    expl:'Les coûts directement affectés à des prestations exclues non optées ne donnent en principe pas droit au DIP. Il faut toutefois vérifier si une option art. 22 est possible / exercée et si une règle spéciale modifie l’analyse.'
  },''','q05 nuance',count=1,required=True)
sub(r"\{ id:'m05-q06'.*?\n  \},",'''{ id:'m05-q06', diff:'easy', art:'art. 23 + 28 LTVA',
    q:'Une dépense est affectée à une exportation de biens exonérée art. 23. Quel impact en principe sur le DIP ?',
    opts:['DIP automatiquement perdu','DIP en principe conservé si les conditions, l’affectation et les preuves sont remplies','Toujours 50%','Le DIP dépend uniquement du pays client'],
    correct:1,
    expl:'Une prestation exonérée au sens de l’art. 23 ne doit pas être confondue avec une prestation exclue art. 21. Les coûts affectés à l’exportation peuvent en principe ouvrir droit au DIP, sous réserve des conditions générales et de la preuve.'
  },''','q06 nuance',count=1,required=True)

# q22: scope the 20-year archive rule to real-estate-related documents.
sub(r"\{ id:'m05-q22'.*?\n  \},",'''{ id:'m05-q22', diff:'med', art:'art. 70 LTVA',
    q:'Pourquoi les documents TVA liés à un immeuble peuvent-ils devoir être conservés plus longtemps que les documents ordinaires ?',
    opts:['Parce que toute entreprise immobilière conserve tout à vie','Parce que les corrections / dégrèvements immobiliers peuvent être suivis sur une longue période et les documents commerciaux relatifs à l’immeuble doivent rester disponibles jusqu’à l’expiration du droit de taxer concerné','Parce que le CO impose 50 ans','Aucune différence'],
    correct:1,
    expl:'La durée prolongée vise les documents commerciaux relatifs aux biens immobiliers nécessaires pour défendre les corrections et dégrèvements. Elle ne signifie pas « conserver tout le dossier de toute entreprise immobilière pendant 20 ans ».'
  },''','q22 archive scope',count=1,required=True)

# q35: avoid teaching the current interest rate as a timeless memorized value.
sub(r"\{ id:'m05-q35'.*?\n  \}\n\];",'''{ id:'m05-q35', diff:'hard', art:'art. 86–87 LTVA + ordonnance DFF',
    q:'Un paiement TVA intervient après l’échéance. Quel réflexe professionnel pour les intérêts moratoires ?',
    opts:['Appliquer toujours 5%','Identifier la date d’échéance, le nombre de jours de retard, le taux DFF applicable à la période et le seuil de perception','Ajouter automatiquement 10%','Aucun intérêt en TVA'],
    correct:1,
    expl:'L’art. 87 prévoit l’intérêt moratoire en cas de retard. Le taux est fixé par le DFF et peut évoluer : pour un cas réel, vérifier le taux applicable à la période, les dates exactes et la pratique AFC de perception plutôt que mémoriser un pourcentage comme règle permanente.'
  }
];''','q35 current-rate reflex',count=1,required=True)

# Flashcard fc08 nuance if old absolute remains after residual1.
sub(r"\{ id:'fc08'.*?\},",'''{ id:'fc08', cat:'Double affectation', term:'Art. 21 vs art. 23',
    art:'art. 21–23',
    def:'Art. 21 : prestation exclue, généralement sans DIP sur les coûts affectés si elle n’est pas optée. Art. 23 : prestation exonérée, avec DIP en principe conservé sous réserve des conditions et preuves. Toujours vérifier option et affectation.' },''','fc08 nuance',count=1,required=True)

p.write_text(t,encoding='utf-8')
print('M05 residual2 changes',len(changes))
for c in changes: print(' -',c)
