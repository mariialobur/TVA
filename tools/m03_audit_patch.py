from pathlib import Path
import re

p = Path('m03-decomptes-methodes-tva.html')
t = p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label,count=0):
    global t
    n=t.count(old)
    if not n:
        print('WARN missing:',label)
        return
    t=t.replace(old,new,count if count else n)
    changes.append(f'{label}:{min(n,count) if count else n}')

def sub(pattern,repl,label,count=1):
    global t
    t2,n=re.subn(pattern,repl,t,count=count,flags=re.S)
    if not n:
        print('WARN regex missing:',label)
        return
    t=t2
    changes.append(f'{label}:{n}')

# Version + author
rep('<span class="sidebar-version">v4.6</span>','<span class="sidebar-version">v5.0</span>','sidebar version',1)
rep('<span class="version-badge">v4.8 — Contrôle final</span>','<span class="version-badge">M03 v5.0</span>','topbar version',1)
footer='<a class="btn-home" href="index.html">← Retour au cours</a>'
author=footer+'<div style="font-size:10.5px;text-align:center;margin-top:8px;line-height:1.6"><a href="https://www.linkedin.com/in/mariia-lobur/" target="_blank" rel="noopener noreferrer" style="color:var(--gold);text-decoration:none">Mariia Lobur · LinkedIn ↗</a><br/><a href="https://github.com/mariialobur" target="_blank" rel="noopener noreferrer" style="color:rgba(255,255,255,.55);text-decoration:none">GitHub ↗</a></div>'
rep(footer,author,'author credit',1)

marker='<!-- BLOC 1 — Méthode effective -->'
objectives='''<div class="theory-block" style="border-left:3px solid var(--gold)">
<h3><span class="num">✓</span>Objectifs de M03 — livrable professionnel</h3>
<p class="prose">À l’issue de M03, l’étudiant doit pouvoir <strong>transformer une qualification M02 en décompte exploitable</strong> : choisir la méthode de décompte admise, déterminer la période et le mode convenu/reçu, reporter les flux dans le décompte électronique en vigueur, rapprocher le décompte avec la comptabilité et préparer une correction documentée lorsqu’un écart est découvert.</p>
<div class="box warning"><div class="box-icon">🧭</div><div class="box-body"><div class="box-title">Règle de sécurité — le formulaire n’est pas la loi</div>Les numéros de chiffres et l’interface ePortal sont des <strong>outils opérationnels susceptibles d’évoluer</strong>. M03 mémorise la logique et les chiffres usuels, mais pour un dossier réel le praticien contrôle toujours le libellé affiché dans le décompte AFC de la période concernée. M05 reste propriétaire des méthodes détaillées de répartition du DIP; M06 de la territorialité; M11 de la procédure de contrôle et du pénal.</div></div>
</div>
'''
if marker in t and 'Objectifs de M03 — livrable professionnel' not in t:
    t=t.replace(marker,objectives+marker,1); changes.append('objectives/scope:1')

# Effective method
rep('Cette méthode est <strong>obligatoire</strong> pour : (1) les assujettis dépassant les seuils TDFN (CA &gt; CHF 5\'024\'000 ou impôt dû &gt; CHF 108\'000), (2) les contribuables avec activités complexes/mixtes, (3) les contribuables ayant déjà eu recours à la méthode forfaitaire et qui doivent y rester pendant 3 ans avant de revenir au TDFN.',
    'La méthode effective est la méthode de référence lorsque l’assujetti ne remplit pas les conditions d’une méthode simplifiée, n’en a pas fait le choix valable ou y renonce. <strong>Une activité mixte ou complexe n’impose pas, à elle seule, la méthode effective</strong> : il faut vérifier l’éligibilité TDFN/TaF et les règles applicables aux activités multiples.',
    'effective mandatory nuance',1)
rep('<tr><td>Activités mixtes</td><td>Obligatoire (calcul prorata IP)</td><td class="art-cell">art. 30 LTVA</td></tr>',
    '<tr><td>Activités mixtes</td><td>Possible; la méthode de décompte ne remplace jamais la qualification des flux et l’analyse du DIP</td><td class="art-cell">art. 29–30 LTVA</td></tr>',
    'mixed activities',1)
sub(r'<div class="box info">\n<div class="box-icon">🧮</div>\n<div class="box-body">\n<div class="box-title">Formule de calcul méthode effective</div>.*?</div>\n</div>',
    '''<div class="box info">
<div class="box-icon">🧮</div>
<div class="box-body">
<div class="box-title">Formule de calcul — méthode effective</div>
<p><strong>Impôt dû sur les opérations + impôt sur les acquisitions − DIP déductible après corrections/réductions = solde du décompte.</strong> Les chiffres 303/313/343/383 et 400/405/410/415/420 sont des repères usuels du décompte actuel, mais le calcul doit suivre les libellés et signes effectivement affichés dans ePortal pour la période. Ne jamais reconstruire un solde uniquement depuis un ancien mémo.</p>
</div>
</div>''','effective formula',1)
sub(r'<div class="box warning">\n<div class="box-icon">⚠️</div>\n<div class="box-body">\n<div class="box-title">Piège fréquent — Mauvais arrondi de la TVA collectée</div>.*?</div>\n</div>',
    '''<div class="box warning">
<div class="box-icon">⚠️</div>
<div class="box-body">
<div class="box-title">Piège fréquent — Écarts d’arrondi et de paramétrage</div>
<p>La comptabilité, les factures et le décompte doivent utiliser une méthode d’arrondi cohérente et documentée. Un écart entre le livre des ventes et le décompte n’est pas couvert par une « tolérance de quelques francs » automatique : il faut pouvoir expliquer l’arrondi, les notes de crédit, les écritures de période et les changements de taux.</p>
</div>
</div>''','rounding nuance',1)

# TDFN
rep('<p class="prose">La <strong>méthode TDFN</strong> (art. 37 LTVA) permet de simplifier le décompte en appliquant un <strong>taux forfaitaire par branche</strong> au CA brut TTC. Ce taux forfaitaire (de 0,1% à 6,8% selon la branche) est calibré par l\'AFC (RS 641.202.62) pour intégrer l\'IP moyen du secteur. <strong>Conséquence : pas de déduction séparée de l\'IP</strong> — il est déjà inclus dans le taux. Le calcul devient : CA brut TTC × taux TDFN = TVA nette due.</p>',
    '<p class="prose">La <strong>méthode TDFN</strong> (art. 37 LTVA) simplifie le décompte en appliquant au chiffre d’affaires déterminant, TVA comprise, le ou les <strong>taux attribués aux activités réellement exercées</strong>. Le taux ne se choisit pas librement dans une table ancienne : il faut utiliser la classification et la pratique AFC en vigueur. Le DIP n’est pas déduit séparément comme en méthode effective, car il est pris en compte forfaitairement dans le mécanisme TDFN.</p>',
    'tdfn theory',1)
sub(r'<h4 style="font-size:14px;color:var\(--navy\);margin:18px 0 8px;font-weight:600">Exemples de taux TDFN par branche.*?</table>',
    '''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Déterminer le taux TDFN — méthode praticienne</h4>
<table class="comp-table">
<thead><tr><th>Étape</th><th>Réflexe professionnel</th></tr></thead>
<tbody>
<tr><td>1. Cartographier les activités</td><td>Partir des prestations réellement fournies, pas du seul objet social ou du libellé comptable.</td></tr>
<tr><td>2. Vérifier l’éligibilité</td><td>Contrôler les seuils et exclusions de la méthode pour la période fiscale concernée.</td></tr>
<tr><td>3. Attribuer le ou les taux</td><td>Utiliser la liste / pratique AFC actuelle. Depuis la réforme 2025, plusieurs activités peuvent conduire à plusieurs taux; la règle de matérialité doit être appliquée selon la pratique en vigueur.</td></tr>
<tr><td>4. Séparer les chiffres d’affaires</td><td>La comptabilité doit permettre de reconstituer le CA soumis à chaque taux TDFN.</td></tr>
<tr><td>5. Documenter</td><td>Conserver la décision d’attribution, la description des activités et les contrôles effectués.</td></tr>
</tbody>
</table>''','replace tdfn rate table',1)
rep('<tr><td>Renoncement TDFN</td><td>Possible mais 3 ans civils en effective avant retour</td><td class="art-cell">art. 81 OTVA</td></tr>',
    '<tr><td>Changement de méthode</td><td>Respecter les délais et conditions de changement applicables à la période; ne pas mémoriser une durée depuis une ancienne version</td><td class="art-cell">art. 37 LTVA + OTVA / pratique AFC</td></tr>',
    'tdfn change duration',1)
sub(r'<div class="box danger">\n<div class="box-icon">🚨</div>\n<div class="box-body">\n<div class="box-title">Piège critique — Dépassement de seuil en cours d\'année</div>.*?</div>\n</div>',
    '''<div class="box danger">
<div class="box-icon">🚨</div>
<div class="box-body">
<div class="box-title">Piège critique — Dépassement d’un seuil TDFN</div>
<p>Un dépassement de seuil impose de vérifier immédiatement les règles de sortie de la méthode pour la période fiscale concernée et d’informer l’AFC dans le délai applicable. <strong>Ne pas enseigner une récupération automatique de DIP sur les stocks via l’art. 32</strong> : les conséquences d’un changement de méthode relèvent des règles spécifiques TDFN/OTVA et de la pratique AFC en vigueur. Inventaire, immobilisations et date d’effet doivent être documentés avant toute écriture de transition.</p>
</div>
</div>''','tdfn threshold transition',1)

# TaF
rep('Différences principales avec TDFN : (1) <strong>pas de plafond</strong> de CA ni de dette fiscale, (2) <strong>plusieurs taux possibles</strong> selon les activités et la pratique applicable, (3) <strong>périodicité semestrielle</strong> standard, (4) destinée aux <strong>structures sans but lucratif</strong> où la simplification administrative est essentielle.',
    'Différences principales avec TDFN : l’accès dépend de la <strong>catégorie d’assujetti admise par l’art. 37 al. 5 et la pratique AFC</strong>; plusieurs taux peuvent être nécessaires selon les activités; la méthode n’autorise pas à traiter indistinctement toutes les NPO comme éligibles. La période de décompte doit être déterminée selon l’art. 35 applicable à la méthode — ne pas transposer automatiquement le semestre TDFN.',
    'taf scope/period',1)
rep('<tr><td>Nombre de taux</td><td>1 ou 2 max.</td><td>Jusqu\'à 3 taux</td></tr>','<tr><td>Nombre de taux</td><td>Plusieurs taux possibles selon les activités et la pratique actuelle</td><td>Plusieurs taux possibles selon l’attribution applicable</td></tr>','taf/tdfn rates',1)
rep('<tr><td>Périodicité</td><td>Semestrielle</td><td>Semestrielle</td></tr>','<tr><td>Périodicité</td><td>Semestrielle en TDFN</td><td>Déterminée selon l’art. 35 / pratique applicable; ne pas supposer « semestrielle »</td></tr>','taf periodicity table',1)
sub(r'<div class="box info">\n<div class="box-icon">📋</div>\n<div class="box-body">\n<div class="box-title">Périodicité semestrielle pour TDFN et TaF</div>.*?</div>\n</div>',
    '''<div class="box info">
<div class="box-icon">📋</div>
<div class="box-body">
<div class="box-title">Périodicité — ne pas confondre méthode et rythme</div>
<p>La TDFN est normalement liée à une période semestrielle. Pour la méthode des taux forfaitaires et les autres situations, contrôler l’art. 35 et l’option annuelle éventuelle. Le délai de remise/paiement se calcule ensuite depuis la fin de la période concernée.</p>
</div>
</div>''','taf period info',1)

# Annual return
rep('Périodes de décompte — Trimestriel · Semestriel · Annuel (art. 35)','Périodes de décompte — Trimestriel · Semestriel · Annuel (art. 35 et 35a)','period heading')
rep('<strong>Décompte annuel</strong> (option) = 1 décompte/an + 3 acomptes trimestriels.','<strong>Décompte annuel</strong> (option dès 2025) = 1 décompte annuel avec acomptes selon la méthode et les règles AFC applicables.','annual intro')
rep('<p class="prose">L\'<strong>art. 35 LTVA</strong> définit les périodes de décompte. Par défaut : <strong>trimestrielle</strong> (méthode effective) ou <strong>semestrielle</strong> (méthodes forfaitaires). Sur demande, l\'assujetti peut choisir un autre rythme dans les limites légales.</p>',
    '<p class="prose">L’<strong>art. 35 LTVA</strong> règle les périodes ordinaires; l’<strong>art. 35a LTVA</strong> encadre le décompte annuel introduit dès 2025. La période dépend de la méthode de décompte et des conditions particulières. Avant de promettre un rythme à un client, vérifier l’éligibilité et les modalités d’acomptes affichées par l’AFC pour la période fiscale concernée.</p>',
    'annual legal basis',1)
rep('<tr><td><strong>Semestrielle</strong> (défaut TDFN/TaF)</td><td>TDFN ou TaF</td><td>2 décomptes/an — simplification</td></tr>','<tr><td><strong>Semestrielle</strong></td><td>Notamment TDFN</td><td>2 décomptes/an lorsque cette période est applicable</td></tr>','period table semi',1)
rep('<tr><td><strong>Annuelle avec acomptes</strong></td><td>CA ≤ CHF 5\'005\'000 + historique de remise/paiement dans les délais + demande via Portail AFC</td><td>1 décompte/an + 3 acomptes trimestriels — gain administratif mais cash-flow concentré</td></tr>',
    '<tr><td><strong>Annuelle avec acomptes</strong></td><td>Sur demande si les conditions de l’art. 35a et de la pratique AFC sont remplies; contrôler le seuil et l’historique au moment de la demande</td><td>1 décompte annuel; nombre et montant des acomptes dépendent de la méthode / règles AFC</td></tr>',
    'annual table',1)

# Interest general
for a in ['4,0%/an dès 01.06','4,0%/an dès 01.09','4,0%/an dès 01.12','4,0%/an dès 01.03']:
    t=t.replace(a,'taux DFF applicable dès l’échéance')
rep("<p>Au-delà de l'échéance 60 jours (art. 86 al. 1), l'AFC peut engager une procédure de rappel/sommation, notamment après échéance, (2) taxation d'office si non-dépôt persistant (art. 86 al. 2 — l'AFC estime la TVA due), (3) intérêts moratoires de 4,0%/an dès le 1er jour suivant échéance (DFF RS 631.014 — taux 2026). Retards répétés = signal de risque ; la prolongation doit être demandée via le service adéquat du Portail AFC lorsque c’est nécessaire.</p>",
    "<p>Après l’échéance, des intérêts moratoires peuvent courir au <strong>taux DFF applicable à la période</strong>. Un défaut de remise peut aussi conduire l’AFC à agir selon la procédure prévue par la LTVA. Pour un dossier réel, utiliser l’échéance affichée dans ePortal et le taux officiel applicable; ne pas mémoriser un taux annuel dans le module.</p>",
    'late payment rate',1)

# Art. 39/40 and bad debt
rep('Contre-prestations convenues vs encaissées (art. 39-40)','Contre-prestations convenues vs reçues — mode de décompte (art. 39; effets art. 40)','agreed title')
rep("L'<strong>art. 39 LTVA</strong> pose le principe : la TVA est due selon les <strong>contre-prestations convenues</strong> (date de la facture, peu importe le paiement effectif). L'<strong>art. 40 LTVA</strong> ouvre une option : sur demande à l'AFC, l'assujetti peut décompter selon les <strong>contre-prestations encaissées</strong> (date du paiement reçu).",
    "L’<strong>art. 39 LTVA</strong> règle le mode de décompte : en principe selon les contre-prestations convenues; sur autorisation/demande selon les conditions applicables, selon les contre-prestations reçues. L’<strong>art. 40 LTVA</strong> traite ensuite de la naissance de la créance fiscale. Il faut donc distinguer <em>choix du mode</em> et <em>moment fiscal</em>.",
    'art39/40 theory',1)
rep('<tr><td>Référence légale</td><td>art. 39 LTVA</td><td>art. 40 LTVA</td></tr>','<tr><td>Référence légale</td><td>art. 39 LTVA</td><td>art. 39 LTVA; effets temporels art. 40</td></tr>','art39 table',1)
rep('<div class="box-title">Facture impayée — Correction art. 27</div>','<div class="box-title">Créance irrécouvrable — modification ultérieure de la contre-prestation</div>','bad debt heading',1)
rep("En méthode <strong>convenue</strong>, si une créance devient <strong>définitivement irrécouvrable</strong> (faillite client clôturée sans paiement, prescription civile), l'assujetti peut <strong>récupérer la TVA déjà versée</strong> via un décompte rectificatif (art. 27 LTVA). Preuve de l'irrécouvrabilité requise (acte de défaut de biens, jugement de clôture de faillite). En méthode <strong>encaissement</strong>, le problème ne se pose pas : pas de TVA versée tant que pas d'encaissement.",
    "En mode convenu, une perte sur débiteur peut entraîner une <strong>modification ultérieure de la contre-prestation et de la dette fiscale</strong> lorsque les conditions sont établies. Le réflexe juridique se rattache à l’art. 41 LTVA et à la pratique AFC, pas à l’art. 27 (qui concerne l’impôt facturé à tort / mention de l’impôt). Documenter la perte, la chronologie et la correction comptable avant d’ajuster le décompte.",
    'bad debt article',1)
rep("L'AFC contrôle systématiquement la cohérence de la méthode choisie : (1) la TVA collectée et l'IP doivent suivre la même règle, (2) le passage d'une méthode à l'autre nécessite une demande formelle et une <strong>correction d'entrée</strong> sur les créances clients et dettes fournisseurs (art. 39 al. 2 + 40 al. 2 LTVA). (3) En méthode encaissement, l'assujetti doit pouvoir produire le détail des encaissements par période. Documentation rigoureuse exigée.",
    "La comptabilité doit être cohérente avec le mode autorisé. Lors d’un changement entre convenu et reçu, appliquer les <strong>règles de transition prévues par la LTVA/OTVA et la pratique AFC</strong> afin d’éviter doubles impositions ou omissions; ne pas comptabiliser une « correction d’entrée » générique sans base spécifique. Le détail des factures, paiements, créances et dettes à la date de transition doit être conservé.",
    'method transition',1)

# Return map
rep('Maîtriser le <strong>Formulaire 100</strong> (ePortal AFC) est la compétence fiduciaire centrale. Chaque ligne correspond à un chiffre numéroté (ch. 200, 221, 225, etc.). Une mauvaise ventilation = rappel AFC. Vous remplissez ce formulaire pour chaque client trimestriellement. Connaître chaque chiffre par cœur est l\'attendu minimal d\'un spécialiste TVA junior.',
    'Savoir <strong>lire le décompte électronique AFC</strong> et justifier chaque rubrique est une compétence fiduciaire centrale. Les chiffres usuels servent de repères, mais le professionnel ne les apprend pas comme une table immuable : il vérifie le formulaire/ePortal de la période, puis relie chaque ligne à la qualification M02 et à la comptabilité.',
    'form rhetoric',1)
rep('Le <strong>Formulaire 100</strong> est structuré en deux blocs principaux : <strong>I. Chiffre d\'affaires</strong> (ch. 200-299) et <strong>II. Calcul de l\'impôt</strong> (ch. 300-499). Le solde est reporté au <strong>ch. 500</strong> (TVA nette due) ou ch. 510 (crédit en faveur de l\'assujetti).',
    'Le décompte est structuré autour du <strong>chiffre d’affaires / déductions</strong>, du <strong>calcul de l’impôt</strong>, du <strong>DIP et de ses corrections</strong>, puis du solde. Les repères ci-dessous correspondent à la structure de travail actuelle du module; tout libellé doit être contrôlé dans ePortal avant dépôt.',
    'form intro',1)
rep('<tr><td class="art-cell">ch. 205</td><td>Prestations à soi-même (usage privé, art. 31)</td><td>Imposable au taux applicable</td></tr>',
    '<tr><td class="art-cell">ch. 205</td><td><strong>Rubrique spécifique du décompte</strong> — lire le libellé de la période</td><td>Ne pas l’utiliser comme synonyme de « prestations à soi-même »; les corrections d’utilisation se traitent dans les rubriques DIP appropriées selon le cas.</td></tr>',
    'ch205 fix',1)
rep('<tr><td class="art-cell">ch. 280</td><td>Autres déductions (escomptes, rabais accordés)</td><td>Réduisent la base imposable</td></tr>',
    '<tr><td class="art-cell">ch. 280</td><td>Autres déductions / ajustements selon le libellé du décompte applicable</td><td>Documenter la nature; les rabais/escomptes relèvent d’abord de la modification de la contre-prestation et de la comptabilité.</td></tr>',
    'ch280 nuance',1)
rep('<tr><td class="art-cell">ch. 420</td><td><strong>Réductions de la déduction de l’IP</strong></td><td>Subventions, taxes touristiques et autres flux art. 18 al. 2 / art. 33.</td></tr>',
    '<tr><td class="art-cell">ch. 420</td><td><strong>Réductions de la déduction de l’IP</strong></td><td>Notamment contributions visées par l’art. 33; toutes les non-contre-prestations ne déclenchent pas automatiquement la même réduction.</td></tr>',
    'ch420 nuance',1)

# Concordance
rep('<h3><span class="num">7</span>Concordance annuelle (art. 72) — Formulaire 550_03 <span class="block-risk risk-red">🔴 Rouge</span></h3>',
    '<h3><span class="num">7</span>Concordance annuelle (art. 72) — correction dans ePortal <span class="block-risk risk-red">🔴 Rouge</span></h3>',
    'concordance heading',1)
t=t.replace('<strong>Formulaire 550_03</strong>','<strong>service de correction / concordance disponible dans ePortal</strong>')
t=t.replace('Formulaire 550_03','correction / concordance ePortal')
rep("Au-delà des 240 jours, l'AFC peut considérer les décomptes périodiques comme définitifs (sauf erreur substantielle pouvant relever de la dénonciation spontanée art. 102).",
    "Le délai de 240 jours est le délai de concordance annuelle prévu par l’art. 72. Une erreur découverte plus tard ne se transforme pas automatiquement en dénonciation spontanée : il faut encore examiner la possibilité de correction, la prescription et, séparément, les éventuels éléments pénaux.",
    'concordance late nuance',1)
sub(r'<div class="box afc">\n<div class="box-icon">🏛️</div>\n<div class="box-body">\n<div class="box-title">Vision AFC — La concordance comme premier filtre de contrôle</div>.*?</div>\n</div>',
    '''<div class="box afc">
<div class="box-icon">🏛️</div>
<div class="box-body">
<div class="box-title">Vision contrôle — concordance reconstituable</div>
<p>La concordance doit permettre d’expliquer le passage entre comptabilité, journaux TVA et décomptes remis. Elle n’est ni un « signal vert » automatique ni une immunité contre le contrôle. Un dossier professionnel conserve le rapprochement, les écritures d’écart, les justificatifs et la preuve de la correction déposée.</p>
</div>
</div>''','concordance risk claims',1)
sub(r'<div class="box danger">\n<div class="box-icon">🚨</div>\n<div class="box-body">\n<div class="box-title">Erreur critique — Confusion concordance vs dénonciation spontanée</div>.*?</div>\n</div>',
    '''<div class="box danger">
<div class="box-icon">🚨</div>
<div class="box-body">
<div class="box-title">Erreur critique — Mélanger correction fiscale et pénal</div>
<p>Une correction selon l’art. 72 vise à remettre le décompte en conformité. L’art. 102 traite d’un éventuel effet pénal favorable sous conditions. <strong>Ne pas décider « concordance » ou « dénonciation » uniquement selon le montant ou la gravité ressentie</strong> : corriger l’impôt, documenter la chronologie et analyser séparément les conditions de l’art. 102 si un risque pénal existe.</p>
</div>
</div>''','concordance vs disclosure',1)

# Prescription/control
rep('<tr><td>Droit de contrôle AFC</td><td>5 ans (10 ans si fraude)</td><td class="art-cell">art. 78 LTVA</td></tr>',
    '<tr><td>Contrôle AFC</td><td>Peut porter sur les périodes non prescrites; appliquer la chronologie concrète</td><td class="art-cell">art. 42 + art. 78 LTVA</td></tr>',
    'control period',1)
sub(r'<div class="box afc">\n<div class="box-icon">🏛️</div>\n<div class="box-body">\n<div class="box-title">Vision AFC — Prescription en cas de soustraction</div>.*?</div>\n</div>',
    '''<div class="box afc">
<div class="box-icon">🏛️</div>
<div class="box-body">
<div class="box-title">Vision contrôle — prescription et pénal sont deux analyses</div>
<p>Le droit de taxer se prescrit selon l’art. 42 et ses causes d’interruption/suspension. L’art. 78 organise le contrôle; il ne crée pas une règle simple « 5 ans, 10 ans si fraude ». Les délais pénaux et la qualification d’une soustraction suivent leurs propres dispositions. Toujours établir une chronologie par période avant de conclure qu’une année est ouverte ou prescrite.</p>
</div>
</div>''','control prescription',1)
rep('Trois notions transversales à maîtriser : (1) la <strong>prescription</strong> détermine combien d\'années en arrière l\'AFC peut contrôler/rappeler (5 ans en principe, 10 ans en cas de fraude), (2) les <strong>délais de paiement</strong> conditionnent la date à laquelle la TVA est exigible (60 jours), (3) les <strong>intérêts moratoires et rémunératoires</strong> 2026 sont à <strong>4,0%/an</strong> (DFF RS 631.014, en vigueur depuis le 1<sup>er</sup> janvier 2026).',
    'Trois notions transversales à maîtriser : (1) la <strong>prescription</strong> doit être calculée période par période selon l’art. 42 et les actes interruptifs/suspensifs, (2) les <strong>délais de remise et de paiement</strong> déterminent les échéances, (3) les <strong>intérêts</strong> se calculent au taux DFF applicable à chaque période. Aucun taux annuel ne doit être mémorisé comme permanent.',
    'prescription intro',1)
sub(r'<h4 style="font-size:14px;color:var\(--navy\);margin:18px 0 8px;font-weight:600">Intérêts 2026.*?</table>',
    '''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Intérêts — méthode de travail</h4>
<table class="comp-table">
<thead><tr><th>Question</th><th>Réflexe</th></tr></thead>
<tbody>
<tr><td>Taux applicable</td><td>Consulter l’ordonnance DFF applicable à la période; un dossier couvrant plusieurs années peut nécessiter plusieurs taux.</td></tr>
<tr><td>Point de départ</td><td>Identifier l’échéance fiscale pertinente avant tout calcul.</td></tr>
<tr><td>Méthode de calcul</td><td>Utiliser le calcul / décompte officiel AFC lorsque disponible et documenter les hypothèses; ne pas imposer une convention 30/360 sans source de la période.</td></tr>
<tr><td>Seuil / montant minimal</td><td>Vérifier la règle actuelle dans l’ordonnance DFF au moment du dossier.</td></tr>
</tbody>
</table>''','interest method block',1)
sub(r'<div class="box info">\n<div class="box-icon">🧮</div>\n<div class="box-body">\n<div class="box-title">Calcul d\'intérêt moratoire — Exemple</div>.*?</div>\n</div>',
    '''<div class="box info">
<div class="box-icon">🧮</div>
<div class="box-body">
<div class="box-title">Calcul d’intérêt — exercice pédagogique</div>
<p>Pour un exercice chiffré, le taux et la convention de jours doivent être <strong>donnés dans l’énoncé</strong>. Dans un dossier réel, reprendre l’échéance, le taux DFF de chaque période et le calcul AFC. L’objectif M03 est la méthode et la traçabilité, pas la mémorisation d’un taux 2026.</p>
</div>
</div>''','interest example',1)

# Legal cards
rep('<div class="leg-title">Méthode TDFN &amp; taux forfaitaires</div>\n<div class="leg-desc">Méthode TDFN (al. 1-4) : taux forfaitaire par branche × CA brut TTC. Conditions : CA imposable TVA comprise ≤ CHF 5\'024\'000 ET impôt dû ≤ CHF 108\'000. Méthode TaF (al. 5) : collectivités publiques et NPO, sans plafond. Engagement min. 1 an.</div>',
    '<div class="leg-title">Méthode TDFN &amp; taux forfaitaires</div>\n<div class="leg-desc">L’art. 37 encadre les méthodes simplifiées. Pour TDFN, contrôler les seuils et l’attribution des taux de la période. Pour TaF, contrôler l’éligibilité de l’entité et les taux applicables. Les détails de changement de méthode et d’activités multiples doivent être vérifiés dans l’OTVA / pratique AFC actuelle.</div>',
    'art37 legal card',1)
rep('<div class="leg-title">Décompte selon les contre-prestations reçues (encaissement)</div>\n<div class="leg-desc">Option sur demande à l\'AFC. TVA due à l\'encaissement effectif (avantage pour clients lents/B2B). Engagement min. 1 an. Cohérence obligatoire entre TVA collectée et IP (même méthode).</div>',
    '<div class="leg-title">Naissance de la créance fiscale — effets du mode de décompte</div>\n<div class="leg-desc">L’art. 40 doit être lu avec l’art. 39 : l’art. 39 encadre le mode convenu/reçu; l’art. 40 règle le moment fiscal. Ne pas présenter l’art. 40 comme l’article qui « autorise » à lui seul la méthode reçue.</div>',
    'art40 legal card',1)
sub(r'<div class="leg-card">\n<div class="leg-icon red">📕</div>\n<div class="leg-content">\n<div class="leg-ref">Art. 87 LTVA.*?</div>\n</div>\n</div>',
    '''<div class="leg-card">
<div class="leg-icon red">📕</div>
<div class="leg-content">
<div class="leg-ref">Art. 87 LTVA — RS 641.20</div>
<div class="leg-title">Intérêts moratoires / rémunératoires</div>
<div class="leg-desc">L’art. 87 renvoie au régime des intérêts. Le <strong>taux chiffré</strong> est fixé par les prescriptions DFF applicables et doit être contrôlé pour la période concernée; ne pas figer un taux annuel dans M03.</div>
<div class="leg-links"><a class="leg-link" href="https://www.fedlex.admin.ch/eli/cc/2009/615/fr#art_87" rel="noopener noreferrer" target="_blank">📄 Art. 87 LTVA</a></div>
</div>
</div>''','art87 legal card',1)
sub(r'<div class="leg-card">\n<div class="leg-icon purple">📕</div>\n<div class="leg-content">\n<div class="leg-ref">Art. 102 LTVA.*?</div>\n</div>\n</div>',
    '''<div class="leg-card">
<div class="leg-icon purple">📕</div>
<div class="leg-content">
<div class="leg-ref">Art. 102 LTVA — RS 641.20</div>
<div class="leg-title">Dénonciation spontanée — effet pénal sous conditions</div>
<div class="leg-desc">L’effet favorable suppose que toutes les conditions légales soient remplies. La chronologie et l’état de connaissance de l’autorité comptent, mais M03 ne doit pas enseigner une garantie automatique fondée uniquement sur la date d’annonce d’un contrôle.</div>
<div class="leg-links"><a class="leg-link" href="https://www.fedlex.admin.ch/eli/cc/2009/615/fr#art_102" rel="noopener noreferrer" target="_blank">📄 Art. 102 LTVA</a></div>
</div>
</div>''','art102 legal card',1)
sub(r'<div class="leg-card">\n<div class="leg-icon gold">📘</div>\n<div class="leg-content">\n<div class="leg-ref">DFF RS 631\.014.*?</div>\n</div>\n</div>',
    '''<div class="leg-card">
<div class="leg-icon gold">📘</div>
<div class="leg-content">
<div class="leg-ref">Ordonnance DFF sur les taux d’intérêt</div>
<div class="leg-title">Taux d’intérêt — source à contrôler par période</div>
<div class="leg-desc">Le taux peut évoluer. Pour un dossier réel ou un calcul rétroactif, consulter l’ordonnance applicable à chaque période et conserver la référence utilisée.</div>
<div class="leg-links"><a class="leg-link" href="https://www.fedlex.admin.ch" rel="noopener noreferrer" target="_blank">📄 Fedlex</a></div>
</div>
</div>''','DFF legal card',1)
sub(r'<div class="leg-card">\n<div class="leg-icon gold">📘</div>\n<div class="leg-content">\n<div class="leg-ref">RS 641\.202\.62.*?</div>\n</div>\n</div>',
    '''<div class="leg-card">
<div class="leg-icon gold">📘</div>
<div class="leg-content">
<div class="leg-ref">TDFN — liste / pratique AFC en vigueur</div>
<div class="leg-title">Attribution des taux TDFN</div>
<div class="leg-desc">Les taux sont liés aux activités et peuvent être adaptés lors des révisions. Le module ne doit pas figer « fiduciaire 6,2% », « commerce 2,1% », etc. comme valeurs éternelles. Toujours contrôler la liste actuelle et l’attribution retenue pour le client.</div>
<div class="leg-links"><a class="leg-link" href="https://www.estv.admin.ch" rel="noopener noreferrer" target="_blank">🔗 Portail AFC</a></div>
</div>
</div>''','tdfn legal rate card',1)
rep('<div class="leg-title">Info TVA 12 — Taux de la dette fiscale nette (TDFN)</div>','<div class="leg-title">Pratique AFC — TDFN</div>','tdfn publication title',1)
rep('<div class="leg-title">Info TVA 15 — Décompte et paiement de l\'impôt</div>','<div class="leg-title">Pratique AFC — Décompte, correction et paiement</div>','decompte publication title',1)

# Case 2 summary bug and rate assumption
rep('<div class="calc-row"><span class="calc-label">TDFN : CA × 6,2%</span><span class="calc-val">CHF 35\'960</span></div>','<div class="calc-row"><span class="calc-label">TDFN : CA TTC du cas × taux TDFN donné (6,2%)</span><span class="calc-val">CHF 38\'873</span></div>','case2 calc tdfn',1)
rep('<div class="calc-row highlight"><span class="calc-label">Gain TDFN vs effective</span><span class="calc-val">+ CHF 6\'260</span></div>','<div class="calc-row highlight"><span class="calc-label">Écart TDFN vs effective dans l’hypothèse</span><span class="calc-val">CHF 1\'607</span></div>','case2 calc difference',1)
rep('• Taux TDFN services fiduciaires : 6,2%','• Pour l’exercice, l’AFC a attribué un taux TDFN de 6,2% à l’activité décrite (valeur pédagogique donnée, à ne pas généraliser)','case2 rate assumption',1)

# Case 3
rep('BatiPro envisage de passer à la méthode encaissement art. 40 pour Q2.','BatiPro envisage de demander le passage au mode selon les contre-prestations reçues au sens de l’art. 39; l’effet temporel se lit avec l’art. 40.','case3 art39',1)
rep('TVA due Q1 si BatiPro avait opté pour la méthode encaissement (art. 40) ?','TVA due Q1 si BatiPro avait été autorisée à décompter selon les contre-prestations reçues ?','case3 question',1)
rep('En méthode encaissement (art. 40 LTVA — option), la TVA est due seulement à l\'encaissement effectif.','Dans le mode selon les contre-prestations reçues, la dette est rattachée aux encaissements selon les art. 39–40 LTVA.','case3 received explanation',1)
sub(r'<div class="case-step" id="m3c3s3">.*?</div>\n</div>\n</div>\n<!-- CAS 4',
    '''<div class="case-step" id="m3c3s3">
<div class="step-question"><span class="step-q-num">Q3</span>Une créance de CHF 90'000 devient définitivement irrécouvrable après avoir été imposée selon le mode convenu. Quel réflexe ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c3s3',this,false)">A) La TVA est toujours définitivement perdue</button>
<button class="step-opt" onclick="caseAnswer('m3c3s3',this,true)">B) Documenter la perte et traiter la modification ultérieure de contre-prestation / dette fiscale selon l’art. 41 et la pratique AFC</button>
<button class="step-opt" onclick="caseAnswer('m3c3s3',this,false)">C) Utiliser l’art. 27 comme règle générale des créances irrécouvrables</button>
<button class="step-opt" onclick="caseAnswer('m3c3s3',this,false)">D) Attendre automatiquement 10 ans</button>
</div>
<div class="step-explanation" id="m3c3s3-expl">Une perte sur débiteur peut modifier la contre-prestation imposable. Le dossier doit prouver l’irrécouvrabilité et la correction comptable; l’ajustement se traite selon l’art. 41 et la pratique AFC applicable. L’art. 27 concerne l’impôt facturé / mentionné à tort et ne doit pas servir de base générique pour les pertes sur débiteurs. <div class="art-ref">📋 art. 41 LTVA · pratique AFC</div></div>
</div>
</div>
</div>
<!-- CAS 4''','case3 bad debt',1)

# Case 4 annual
rep('Le décompte annuel (art. 35 al. 1 LTVA + pratique AFC) suppose : (1) CA ≤ CHF 5\'005\'000, (2) bon historique de paiement (pas de retards récents), (3) demande via le Portail AFC. L\'AFC accepte ou refuse selon le profil de risque. Boutique Mode (CHF 950\'000) remplit largement la condition CA.',
    'Le décompte annuel est encadré par l’art. 35a LTVA. Le seuil et les conditions de comportement/remise doivent être contrôlés dans la pratique AFC de la période avant la demande. Avec CHF 950\'000 de CA, Boutique Mode est sous le seuil chiffré présenté dans le cas, mais l’éligibilité ne se réduit pas au CA seul.',
    'case4 eligibility',1)
rep('1 décompte annuel + 3 acomptes trimestriels obligatoires (calculés sur l\'année précédente)','1 décompte annuel + acomptes selon la méthode et le calendrier fixés par l’AFC','case4 option',1)
rep('Le décompte annuel s\'accompagne de <strong>3 acomptes trimestriels obligatoires</strong> calculés sur la TVA due de l\'année précédente (1/4 pour chaque trimestre Q1, Q2, Q3). Le décompte annuel final régularise au début de l\'année suivante. Avantage : 1 seul décompte détaillé/an. Inconvénient : trésorerie similaire (acomptes), gestion plus pointue.',
    'Le décompte annuel s’accompagne d’<strong>acomptes fixés selon les règles AFC applicables à la méthode de décompte</strong>. Le praticien contrôle le calendrier et les montants dans ePortal; il ne promet pas « trois quarts de l’année précédente » comme formule universelle. Le décompte annuel final régularise les acomptes.',
    'case4 installments',1)

# Case 6
sub(r'<div class="case-step" id="m3c6s2">.*?</div>\n</div>\n<div class="case-step" id="m3c6s3">',
    '''<div class="case-step" id="m3c6s2">
<div class="step-question"><span class="step-q-num">Q2</span>Au passage TDFN → effective, peut-on récupérer automatiquement 8,1% sur tout le stock au titre de l’art. 32 ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,false)">A) Oui, toujours sur la valeur comptable du stock</button>
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,true)">B) Non — appliquer les règles spécifiques de changement de méthode TDFN/OTVA et la pratique AFC actuelle avant toute correction</button>
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,false)">C) Oui, mais seulement sans inventaire</button>
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,false)">D) Le stock doit être vendu avant le changement</button>
</div>
<div class="step-explanation" id="m3c6s2-expl">La TDFN intègre forfaitairement le DIP; le changement de méthode obéit à des règles spécifiques. <strong>L’art. 32 n’autorise pas à lui seul une récupération mécanique « stock × taux normal ».</strong> Avant l’écriture de transition, documenter stocks/immobilisations et appliquer l’OTVA / pratique AFC en vigueur à la date du changement. <div class="art-ref">📋 art. 37 LTVA · OTVA / pratique AFC TDFN</div></div>
</div>
<div class="case-step" id="m3c6s3">''','case6 stock',1)
sub(r'<div class="case-step" id="m3c6s3">.*?</div>\n</div>\n</div>\n<!-- CAS 7',
    '''<div class="case-step" id="m3c6s3">
<div class="step-question"><span class="step-q-num">Q3</span>Quel délai faut-il respecter avant un nouveau changement de méthode ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c6s3',this,true)">A) Vérifier la règle de changement applicable à la période fiscale et déposer la demande dans le délai AFC</button>
<button class="step-opt" onclick="caseAnswer('m3c6s3',this,false)">B) Toujours exactement 3 ans, quelle que soit la version légale</button>
<button class="step-opt" onclick="caseAnswer('m3c6s3',this,false)">C) Toujours 1 mois</button>
<button class="step-opt" onclick="caseAnswer('m3c6s3',this,false)">D) Le changement est irréversible</button>
</div>
<div class="step-explanation" id="m3c6s3-expl">Les délais de changement ont fait l’objet de révisions et doivent être contrôlés dans l’OTVA / pratique AFC en vigueur. Le bon réflexe M03 est de vérifier la période minimale et le délai de demande <strong>avant</strong> de conseiller le passage. <div class="art-ref">📋 art. 37 LTVA · OTVA / pratique AFC</div></div>
</div>
</div>
</div>
<!-- CAS 7''','case6 waiting period',1)

# Case 7 rates become exercise assumptions
rep('Taux d\'intérêt moratoire applicable : 4,5%/an en 2025 → 4,0%/an dès 01.01.2026 (RS 631.014).','Pour cet <strong>exercice pédagogique</strong>, l’énoncé fournit les taux 4,5% pour la portion 2025 et 4,0% pour la portion 2026. Dans un dossier réel, les taux doivent être contrôlés dans l’ordonnance DFF applicable.','case7 assumptions',1)
t=t.replace('selon la méthode commerciale 30/360','selon la convention de calcul donnée dans l’exercice')
t=t.replace('méthode commerciale 30/360','convention pédagogique 30/360')

# Case 8 no universal subsidy ratio
sub(r'<div class="case-step" id="m3c8s3">.*?</div>\n</div>\n<div class="case-step" id="m3c8s4">',
    '''<div class="case-step" id="m3c8s3">
<div class="step-question"><span class="step-q-num">Q3</span>Comment traiter le DIP lié à l’activité de formation exclue et à la subvention ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c8s3',this,false)">A) Appliquer automatiquement le ratio subventions / (subventions + CA) à tout l’IP</button>
<button class="step-opt" onclick="caseAnswer('m3c8s3',this,true)">B) Affecter directement l’IP lié à la formation, qualifier la subvention, puis appliquer une méthode de réduction appropriée aux coûts communs si l’art. 33 l’exige</button>
<button class="step-opt" onclick="caseAnswer('m3c8s3',this,false)">C) Supprimer tout l’IP</button>
<button class="step-opt" onclick="caseAnswer('m3c8s3',this,false)">D) Ignorer la subvention dans tous les cas</button>
</div>
<div class="step-explanation" id="m3c8s3-expl">L’IP directement lié à une prestation exclue non optée doit être traité selon son affectation. Pour la subvention, il faut d’abord vérifier qu’elle relève bien de l’art. 33 et identifier les coûts financés / communs. <strong>Il n’existe pas dans M03 de prorata universel « subvention ÷ chiffre d’affaires ».</strong> La méthode détaillée appartient à M05. <div class="art-ref">📋 art. 29–30 + art. 33 LTVA · renvoi M05</div></div>
</div>
<div class="case-step" id="m3c8s4">''','case8 DIP method',1)
sub(r'<div class="case-step" id="m3c8s4">.*?</div>\n</div>\n<div class="calc-box">.*?</div>\n</div>\n</div>\n</div>\n<!-- Niveau 3',
    '''<div class="case-step" id="m3c8s4">
<div class="step-question"><span class="step-q-num">Q4</span>Peut-on calculer un solde TVA final fiable avec les seules données du cas ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c8s4',this,false)">A) Oui, en appliquant automatiquement 5,62% à l’IP commun</button>
<button class="step-opt" onclick="caseAnswer('m3c8s4',this,true)">B) Non — il manque la méthode justifiée de réduction liée à la subvention / affectation des coûts communs</button>
<button class="step-opt" onclick="caseAnswer('m3c8s4',this,false)">C) Oui, ch. 420 vaut toujours le montant de la subvention</button>
<button class="step-opt" onclick="caseAnswer('m3c8s4',this,false)">D) Oui, aucun DIP n’est déductible</button>
</div>
<div class="step-explanation" id="m3c8s4-expl">La TVA sur les ventes imposables peut être calculée, mais le <strong>solde net</strong> dépend du traitement correct du DIP commun. Sans faits supplémentaires sur la subvention, les coûts financés et la méthode appropriée, chiffrer CHF 972 serait une fausse précision. La sortie professionnelle est une matrice de qualification + une demande d’informations / calcul M05. <div class="art-ref">📋 M03 → M05</div></div>
</div>
</div>
</div>
</div>
<!-- Niveau 3''','case8 final',1)

# Case 9
sub(r'<!-- CAS 9 — Contrôle AFC avec extrapolation -->.*?<!-- CAS 10 — Dénonciation spontanée -->',
    '''<!-- CAS 9 — Contrôle AFC / estimation -->
<div class="case-block">
<div class="case-header"><div class="case-num">09</div><div class="case-meta"><div class="case-title">Helvetia Trading SA — Erreur récurrente et contrôle AFC</div><div class="case-subtitle">PME commerce · Vaud · Contrôle 2026 · 🔴 Risque élevé</div></div></div>
<div class="case-body">
<div class="case-scenario"><strong>Contexte :</strong> Helvetia a classé des prestations B2B étrangères au ch. 230 alors que, sous les faits donnés, elles relèvent de la territorialité et du ch. 221. L’erreur existe sur plusieurs périodes; l’AFC demande la reconstitution.</div>
<div class="case-context">📚 <strong>Objectif :</strong> distinguer correction fiscale, droit au DIP, période non prescrite et éventuelle estimation.</div>
<div class="case-step" id="m3c9s1"><div class="step-question"><span class="step-q-num">Q1</span>Premier impact à analyser ?</div><div class="step-options"><button class="step-opt" onclick="caseAnswer('m3c9s1',this,true)">A) Requalifier les flux et recalculer le DIP par affectation; ch. 221 et ch. 230 n’ont pas les mêmes conséquences</button><button class="step-opt" onclick="caseAnswer('m3c9s1',this,false)">B) Appliquer 8,1% à tout le CA étranger</button><button class="step-opt" onclick="caseAnswer('m3c9s1',this,false)">C) Aucune conséquence possible</button><button class="step-opt" onclick="caseAnswer('m3c9s1',this,false)">D) Amende automatique</button></div><div class="step-explanation" id="m3c9s1-expl">La qualification et le lieu déterminent le traitement du chiffre d’affaires et du DIP. Le dossier doit être reconstruit période par période. <div class="art-ref">📋 art. 8, 21, 29–30 LTVA</div></div></div>
<div class="case-step" id="m3c9s2"><div class="step-question"><span class="step-q-num">Q2</span>Combien d’années l’AFC peut-elle reprendre automatiquement ?</div><div class="step-options"><button class="step-opt" onclick="caseAnswer('m3c9s2',this,false)">A) Toujours exactement 5</button><button class="step-opt" onclick="caseAnswer('m3c9s2',this,true)">B) Il faut calculer la prescription selon l’art. 42 et la chronologie; l’art. 78 organise le contrôle</button><button class="step-opt" onclick="caseAnswer('m3c9s2',this,false)">C) Toujours 10 en cas d’erreur</button><button class="step-opt" onclick="caseAnswer('m3c9s2',this,false)">D) Une seule année</button></div><div class="step-explanation" id="m3c9s2-expl">La fenêtre de contrôle ne se résume pas à un nombre mémorisé. Vérifier naissance de la créance, interruptions/suspensions et prescription absolue. <div class="art-ref">📋 art. 42 + art. 78 LTVA</div></div></div>
<div class="case-step" id="m3c9s3"><div class="step-question"><span class="step-q-num">Q3</span>Une extrapolation à partir d’un échantillon est-elle automatique ?</div><div class="step-options"><button class="step-opt" onclick="caseAnswer('m3c9s3',this,false)">A) Oui, tout écart d’une année est multiplié par cinq</button><button class="step-opt" onclick="caseAnswer('m3c9s3',this,true)">B) Non — toute estimation/extrapolation doit reposer sur des faits comparables, une méthode défendable et les périodes juridiquement ouvertes</button><button class="step-opt" onclick="caseAnswer('m3c9s3',this,false)">C) Oui, sans examen des pièces</button><button class="step-opt" onclick="caseAnswer('m3c9s3',this,false)">D) Jamais</button></div><div class="step-explanation" id="m3c9s3-expl">Le praticien teste la représentativité, la qualité des données et les différences entre périodes. Aucun « rappel type » ne doit être inventé. <div class="art-ref">📋 contrôle / estimation selon LTVA et pratique</div></div></div>
<div class="case-step" id="m3c9s4"><div class="step-question"><span class="step-q-num">Q4</span>Quelle réponse professionnelle au contrôle ?</div><div class="step-options"><button class="step-opt" onclick="caseAnswer('m3c9s4',this,true)">A) Fournir une reconstruction documentée, corriger ce qui est établi et contester méthodiquement ce qui ne l’est pas</button><button class="step-opt" onclick="caseAnswer('m3c9s4',this,false)">B) Nier les faits</button><button class="step-opt" onclick="caseAnswer('m3c9s4',this,false)">C) Accepter toute extrapolation sans contrôle</button><button class="step-opt" onclick="caseAnswer('m3c9s4',this,false)">D) Retarder les réponses pour « négocier » les intérêts</button></div><div class="step-explanation" id="m3c9s4-expl">Séparer faits, qualification, calcul fiscal, prescription et pénal. M11 approfondira la stratégie procédurale. <div class="art-ref">📋 méthode M03 → M11</div></div></div>
</div></div>
<!-- CAS 10 — Dénonciation spontanée -->''','replace case9',1)

# Dangerous global cleanup
dangerous_repls={
    'art. 40 LTVA — option':'art. 39 LTVA — mode sur demande; effets art. 40',
    'méthode encaissement art. 40':'mode selon les contre-prestations reçues (art. 39; effets art. 40)',
    'correction art. 27 LTVA':'correction selon l’art. 41 LTVA',
    'correction d\'entrée sur stocks lors du passage TDFN → effective (art. 32 LTVA — favorable)':'application des règles spécifiques de transition TDFN/OTVA; pas de récupération automatique « stock × taux »',
    'Retour TDFN après effective : min. 3 ans civils':'Retour/changement de méthode : délai à vérifier dans l’OTVA / pratique AFC en vigueur',
    'périodicité semestrielle est réservée aux TDFN/TaF':'périodicité semestrielle concerne notamment la TDFN; vérifier la période applicable aux TaF',
    '4,0%/an en 2026':'taux DFF applicable à la période',
    '4,0%/an (taux 2026)':'taux DFF applicable',
    'Échec garanti':'Effet favorable non garanti',
    'AVANT toute annonce de contrôle':'chronologie à documenter et conditions légales à vérifier',
}
for a,b in dangerous_repls.items():
    if a in t:
        t=t.replace(a,b); changes.append('global:'+a[:24])

# Error cards remove fictional money ranges
t=re.sub(r'<div class="error-impact">CHF[^<]*</div>','<div class="error-impact">Impact à chiffrer selon dossier</div>',t)
t=re.sub(r'<div class="error-section-title">Impact financier moyen</div>\s*<div class="error-text">.*?</div>',
         '<div class="error-section-title">Conséquence possible</div><div class="error-text">Le montant dépend des périodes, de la base HT/TTC, du DIP effectivement ouvert, des preuves et des intérêts applicables. Aucun « impact moyen » ne doit être présenté comme statistique AFC sans source.</div>',t,flags=re.S)
sub(r'<!-- E8 -->.*?<div class="section-nav">',
    '''<!-- E8 -->
<div class="error-block"><div class="error-head"><div class="error-num">08</div><div class="error-title">Changement TDFN → effective traité comme une simple écriture d’IP</div><div class="error-impact">Impact à chiffrer selon dossier</div></div><div class="error-body"><div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">Le dossier applique automatiquement « valeur des stocks × taux » au premier décompte effectif sans vérifier les règles de transition TDFN.</div></div><div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Documenter stocks, immobilisations, activités et date du changement; appliquer l’OTVA / pratique AFC actuelle relative au changement de méthode. L’art. 32 ne constitue pas à lui seul une autorisation de récupération automatique.</div></div><div class="error-section"><div class="error-section-title">Conséquence possible</div><div class="error-text">Une transition mal traitée peut créer une double déduction ou une perte de droit. Reconstituer le traitement avant correction.</div></div></div></div>
<div class="section-nav">''','error8 replace',1)

# QCM targeted fixes
sub(r"\{ id:'m03-q05'.*?\},\n  \{ id:'m03-q06'",
    "{ id:'m03-q05', diff:'easy', art:'art. 87 LTVA + ordonnance DFF',\n    q:'Quel réflexe est correct pour les intérêts moratoires ?',\n    opts:['Mémoriser 4,0% comme taux permanent','Vérifier le taux DFF applicable à la période et l’échéance avant de calculer','Utiliser toujours 5%','Aucun intérêt n’est possible en TVA'],\n    correct:1,\n    expl:'Le taux peut évoluer. M03 enseigne à identifier l’échéance, le taux DFF de la période et le calcul applicable, pas à mémoriser un chiffre annuel.'\n  },\n  { id:'m03-q06'",
    'q05 interest',1)
rep('La périodicité semestrielle est réservée aux TDFN/TaF.','La TDFN est normalement semestrielle; pour TaF, vérifier la période applicable selon l’art. 35 et la pratique actuelle.','q01 taf period')

# Global subsidy ratios and disclosure guarantees
t=t.replace('Prorata = Subventions ÷ (Subventions + CA imposable)','Méthode de réduction à déterminer selon affectation et art. 33; aucun prorata universel')
t=t.replace('Subventions / (Subventions + CA imposable)','méthode appropriée selon art. 33 et affectation')
t=t.replace('signalement complet AVANT annonce de contrôle','vérification de toutes les conditions de l’art. 102, de la chronologie et de l’état de connaissance de l’autorité')
t=t.replace('exempt d\'amende art. 96','effet pénal favorable seulement si toutes les conditions légales sont remplies')
t=t.replace('Évite la sanction pénale mais pas les intérêts moratoires.','Peut produire un effet pénal favorable si toutes les conditions sont remplies; le traitement fiscal et les intérêts restent à analyser séparément.')

# Volatile interest remnants
t=t.replace('Intérêts moratoires 2026 sont à <strong>4,0%/an</strong>','Intérêts moratoires : taux DFF applicable à la période')
t=t.replace('intérêts moratoires 4,0%/an','intérêts au taux DFF applicable')
t=t.replace('intérêts moratoires 4,0%','intérêts au taux DFF applicable')
t=t.replace('taux 2026 : 4,0%','taux DFF à vérifier pour la période')

# Audit note
leg_marker='<h4 style="font-size:14px;color:var(--navy);margin:18px 0 12px;font-weight:600">Articles LTVA clés M03 — Liens Fedlex</h4>'
note='''<div class="box success" style="margin:18px 0"><div class="box-icon">✅</div><div class="box-body"><div class="box-title">Audit professionnel M03 — 06.09.2026</div>Le module a été révisé pour supprimer les automatismes dangereux : art. 39/40, créances irrécouvrables, périodicité TaF, changement TDFN, subventions/DIP, prescription/contrôle et taux d’intérêt volatils. Pour les <strong>numéros de rubriques ePortal, taux TDFN et taux d’intérêt</strong>, la source officielle de la période reste prioritaire sur tout mémo pédagogique.</div></div>
'''
if leg_marker in t and 'Audit professionnel M03 — 06.09.2026' not in t:
    t=t.replace(leg_marker,note+leg_marker,1); changes.append('audit note:1')

p.write_text(t,encoding='utf-8')
print('Applied changes:',len(changes))
for c in changes: print(' -',c)
