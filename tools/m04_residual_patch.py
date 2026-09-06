from pathlib import Path

p=Path('m04-tva-comptabilite-suisse.html')
t=p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label):
    global t
    n=t.count(old)
    if not n:
        print('WARN missing',label)
        return
    t=t.replace(old,new)
    changes.append((label,n))

# Accounting examples: keep acquisition tax on its own pedagogical account.
rep('<br/>Cr 2200 TVA due acquisition 162','<br/>Cr 2202 TVA due acquisition 162','acquisition account consistency')

# Cash-flow: no invented universal instalment-plan ceiling.
rep('(3) plan de paiement négocié (max 24 mois), (4) en cas de défaillance prolongée : poursuites + risque de faillite.',
    '(3) éventuel arrangement de paiement à négocier selon le dossier, (4) en cas de défaillance prolongée : poursuites + risque de faillite.',
    'remove universal 24-month ceiling')

# ERP comparison: remove vendor marketing and unsupported compliance claims.
old_erp='''<table class="comp-table">
<thead><tr><th>ERP</th><th>Cible</th><th>Points forts TVA</th><th>Limites</th></tr></thead>
<tbody>
<tr><td><strong>Bexio</strong></td><td>1-50 employés · Cloud</td><td>Décompte TVA généré + export ePortal · Suivi temps réel · UX moderne</td><td>TDFN limité · Complexité bridée</td></tr>
<tr><td><strong>Abacus</strong></td><td>PME 20-500 · Cloud + on-premise</td><td>Gestion mixte complexe · Multi-sociétés · Reporting fiscal avancé</td><td>Setup lourd · Coût élevé</td></tr>
<tr><td><strong>Crésus</strong></td><td>Artisans + indépendants · Desktop CH</td><td>Simplicité · Adapté petites structures · Conformité AFC native</td><td>Pas cloud natif · Moins moderne</td></tr>
<tr><td><strong>Winbiz</strong></td><td>TPE / micro-entreprises</td><td>Très simple · Décompte TVA automatique · Coût faible</td><td>Limite scalabilité · Reporting basique</td></tr>
<tr><td><strong>SAP / Oracle</strong></td><td>Grandes entreprises</td><td>Multi-pays · Multi-devises · Audit trail complet</td><td>Adaptation paramétrage TVA suisse complexe</td></tr>
</tbody>
</table>'''
new_erp='''<table class="comp-table">
<thead><tr><th>Système</th><th>Ce que M04 contrôle</th><th>Preuve attendue</th></tr></thead>
<tbody>
<tr><td><strong>ERP / logiciel PME</strong><br/><span style="font-size:11px;color:var(--muted)">Bexio, Crésus, Winbiz, etc.</span></td><td>Entité, méthode, périodicité, codes TVA, comptes, cut-off</td><td>Paramètres + table de mapping + export de contrôle</td></tr>
<tr><td><strong>ERP intégré</strong><br/><span style="font-size:11px;color:var(--muted)">Abacus, SAP, Oracle, etc.</span></td><td>Interfaces, multi-entités, règles automatiques, exceptions manuelles</td><td>Journal des règles + tests + rapprochement décompte/comptabilité</td></tr>
<tr><td><strong>Solution sur mesure / fichiers</strong></td><td>Traçabilité des transformations de données et contrôles d’intégrité</td><td>Documentation du flux + version des fichiers + piste d’audit</td></tr>
</tbody>
</table>'''
rep(old_erp,new_erp,'neutral ERP table')

# Archiving: only real-estate-related documents get the 20-year rule.
rep('En pratique fiduciaire, conservez tout pendant <strong>20 ans</strong> pour les entreprises avec activité immobilière, <strong>10 ans</strong> pour les autres.',
    'En pratique fiduciaire, appliquez la durée prolongée aux <strong>documents commerciaux liés aux biens immobiliers</strong>; ne transformez pas cette règle en « 20 ans pour tout le dossier » d’une entreprise qui possède simplement un immeuble.',
    'real estate archive scope')
rep('<tr><td>Rapport de gestion + comptes annuels signés</td><td>10 ans</td><td class="art-cell">art. 958f OR</td><td>Papier obligatoire (signature)</td></tr>',
    '<tr><td>Rapport de gestion / rapport de révision lorsqu’applicable</td><td>10 ans</td><td class="art-cell">art. 958f OR</td><td>Conserver dans la forme écrite et signée requise; les livres et pièces peuvent être électroniques selon CO/OLICO</td></tr>',
    'signed reports wording')
rep('En pratique, pour une entreprise avec activité immobilière, conservez TOUT pendant 20 ans pour simplifier la gestion.',
    'La durée de 20 ans vise les <strong>documents commerciaux relatifs aux biens immobiliers</strong>; les autres documents suivent leur propre durée de conservation.',
    'q22 real estate scope')

# Jurisprudence / evidence: remove misattributed case-law claims.
old_j1='''<div class="leg-ref">ATF 140 II 202 — Tribunal fédéral</div>
<div class="leg-title">Concordance annuelle — Effet du délai 240 jours</div>
<div class="leg-desc">Confirme que le délai de 240 jours de l'art. 72 LTVA n'est pas un simple délai d'ordre : au-delà, les décomptes périodiques peuvent être considérés comme définitifs, sauf erreur substantielle pouvant relever de la dénonciation spontanée (art. 102).</div>'''
new_j1='''<div class="leg-ref">ATF 140 II 202 — Tribunal fédéral</div>
<div class="leg-title">Auto-taxation et notification d’estimation</div>
<div class="leg-desc">Cet arrêt est utile pour comprendre la procédure TVA : l’assujetti reste responsable de son auto-taxation et la <strong>notification d’estimation</strong> n’est pas, à elle seule, une décision formelle ordinaire. Il ne doit pas être cité comme source du repère de 240 jours de la concordance annuelle, qui relève de l’art. 72 et de la pratique AFC actuelle.</div>'''
rep(old_j1,new_j1,'correct ATF 140 II 202 topic')

old_j2='''<div class="leg-ref">ATF 123 II 295 — Tribunal fédéral</div>
<div class="leg-title">Principe de neutralité TVA — Fondement</div>
<div class="leg-desc">Arrêt fondateur : la <strong>neutralité TVA est le principe fondateur</strong> du système de TVA suisse. Les écritures comptables doivent permettre de respecter ce principe : la TVA n'est pas une charge pour l'entreprise assujettie (sauf cas exclus art. 21). Toute construction comptable qui dénaturerait la neutralité (ex. : TVA déductible enregistrée en charge) crée un risque de correction, de refus partiel du DIP ou de requalification en cas de contrôle.</div>'''
new_j2='''<div class="leg-ref">Principe de neutralité — logique TVA</div>
<div class="leg-title">TVA déductible vs TVA non déductible</div>
<div class="leg-desc">La TVA <strong>déductible</strong> ne constitue en principe pas une charge définitive pour l’assujetti. En revanche, la TVA qui n’ouvre pas de droit au DIP peut rester dans le coût de la charge ou de l’actif. M04 sépare donc la mécanique comptable de la question juridique du droit à déduction, approfondie en M05.</div>'''
rep(old_j2,new_j2,'neutrality nuance')

old_j3='''<div class="leg-ref">ATF 138 II 465 — Tribunal fédéral</div>
<div class="leg-title">Force probante de la comptabilité</div>
<div class="leg-desc">Une comptabilité conforme aux art. 957a et 958 OR a une <strong>présomption de véracité</strong> que l'AFC doit renverser pour la contester. Inversement, une comptabilité défaillante perd cette force probante et expose à la fixation par voie d’estimation.</div>'''
new_j3='''<div class="leg-ref">Art. 81 al. 3 LTVA · pratique AFC</div>
<div class="leg-title">Liberté et appréciation des moyens de preuve</div>
<div class="leg-desc">La TVA applique la <strong>liberté des moyens de preuve</strong> : un fait ne doit pas dépendre exclusivement d’un document unique. Une comptabilité régulière, des pièces et une piste d’audit cohérente renforcent la preuve; si les bases ne peuvent pas être établies de manière fiable, l’art. 79 permet une fixation par voie d’estimation.</div>'''
rep(old_j3,new_j3,'evidence freedom card')

# Case 8: no universal subsidy prorata. Direct allocation and appropriate method come first.
start=t.find('<div class="case-step" id="m4c8s2">')
end=t.find('</div>\n</div>\n</div>\n<!-- Niveau 3', start)
if start!=-1 and end!=-1:
    end += len('</div>\n</div>\n</div>')
    new_case8='''<div class="case-step" id="m4c8s2">
<div class="step-question"><span class="step-q-num">Q2</span>Comment déterminer la réduction du DIP liée à la subvention ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c8s2',this,false)">A) Toujours subvention / (subvention + chiffre d’affaires)</button>
<button class="step-opt" onclick="caseAnswer('m4c8s2',this,true)">B) Identifier d’abord l’affectation de la subvention et les coûts concernés; appliquer ensuite la méthode appropriée à la nature du financement</button>
<button class="step-opt" onclick="caseAnswer('m4c8s2',this,false)">C) Toujours 100% du DIP</button>
<button class="step-opt" onclick="caseAnswer('m4c8s2',this,false)">D) Aucune réduction n’est jamais requise</button>
</div>
<div class="step-explanation" id="m4c8s2-expl">L’art. 33 LTVA impose une réduction du DIP en présence de subventions, mais <strong>il n’existe pas une clé universelle applicable à toutes les subventions</strong>. Il faut d’abord savoir si la contribution finance un objet, un domaine d’activité, un déficit d’exploitation ou une autre situation. Une affectation directe aux coûts concernés prime lorsqu’elle est possible; une clé globale n’est utilisée que lorsqu’elle donne un résultat approprié selon la pratique AFC. <div class="art-ref">📋 art. 33 LTVA · pratique AFC Subventions / DIP</div></div>
</div>
<div class="case-step" id="m4c8s3">
<div class="step-question"><span class="step-q-num">Q3</span>L’activité de formation exclue art. 21 doit-elle aussi être prise en compte pour le DIP ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c8s3',this,false)">A) Non — la subvention absorbe toutes les autres corrections</button>
<button class="step-opt" onclick="caseAnswer('m4c8s3',this,true)">B) Oui — affecter d’abord directement les coûts, puis répartir les coûts communs selon une clé objective; traiter séparément la réduction liée à la subvention</button>
<button class="step-opt" onclick="caseAnswer('m4c8s3',this,false)">C) Oui — appliquer automatiquement CA imposable / CA total à tout le DIP</button>
<button class="step-opt" onclick="caseAnswer('m4c8s3',this,false)">D) Tout le DIP devient déductible</button>
</div>
<div class="step-explanation" id="m4c8s3-expl">L’art. 30 et l’art. 33 répondent à deux questions différentes. Pour l’activité mixte, on commence par l’<strong>affectation directe</strong> des dépenses; seuls les coûts communs nécessitent une clé objective. La subvention fait ensuite l’objet de sa propre analyse de réduction du DIP. Le résultat ne peut donc pas être calculé correctement à partir des seuls quatre montants de chiffre d’affaires donnés dans ce mini-cas. Le calcul détaillé et le choix de la clé sont approfondis en M05. <div class="art-ref">📋 art. 30 + 33 LTVA · M05</div></div>
</div>
<div class="calc-box"><div class="calc-title">📊 Ordre de travail — FormaPlus</div><div class="calc-row"><span class="calc-label">1. Qualifier les activités</span><span class="calc-val">imposable / exclue</span></div><div class="calc-row"><span class="calc-label">2. Affecter les coûts directs</span><span class="calc-val">avant tout prorata</span></div><div class="calc-row"><span class="calc-label">3. Répartir les coûts communs</span><span class="calc-val">clé objective documentée</span></div><div class="calc-row"><span class="calc-label">4. Analyser la subvention</span><span class="calc-val">objet / domaine / déficit / autre</span></div><div class="calc-row total"><span class="calc-label">5. Reporter la réduction admissible</span><span class="calc-val">ch. 420 selon calcul documenté</span></div></div>
</div>
</div>
</div>'''
    t=t[:start]+new_case8+t[end:]
    changes.append(('rebuild case 8 subsidy logic',1))
else:
    print('WARN missing case8 boundaries')

# Case 10: art. 79, no impossible spontaneous disclosure after control has been announced.
rep('B) Oui — art. 79 LTVA : comptabilité non vérifiable = fixation par voie d’estimation par estimation',
    'B) Oui — art. 79 LTVA : si les bases ne peuvent pas être établies de manière fiable, l’AFC peut procéder à une fixation par voie d’estimation',
    'case10 q1 answer')
rep('<strong>Art. 86 al. 2 LTVA</strong> : si les éléments transmis sont manifestement incomplets ou que les résultats sont en désaccord avec les faits, l\'AFC procède à une <strong>fixation par voie d’estimation</strong>.',
    '<strong>Art. 79 LTVA</strong> : si les documents comptables font défaut, sont incomplets ou que les résultats ne correspondent manifestement pas à la réalité, l’AFC peut procéder à une <strong>fixation par voie d’estimation</strong>.',
    'case10 art79 explanation')
rep('B) Reconstitution maximale (banque, fournisseurs, RC, déclarations sociales) + déclaration force majeure + négociation extrapolation modérée + dénonciation spontanée art. 102 si erreurs identifiées',
    'B) Reconstitution maximale (banque, fournisseurs, caisse, déclarations sociales) + dossier du sinistre + coopération documentée + critique motivée de la méthode d’estimation si nécessaire',
    'case10 strategy option')
old_strat='''<strong>Stratégie de défense professionnelle :</strong> (1) <strong>Reconstitution maximale</strong> par sources tierces — extraits bancaires complets sur 12 mois, listings fournisseurs (demandes de duplicatas factures), comptes annuels signés par fiduciaire 2022, déclarations TVA cantonales et fédérales archivées, déclarations AVS/LPP (cohérence CA/masse salariale), Z détaillés des caisses récupérables. (2) <strong>Dossier force majeure</strong> — déclaration sinistre assurance (avec n° dossier), rapport d'expert, photos datées, témoignages, attestation police s'il y a eu intervention. Ce dossier doit être présenté <strong>spontanément à l'inspecteur AFC dès le début</strong> du contrôle pour bénéficier de la clémence administrative. (3) <strong>Négociation</strong> avec l'inspecteur AFC pour limiter l'extrapolation : proposer une méthode alternative (CA bancaire vérifié). (4) <strong>Dénonciation spontanée</strong> art. 102 à envisager uniquement si les conditions sont réunies et avant tout contrôle annoncé ; l’exemption d’amende n’est pas automatique sans analyse. (5) <strong>Réclamation</strong> 30j contre la décision si nécessaire (art. 83 LTVA).'''
new_strat='''<strong>Stratégie de défense professionnelle :</strong> (1) <strong>Reconstitution maximale</strong> par sources tierces — banque, duplicatas fournisseurs, données de caisse, ERP, comptes annuels et autres archives fiables. (2) <strong>Dossier du sinistre</strong> — déclaration d’assurance, rapport d’expert, photos et éléments datés afin d’expliquer la perte documentaire sans prétendre qu’elle supprime l’obligation de conservation. (3) <strong>Coopération et preuve</strong> — fournir une reconstitution structurée et, si l’AFC estime les bases, examiner les comparables, hypothèses et marges retenues; proposer une méthode alternative mieux étayée si nécessaire. (4) <strong>Procédure</strong> — distinguer correction fiscale, éventuel risque pénal et voies de droit. Dans ce cas, le contrôle est déjà annoncé : on ne présente donc pas la dénonciation spontanée comme une solution automatique. (5) <strong>Réclamation</strong> dans le délai légal contre une décision contestée, le cas échéant.'''
rep(old_strat,new_strat,'case10 strategy explanation')
rep('📋 art. 83 + 102 LTVA + stratégie fiduciaire','📋 art. 79 + 81 + 83 LTVA · stratégie de preuve','case10 strategy ref')

# Case 11: acquisition tax is not triggered merely because the supplier is foreign.
old_q11='''<div class="case-step" id="m4c11s2">
<div class="step-question"><span class="step-q-num">Q2</span>Pour les achats étrangers (AWS, Stripe, Notion) : quel traitement ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">A) Pas de TVA — fournisseurs étrangers</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,true)">B) Auto-imposition art. 45 LTVA : (96'000 + 24'000 + 6'000) × 8,1% = CHF 10'206 au ch. 383 + ch. 400/405 (IP selon nature) — effet net 0 mais déclaration obligatoire</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">C) TVA à 8,1% à payer aux fournisseurs étrangers</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">D) Auto-imposition uniquement si &gt; CHF 100'000</button>
</div>
<div class="step-explanation" id="m4c11s2-expl">
<strong>Auto-imposition art. 45 LTVA</strong> systématique pour tous les services achetés à l'étranger : AWS (cloud), Stripe (services bancaires intermédiaires), Notion (SaaS). Total HT = CHF 126'000. TVA auto-imposée = 126'000 × 8,1% = <strong>CHF 10'206</strong> à déclarer au ch. 383 ET au ch. 400/405 (IP selon nature, activité 100% générant DIP — exonérés art. 23 conservent le DIP). Effet net souvent nul si le DIP est intégralement admis, mais déclaration <strong>obligatoire</strong>. En cas d’omission, la qualification pénale dépend de l’avantage fiscal, de la faute et des circonstances du dossier.
            <div class="art-ref">📋 art. 45 LTVA + analyse art. 96 selon circonstances</div>
</div>
</div>'''
new_q11='''<div class="case-step" id="m4c11s2">
<div class="step-question"><span class="step-q-num">Q2</span>Pour les achats étrangers (AWS, Stripe, Notion) : quel traitement ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">A) Pas de TVA dès que le fournisseur est étranger</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,true)">B) Qualifier chaque prestation : AWS/Notion relèvent typiquement du principe du destinataire et peuvent générer l’impôt sur les acquisitions; les frais Stripe doivent être analysés selon leur nature avant de les inclure</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">C) Auto-imposer automatiquement les CHF 126'000 à 8,1% sans qualifier les services</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">D) L’impôt sur les acquisitions n’existe qu’au-delà de CHF 100'000</button>
</div>
<div class="step-explanation" id="m4c11s2-expl">L’art. 45 ne signifie pas « fournisseur étranger = acquisition tax ». Il faut déterminer la <strong>nature de la prestation</strong>, son lieu et vérifier qu’elle n’est ni exclue ni exonérée. Les prestations cloud/SaaS régies par le principe du destinataire sont des cas typiques; les frais d’un prestataire de paiement doivent être ventilés selon la prestation réellement fournie. CloudWare étant déjà inscrite au registre TVA, le seuil de CHF 10'000 applicable aux destinataires non inscrits n’est pas le test du cas. Le DIP correspondant ne se déduit que dans la mesure où les conditions de l’art. 28 ss sont remplies. <div class="art-ref">📋 art. 45 LTVA · Info TVA 14 · M05/M06</div></div>
</div>'''
rep(old_q11,new_q11,'case11 acquisition qualification')
rep('B) Oui — 100% déductible. Toutes les activités (Suisse 8,1% + exports UE/USA art. 23) génèrent le DIP. Pas de prorata.',
    'B) En principe oui si les dépenses servent aux prestations suisses imposables et aux prestations étrangères qui ouvriraient le droit au DIP; vérifier l’affectation réelle et l’art. 29 pour les prestations étrangères',
    'case11 DIP option')
rep('<strong>Toutes les activités</strong> de CloudWare ouvrent le droit au DIP : ventes Suisse imposables 8,1% + ventes UE/USA hors champ suisse (art. 8 al. 1) mais qui seraient imposables si fournies en Suisse. Il n’y a donc <strong>pas de prorata de DIP</strong> sur le bureau commun. Loyer + IT local : IP déductible intégralement sous réserve des conditions générales de l’art. 28. <strong>Ne pas confondre</strong> hors champ géographique avec prestations exclues art. 21.',
    '<strong>Les prestations étrangères ne font pas perdre automatiquement le DIP.</strong> Pour les prestations qui seraient imposables si elles étaient fournies en Suisse, le droit au DIP peut être conservé selon les règles applicables, notamment l’art. 29. Il faut toutefois vérifier l’affectation réelle des dépenses et l’absence d’activité exclue/non entrepreneuriale. Le cas illustre donc un contrôle d’affectation, pas une règle « étranger = 100% DIP ».',
    'case11 DIP explanation')

# Quiz: remove remaining incorrect shortcuts.
old_q14="""  { id:'m04-q14', diff:'med', art:'art. 72 LTVA',
    q:'CA TVA déclaré annuel CHF 1\\'500\\'000. CA comptable brut CHF 1\\'525\\'000. Escomptes accordés CHF 25\\'000. Y a-t-il un écart de concordance ?',
    opts:[
      'Oui — CHF 25\\'000',
      'Non — concordance parfaite (1\\'525 − 25 escomptes = 1\\'500 = CA TVA déclaré)',
      'Oui — CHF 50\\'000',
      'Impossible à dire'
    ],
    correct:1,
    expl:'Concordance correcte. CA comptable NET = CA brut − Escomptes accordés (3800) = 1\\'525\\'000 − 25\\'000 = CHF 1\\'500\\'000 = CA TVA déclaré. Écart = 0. Les escomptes sont des réducteurs de contre-prestation (art. 41 LTVA), inscrits au ch. 235 du décompte. La concordance est parfaite, signal vert AFC.'
  },"""
new_q14="""  { id:'m04-q14', diff:'med', art:'art. 72 LTVA · décompte',
    q:'Le ch. 200 cumulé est CHF 1\\'525\\'000 et les escomptes accordés sont CHF 25\\'000. Quel contrôle est correct ?',
    opts:[
      'Comparer directement ch. 200 au CA net après escomptes et exiger toujours zéro',
      'Rapprocher le ch. 200 aux contre-prestations à déclarer en brut, puis contrôler séparément les réductions de contre-prestation au ch. 235 et documenter le pont comptable',
      'Ajouter les acquisitions ch. 383 au chiffre d’affaires',
      'Ignorer les escomptes'
    ],
    correct:1,
    expl:'La concordance doit expliquer le passage entre comptabilité et décompte. Le ch. 200 représente le total des contre-prestations à déclarer avant les déductions du bloc chiffre d’affaires; les réductions de contre-prestation sont ensuite contrôlées séparément, notamment au ch. 235. Si la comptabilité présente les produits nets, un pont documenté est nécessaire au lieu d’une comparaison simpliste.'
  },"""
rep(old_q14,new_q14,'q14 concordance logic')

old_q16="""  { id:'m04-q16', diff:'med', art:'art. 39-40 LTVA',
    q:'Lors du passage méthode convenue → encaissement au 01.01.2026, factures clients ouvertes CHF 200\\'000. Que faire ?',
    opts:[
      'Aucune action — encaisser normalement',
      'Correction d\\'entrée art. 40 al. 2 : TVA déjà déclarée 2025 ne doit pas être redéclarée à l\\'encaissement 2026',
      'Annuler les factures 2025',
      'Émettre de nouvelles factures'
    ],
    correct:1,
    expl:'Correction d\\'entrée obligatoire pour éviter une double imposition. Les factures émises en 2025 ont déjà été déclarées en méthode convenue (à l\\'émission). Lors de l\\'encaissement en 2026 (méthode encaissement), la TVA ne doit pas être redéclarée. Documentation rigoureuse exigée par l\\'AFC : liste détaillée des créances ouvertes au 01.01 avec mention "TVA déjà déclarée 2025".'
  },"""
new_q16="""  { id:'m04-q16', diff:'med', art:'art. 39–40 LTVA · transition',
    q:'Lors d’un changement du décompte selon contre-prestations convenues vers reçues, quel est le bon réflexe comptable ?',
    opts:[
      'Ne rien documenter; le logiciel corrigera forcément tout seul',
      'Établir la liste des créances/dettes ouvertes à la date de bascule et appliquer les règles de transition de la période afin d’éviter doubles déclarations ou omissions',
      'Annuler toutes les factures ouvertes',
      'Déclarer une seconde fois la TVA lors de l’encaissement'
    ],
    correct:1,
    expl:'Le changement de mode exige une transition documentée. Le professionnel identifie les factures et paiements déjà pris en compte sous l’ancien mode, vérifie les règles LTVA/OTVA et la pratique AFC applicables au changement, puis contrôle le premier décompte sous le nouveau mode. M04 n’enseigne pas une « correction d’entrée art. 40 al. 2 » générique.'
  },"""
rep(old_q16,new_q16,'q16 transition')

old_q17="""  { id:'m04-q17', diff:'med', art:'art. 33 LTVA',
    q:'Subvention hors champ CHF 100\\'000, CA imposable CHF 500\\'000. Prorata de réduction DIP (art. 33) ?',
    opts:[
      '20%',
      '16,67% = 100 / (100 + 500)',
      '50%',
      'Pas de réduction'
    ],
    correct:1,
    expl:'Art. 33 LTVA : la subvention hors champ réduit le DIP par prorata. Formule : Subvention / (Subvention + CA total générant DIP) = 100\\'000 / (100\\'000 + 500\\'000) = 16,67%. L\\'IP commun est réduit de ce pourcentage et inscrit au ch. 420 du décompte. Attention : article spécifique aux subventions, distinct de l\\'art. 30 (corrections d\\'affectation activités exclues).'
  },"""
new_q17="""  { id:'m04-q17', diff:'med', art:'art. 33 LTVA · pratique AFC',
    q:'Une entreprise reçoit une subvention de CHF 100\\'000. Quelle information manque avant de calculer la réduction du DIP ?',
    opts:[
      'Aucune : la formule 100 / (100 + CA) est toujours obligatoire',
      'L’affectation de la subvention et des dépenses concernées (objet, domaine, déficit d’exploitation, autres coûts) afin de choisir une méthode appropriée',
      'Uniquement le numéro de compte bancaire',
      'La couleur du justificatif'
    ],
    correct:1,
    expl:'L’art. 33 entraîne une réduction du DIP, mais la méthode dépend de l’affectation. Une contribution directement attribuable à un objet ou domaine doit être traitée sur les coûts concernés; une clé globale n’est utilisée que lorsqu’elle est appropriée. Le ch. 420 reçoit la réduction calculée et documentée.'
  },"""
rep(old_q17,new_q17,'q17 subsidy')

rep("expl:'Art. 86 al. 2 LTVA : en cas de pièces manquantes ou comptabilité non vérifiable, l\\'AFC procède à une taxation d\\'office par estimation (ratios de branche, méthode comparative). La force majeure (incendie, dégât) atténue mais n\\'élimine pas l\\'obligation d\\'archivage sécurisé (art. 70 LTVA — obligation de moyens). Stratégie de défense : reconstitution maximale par sources tierces (banque, fournisseurs, déclarations sociales).'",
    "expl:'Art. 79 LTVA : si les documents comptables font défaut, sont incomplets ou que les résultats ne correspondent manifestement pas à la réalité, l’AFC peut fixer la créance par voie d’estimation. La stratégie consiste à reconstituer les bases avec des preuves fiables et à discuter la méthode d’estimation sur des éléments objectifs.'",
    'q23 art79')

old_q27="""  { id:'m04-q27', diff:'hard', art:'art. 33 + 30 LTVA cumulés',
    q:'Activité mixte : CA imposable 200, CA exclu 300, subvention 100. IP brut 50. Calcul DIP net ?',
    opts:[
      'CHF 50 (intégral)',
      'CHF 16 ≈ 50 × (200/500) × (1 − 100/600). Cumul art. 30 (prorata imposable/total) ET art. 33 (réduction subvention) sur IP commun',
      'CHF 25 (50%)',
      'CHF 0'
    ],
    correct:1,
    expl:'Application cumulative art. 30 + 33 LTVA. Étape 1 (art. 30) : IP commun réduit par prorata CA imposable / CA total = 200 / 500 = 40%. IP après art. 30 = 50 × 40% = 20. Étape 2 (art. 33) : Réduction subvention = Subv / (Subv + CA total générant DIP) = 100 / (100 + 500) = 16,67%. IP final = 20 × (1 − 16,67%) = 20 × 83,33% = CHF 16,67 ≈ CHF 17. L\\'option B annonce 16 — arrondi acceptable. Logique : les deux corrections sont cumulatives car elles couvrent des dimensions distinctes (activité vs financement public).'
  },"""
new_q27="""  { id:'m04-q27', diff:'hard', art:'art. 30 + 33 LTVA',
    q:'Activité mixte + subvention : quel ordre d’analyse du DIP est professionnel ?',
    opts:[
      'Appliquer automatiquement deux pourcentages calculés uniquement sur les chiffres d’affaires',
      'Affecter les dépenses directement quand c’est possible, répartir les coûts communs selon une clé objective, puis traiter la réduction liée à la subvention selon son affectation et la pratique applicable',
      'Refuser tout le DIP',
      'Déduire tout le DIP'
    ],
    correct:1,
    expl:'Les art. 30 et 33 peuvent tous deux intervenir, mais ils ne créent pas une formule universelle en cascade. La qualité du calcul dépend de l’affectation directe, de la clé retenue pour les coûts communs et de la nature du financement public. Toute clé doit être documentée et appropriée au dossier.'
  },"""
rep(old_q27,new_q27,'q27 subsidy/activity mix')

old_q28="""  { id:'m04-q28', diff:'hard', art:'art. 78 + 68 LTVA',
    q:'Lors d\\'un contrôle TVA, l\\'AFC demande l\\'accès lecture à l\\'ERP avec extraction des journaux. Le contribuable peut-il refuser ?',
    opts:[
      'Oui — secret commercial',
      'Non — art. 78 + 68 LTVA imposent la coopération. Refus = présomption de soustraction + taxation d\\'office (art. 79). Stratégie : préparer extraits Excel structurés AVANT pour limiter l\\'accès direct',
      'Oui — uniquement sur autorisation judiciaire',
      'Cela dépend de la taille de l\\'entreprise'
    ],
    correct:1,
    expl:'Art. 78 LTVA donne à l\\'AFC un large pouvoir de contrôle ; art. 68 LTVA impose l\\'obligation de renseignement à l\\'assujetti. Le refus d\\'accès = (1) Présomption négative défavorable, (2) Taxation d\\'office probable (art. 79), (3) Amende art. 98 LTVA possible. Bonne pratique fiduciaire : (a) Préparer les extraits ERP structurés en amont (journaux ventes, achats, grand-livre des comptes TVA), (b) Limiter l\\'accès direct au personnel ERP, (c) Présenter le dossier de manière organisée. La coopération maîtrisée permet de garder le contrôle de la narration tout en respectant les obligations légales.'
  },"""
new_q28="""  { id:'m04-q28', diff:'hard', art:'art. 68 + 78 LTVA',
    q:'Lors d’un contrôle TVA, l’AFC demande les données détaillées de l’ERP. Quel est le bon réflexe ?',
    opts:[
      'Refuser toute donnée au titre du secret commercial',
      'Coopérer et fournir les informations/documents nécessaires sous une forme exploitable; coordonner la modalité technique (exports, lecture seule ou accès encadré) selon le contrôle',
      'Donner systématiquement les mots de passe administrateur',
      'Envoyer uniquement le bilan'
    ],
    correct:1,
    expl:'Les art. 68 et 78 imposent la collaboration et permettent le contrôle. Ils ne créent pas pour autant une règle universelle « accès direct illimité à l’ERP ». La priorité est une piste d’audit exploitable et complète. Si les bases restent insuffisantes, l’art. 79 peut devenir pertinent.'
  },"""
rep(old_q28,new_q28,'q28 ERP access')

old_q29="""  { id:'m04-q29', diff:'hard', art:'OLICO + art. 958f OR',
    q:'Une PME archive ses factures en PDF sur Google Drive partagé entre 3 personnes. Conformité OLICO ?',
    opts:[
      'Conforme — c\\'est un cloud',
      'NON conforme à OLICO : manque (a) intégrité garantie (modifications possibles), (b) traçabilité des accès, (c) horodatage certifié. Risque : force probante contestée → taxation d\\'office',
      'Conforme si les PDFs sont signés',
      'Question non pertinente'
    ],
    correct:1,
    expl:'OLICO (RS 221.431) exige 4 conditions cumulatives : (1) <strong>Intégrité</strong> — système empêchant les modifications après archivage (Google Drive permet modification donc défaillant), (2) <strong>Disponibilité</strong> pendant 10 ans (OK si Google Workspace payant), (3) <strong>Lisibilité</strong> assurée (PDF/A recommandé, pas PDF standard), (4) <strong>Traçabilité</strong> des accès et modifications. Solutions conformes : Bexio Document, Abacus Cloud, Adcubum, DocBoxQ. En cas de contrôle AFC : un archivage non conforme = force probante contestée (ATF 138 II 465) → taxation d\\'office possible.'
  },"""
new_q29="""  { id:'m04-q29', diff:'hard', art:'OLICO + art. 958f CO',
    q:'Une PME archive ses factures dans un cloud partagé. Peut-on conclure à la conformité OLICO uniquement à partir du nom du fournisseur ?',
    opts:[
      'Oui — tout cloud est conforme',
      'Non — il faut vérifier le dispositif concret : organisation, intégrité/traçabilité adaptée au support, disponibilité, lisibilité et possibilité de reconstituer la piste d’audit',
      'Oui uniquement si les fichiers sont PDF/A',
      'Non — le stockage électronique est interdit'
    ],
    correct:1,
    expl:'L’OLICO admet des supports modifiables et non modifiables sous conditions. La conformité dépend des mesures techniques et organisationnelles et de la vérifiabilité, pas de la marque du service ni d’un format de fichier unique. La piste d’audit doit rester reconstituable pendant la durée de conservation.'
  },"""
rep(old_q29,new_q29,'q29 OLICO')

old_q30="""  { id:'m04-q30', diff:'hard', art:'art. 961a-b OR + 39 LTVA',
    q:'Une SA passe de TDFN à effective au 01.01.2026. Quelles obligations comptables ?',
    opts:[
      'Aucune obligation particulière',
      'Mentionner le changement en annexe aux comptes (art. 961a OR — méthodes appliquées), documenter la correction d\\'entrée (art. 32 LTVA + 81 OTVA, 3 ans min. en effective avant retour TDFN), conserver justification interne',
      'Republier 5 ans de comptes',
      'Demander autorisation TF'
    ],
    correct:1,
    expl:'Obligations cumulatives : (1) <strong>Annexe aux comptes</strong> (art. 961a OR) — mention du changement de méthode et son impact chiffré. Exemple : "À compter du 01.01.2026, la société applique la méthode effective au lieu de la TDFN. Cette modification a entraîné une correction d\\'entrée de CHF X au 01.01.2026 (art. 32 LTVA)." (2) <strong>Correction d\\'entrée</strong> (art. 32 LTVA + 81 OTVA) — recalcul des stocks et investissements pour récupérer/restituer la TVA selon la nouvelle méthode. (3) <strong>Engagement minimum</strong> : 1 an en TDFN avant passage à effective (art. 79 OTVA) · 3 ans en effective avant retour à TDFN (art. 81 OTVA). (4) <strong>Documentation interne</strong> — note justifiant le choix (motivation économique). (5) <strong>Principe de comparabilité</strong> (art. 958c OR) — les comparaisons N vs N-1 doivent être expliquées.'
  }"""
new_q30="""  { id:'m04-q30', diff:'hard', art:'TDFN → effective · pratique AFC 2025+',
    q:'Une SA passe valablement de TDFN à la méthode effective. Quel dossier comptable faut-il préparer ?',
    opts:[
      'Aucun dossier particulier',
      'Documenter la date et l’autorisation/modalité du changement, inventorier les biens/services à valeur résiduelle, déterminer le dégrèvement ultérieur admissible et rapprocher le premier décompte effectif; mention en annexe seulement si les règles comptables l’exigent ou si l’information est significative',
      'Appliquer automatiquement 8,1% à tout le stock',
      'Attendre trois ans avant toute correction'
    ],
    correct:1,
    expl:'Depuis 2025, le passage TDFN → effective entraîne une analyse de la valeur résiduelle et peut ouvrir un dégrèvement ultérieur porté dans le premier décompte effectif, actuellement au ch. 410. Le changement est possible au plus tôt après une période fiscale complète sous réserve des conditions/délais applicables. La comptabilité doit conserver l’inventaire et les pièces permettant le calcul; une annexe aux comptes n’est pas automatiquement imposée par le seul changement TVA.'
  }"""
rep(old_q30,new_q30,'q30 TDFN transition')

# Flashcards / vocab / cheatsheet residuals.
rep("{ id:'fc04', cat:'Cadre légal', term:'OR art. 958 — Image fidèle',\n    art:'art. 958 OR',\n    def:'Les comptes doivent présenter une image fidèle (true and fair view) de la situation économique. Standard suisse impératif. Toute écriture trompeuse ou incomplète viole l\\'art. 958.' },",
    "{ id:'fc04', cat:'Cadre légal', term:'OR art. 958 — Objectif des comptes',\n    art:'art. 958 OR',\n    def:'Les comptes annuels doivent présenter la situation économique de façon qu’un tiers puisse s’en faire une opinion fondée. Ne pas traduire automatiquement cette formule par le concept IFRS « true and fair view ».' },",
    'fc04 art958')
rep("def:'4 conditions cumulatives : intégrité garantie, disponibilité 10 ans, lisibilité (PDF/A), traçabilité accès. Non conforme = force probante perdue (ATF 138 II 465) = taxation d\\'office possible.' },",
    "def:'La conservation électronique doit rester vérifiable, lisible et disponible; des supports modifiables ou non modifiables sont possibles sous conditions OLICO. La conformité dépend des mesures techniques/organisationnelles, pas d’un format ou fournisseur unique.' },",
    'fc14 OLICO')
rep('<div class="vc-art">art. 40 LTVA</div>\n<div class="vc-use">TVA due à l\'encaissement effectif. Avantage cash-flow pour DSO long. Demande AFC requise.</div>',
    '<div class="vc-art">art. 39 LTVA · effets art. 40</div>\n<div class="vc-use">Mode de décompte selon les contre-prestations reçues : choix encadré par l’art. 39; l’art. 40 règle la naissance de la créance fiscale. À documenter dans la comptabilité.</div>',
    'vocab received method')
rep('<p><strong>Comptabilité obligatoire</strong> : CA &gt; CHF 500\'000 (art. 957 OR)</p>',
    '<p><strong>Comptabilité complète</strong> : personnes morales selon CO; entreprises individuelles/sociétés de personnes selon seuils de l’art. 957. Ne pas appliquer « 500’000 » à toutes les formes juridiques.</p>',
    'cheat accounting scope')
rep('<p><strong>OR 958</strong> Image fidèle</p>',
    '<p><strong>OR 958</strong> Objectif : permettre une opinion fondée sur la situation économique</p>',
    'cheat art958')
rep('<p><strong>LTVA 96-99</strong> Sanctions (simple/qualifiée/escroquerie)</p>',
    '<p><strong>LTVA 96-99</strong> Droit pénal TVA — qualification détaillée en M11</p>',
    'cheat penal label')
rep('<p><strong>Soustraction qualifiée</strong> : avec intention/répétition (art. 97)</p>',
    '<p><strong>Art. 97</strong> : fixation de la peine / circonstances prévues par la loi — analyse détaillée en M11</p>',
    'cheat art97')
rep("def:'10 ans pour livres et pièces (art. 958f OR + art. 70 al. 2 LTVA). Pour pièces immobilières : \"jusqu\\'à expiration du droit de taxer\" = 20 ans en pratique (art. 70 al. 3 LTVA). Format papier ou électronique OLICO. Comptes signés + rapport de gestion = papier obligatoire.' },",
    "def:'10 ans en principe pour livres/pièces selon CO et jusqu’à la prescription absolue selon LTVA; documents commerciaux relatifs aux biens immobiliers : 20 ans. Livres/pièces peuvent être électroniques selon CO/OLICO; les documents soumis à une exigence de forme écrite/signée se conservent dans la forme requise.' },",
    'fc03 archiving')

# Plan-account vocabulary: practical standard, never official law.
rep('Liste structurée des comptes utilisés. Standard PME suisse : classe 1 actifs, 2 passifs, 3 produits, 4-6 charges.',
    'Liste structurée des comptes utilisés. Les classes et numéros présentés sont une convention pratique courante; le CO exige surtout une comptabilité claire, complète et traçable.',
    'vocab chart accounts')

p.write_text(t,encoding='utf-8')
print('Residual changes:',len(changes))
for x in changes: print(' -',x)
