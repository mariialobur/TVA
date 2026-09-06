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

# Hero / terminology / current portal
rep('les délais de paiement, la prescription et les intérêts moratoires/rémunératoires 2026.',
    'les délais de paiement, la prescription et le calcul des intérêts selon le taux applicable à chaque période.',
    'hero interest scope',1)
rep('Vous l\'établissez via le <strong>Formulaire 100 AFC</strong> trimestriellement, en ventilant chaque opération aux bons chiffres du décompte (ch. 200, 220, 221, 225, 230, 303, 313, 343, 383, 400, 405, 410, 415, 420, 479, 500).',
    'Vous l’établissez aujourd’hui via le <strong>Portail AFC · Décompte TVA pro</strong>, en reliant chaque flux aux rubriques du décompte de la période. Les chiffres usuels restent utiles comme repères, mais le libellé affiché dans le portail prime sur un ancien formulaire ou une ancienne capture.',
    'current portal in effective',1)
rep('<tr><td>Formulaire</td><td>Formulaire 100 (décompte standard)</td><td class="art-cell">art. 71 LTVA</td></tr>',
    '<tr><td>Dépôt</td><td>Portail AFC · Décompte TVA pro</td><td class="art-cell">art. 71–71a LTVA</td></tr>',
    'effective portal table',1)

# TDFN reality: more than one rate possible under current rules
rep('Elle simplifie radicalement la gestion : <strong>un seul taux forfaitaire</strong> appliqué au CA brut TTC remplace tout le calcul d\'IP.',
    'Elle simplifie la gestion : le ou les <strong>taux TDFN attribués aux activités</strong> sont appliqués au chiffre d’affaires déterminant TVA comprise, sans déduction séparée du DIP.',
    'tdfn reality rates',1)
rep('<tr><td>Choix volontaire</td><td>Sur option formelle à l\'AFC</td><td>Demande écrite, engagement min. 1 an</td></tr>',
    '<tr><td>Choix volontaire</td><td>Sur demande / choix valable auprès de l’AFC</td><td>Le mode doit être conservé au moins pendant une période fiscale complète; vérifier le délai de demande de la période concernée</td></tr>',
    'tdfn one-period rule',1)

# TaF current periodicity / eligibility
rep('<tr><td>Périodicité</td><td>Semestrielle en TDFN</td><td>Déterminée selon l’art. 35 / pratique applicable; ne pas supposer « semestrielle »</td></tr>',
    '<tr><td>Périodicité ordinaire</td><td>Semestrielle</td><td>Trimestrielle</td></tr>',
    'taf exact periodicity',1)
rep('La TDFN est normalement liée à une période semestrielle. Pour la méthode des taux forfaitaires et les autres situations, contrôler l’art. 35 et l’option annuelle éventuelle. Le délai de remise/paiement se calcule ensuite depuis la fin de la période concernée.',
    'La <strong>TDFN</strong> se décompte en règle générale semestriellement. La méthode des <strong>taux forfaitaires (TaF)</strong> se décompte en règle générale trimestriellement. Une option de décompte annuel peut ensuite modifier ce rythme si ses conditions sont remplies. Le délai de remise/paiement se calcule depuis la fin de la période concernée.',
    'taf periodicity info',1)
rep('<p>La périodicité du décompte conditionne votre rythme de travail fiduciaire. <strong>Décompte trimestriel</strong> (standard méthode effective) = 4 décomptes/an aux échéances 31.05, 31.08, 30.11, 28/29.02. <strong>Décompte semestriel</strong> (TDFN/TaF) = 2 décomptes/an. <strong>Décompte annuel</strong> (option dès 2025) = 1 décompte annuel avec acomptes selon la méthode et les règles AFC applicables.</p>',
    '<p>La périodicité du décompte conditionne votre rythme de travail fiduciaire. <strong>Méthode effective et TaF</strong> : décompte trimestriel en règle générale. <strong>TDFN</strong> : décompte semestriel en règle générale. <strong>Décompte annuel</strong> : option distincte depuis 2025, avec des acomptes dont le nombre dépend de la méthode.</p>',
    'period reality',1)

# Annual reporting exact current mechanics (2026 state)
rep('<tr><td><strong>Annuelle avec acomptes</strong></td><td>Sur demande si les conditions de l’art. 35a et de la pratique AFC sont remplies; contrôler le seuil et l’historique au moment de la demande</td><td>1 décompte annuel; nombre et montant des acomptes dépendent de la méthode / règles AFC</td></tr>',
    '<tr><td><strong>Annuelle avec acomptes</strong></td><td>CA annuel ≤ CHF 5’005’000 et conditions de l’art. 35a / pratique AFC; demande dans le délai prévu</td><td>1 décompte annuel. En état 2026 : 3 acomptes pour effective/TaF, 1 acompte pour TDFN; montants fixés par l’AFC puis régularisés au décompte annuel.</td></tr>',
    'annual exact table',1)

# Return map: current exact box 205 / 280 and current portal heading
rep('<h3><span class="num">6</span>Chiffres clés du décompte TVA — Formulaire 100 <span class="block-risk risk-red">🔴 Rouge</span></h3>',
    '<h3><span class="num">6</span>Chiffres clés du décompte TVA — repères du Décompte TVA pro <span class="block-risk risk-red">🔴 Rouge</span></h3>',
    'return map heading',1)
rep('<tr><td class="art-cell">ch. 205</td><td><strong>Rubrique spécifique du décompte</strong> — lire le libellé de la période</td><td>Ne pas l’utiliser comme synonyme de « prestations à soi-même »; les corrections d’utilisation se traitent dans les rubriques DIP appropriées selon le cas.</td></tr>',
    '<tr><td class="art-cell">ch. 205</td><td>Prestations exclues de l’art. 21 pour lesquelles l’option d’imposition a été exercée</td><td>À rapprocher de l’art. 22 et des factures / contrats correspondants.</td></tr>',
    'ch205 exact',1)
rep('<tr><td class="art-cell">ch. 280</td><td>Autres déductions / ajustements selon le libellé du décompte applicable</td><td>Documenter la nature; les rabais/escomptes relèvent d’abord de la modification de la contre-prestation et de la comptabilité.</td></tr>',
    '<tr><td class="art-cell">ch. 280</td><td>Diverses déductions prévues par le décompte (p. ex. valeur du sol, part non imposable / prix d’achat selon le cas)</td><td>Ne pas utiliser ch. 280 comme rubrique générale des rabais/escomptes; ceux-ci relèvent notamment du ch. 235 / modification de contre-prestation.</td></tr>',
    'ch280 exact',1)

# Concordance: explain 180th day + operational 240 days / art. 43 nuance
rep('L\'<strong>art. 72 LTVA</strong> impose à l\'assujetti de corriger les <strong>inexactitudes constatées dans le cadre de la concordance annuelle</strong>, dans les <strong>240 jours suivant la fin de l\'exercice commercial</strong>. Le formulaire dédié est le <strong>550_03</strong>, déposé via ePortal AFC. Le délai de 240 jours est le délai de concordance annuelle prévu par l’art. 72. Une erreur découverte plus tard ne se transforme pas automatiquement en dénonciation spontanée : il faut encore examiner la possibilité de correction, la prescription et, séparément, les éventuels éléments pénaux.',
    'L’<strong>art. 72 LTVA</strong> exige la concordance annuelle et rattache la correction à la <strong>période de décompte dans laquelle tombe le 180e jour suivant la fin de l’exercice</strong>. L’AFC indique en pratique qu’en l’absence de décompte rectificatif dans les <strong>240 jours</strong> suivant la fin de l’exercice, elle part du principe que les décomptes sont complets et corrects. Ces deux repères ne se contredisent pas : pour un assujetti trimestriel avec clôture au 31 décembre, le 180e jour tombe au T2, dont le décompte arrive ensuite à échéance. Une erreur découverte plus tard doit être analysée au regard des possibilités de correction et de l’art. 43, de la prescription et, séparément, d’un éventuel risque pénal.',
    'concordance 180/240',1)
rep('<tr><td>Délai</td><td>240 jours après fin exercice commercial</td></tr>',
    '<tr><td>Repère légal / pratique</td><td>Correction dans la période contenant le 180e jour après la clôture; l’AFC utilise aussi le repère pratique de 240 jours pour la finalisation de la concordance annuelle.</td></tr>',
    'concordance table timing',1)
rep('Étape 4 — Déposer correction / concordance ePortal via ePortal AFC dans les 240 jours',
    'Étape 4 — Déposer la correction dans la période / le délai applicable selon art. 72 et le Portail AFC',
    'concordance workflow',1)

# Current interest facts are allowed if dated and sourced; restore a precise current note without making it permanent
sub(r'<h4 style="font-size:14px;color:var\(--navy\);margin:18px 0 8px;font-weight:600">Intérêts — méthode de travail</h4>.*?</table>',
    '''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Intérêts — méthode de travail et état 2026</h4>
<table class="comp-table">
<thead><tr><th>Question</th><th>Réflexe</th></tr></thead>
<tbody>
<tr><td>Taux applicable</td><td>Consulter l’ordonnance DFF de la période. <strong>État vérifié au 06.09.2026 :</strong> 4,0% pour 2026; 4,5% pour 2025.</td></tr>
<tr><td>Point de départ</td><td>Identifier l’échéance fiscale; l’intérêt moratoire court après l’échéance jusqu’au paiement.</td></tr>
<tr><td>Méthode de calcul</td><td>L’AFC utilise la méthode commerciale 30/360 dans ses calculs de concordance / intérêts. Pour un dossier réel, reprendre le calcul officiel et documenter les périodes/taux.</td></tr>
<tr><td>Seuil pratique</td><td>État 2026 : les intérêts inférieurs à CHF 100 ne sont en principe ni perçus ni versés.</td></tr>
</tbody>
</table>''','interest verified block',1)
rep('Pour un exercice chiffré, le taux et la convention de jours doivent être <strong>donnés dans l’énoncé</strong>. Dans un dossier réel, reprendre l’échéance, le taux DFF de chaque période et le calcul AFC. L’objectif M03 est la méthode et la traçabilité, pas la mémorisation d’un taux 2026.',
    'Pour un exercice chiffré, les taux peuvent être donnés dans l’énoncé. En état vérifié au 06.09.2026, le taux est 4,0% pour 2026 et 4,5% pour 2025; l’AFC applique la méthode commerciale 30/360. Pour les périodes futures, recontrôler l’ordonnance DFF avant de calculer.',
    'interest example verified',1)

# Case 4 annual exact rules
rep("B) CA ≤ CHF 5'005'000 + bon historique de remise/paiement + demande via Portail AFC",
    "B) CA ≤ CHF 5'005'000 + conditions de remise/paiement remplies + demande dans le délai de l’art. 35a / Portail AFC",
    'case4 annual answer',1)
rep('Le décompte annuel est encadré par l’art. 35a LTVA. Le seuil et les conditions de comportement/remise doivent être contrôlés dans la pratique AFC de la période avant la demande. Avec CHF 950\'000 de CA, Boutique Mode est sous le seuil chiffré présenté dans le cas, mais l’éligibilité ne se réduit pas au CA seul.',
    'Le décompte annuel est encadré par l’art. 35a LTVA. <strong>État 2026 :</strong> CA annuel ≤ CHF 5’005’000; les décomptes des trois années précédentes et futurs doivent avoir été remis et payés dans les délais; la demande se fait dans les 60 jours suivant le début de l’exercice (ou, pour un nouvel assujetti, dans les 60 jours suivant l’attribution du numéro TVA). Avec CHF 950’000, la condition de CA est remplie, mais les autres conditions doivent encore l’être.',
    'case4 eligibility exact',1)
rep('Le décompte annuel s’accompagne d’<strong>acomptes fixés selon les règles AFC applicables à la méthode de décompte</strong>. Le praticien contrôle le calendrier et les montants dans ePortal; il ne promet pas « trois quarts de l’année précédente » comme formule universelle. Le décompte annuel final régularise les acomptes.',
    'Le décompte annuel s’accompagne d’acomptes fixés par l’AFC. <strong>État 2026 :</strong> méthode effective ou TaF = trois acomptes (échéances 30 mai, 30 août, 30 novembre); TDFN = un acompte (30 août). Le décompte annuel final, dû à la fin février de l’année suivante, régularise ces acomptes.',
    'case4 instalments exact',1)
rep('<div class="art-ref">📋 art. 35 al. 1 LTVA</div>','<div class="art-ref">📋 art. 35a LTVA · pratique AFC décompte annuel</div>','case4 art ref',2)

# Case 5 concordance timing and current interest
rep('Quel délai pour déposer le correction / concordance ePortal et corriger ?',
    'Quel repère juridique faut-il utiliser pour la concordance annuelle ?',1)
rep("C) 240 jours après fin de l'exercice (art. 72 LTVA)",
    'C) Corriger dans la période contenant le 180e jour après la clôture; l’AFC utilise aussi le repère pratique de 240 jours pour la finalisation',1)
rep("L'art. 72 LTVA impose un délai de 240 jours après la fin de l'exercice commercial pour corriger les inexactitudes via la concordance annuelle. Pour l'exercice 2025 clos le 31.12.2025 → délai = <strong>28.08.2026</strong>. Au-delà : l'AFC peut considérer les décomptes comme définitifs (sauf erreur substantielle → dénonciation spontanée art. 102).",
    'L’art. 72 rattache la correction à la période de décompte dans laquelle tombe le <strong>180e jour</strong> après la clôture. L’AFC indique aussi qu’en l’absence de rectification dans les <strong>240 jours</strong>, elle part du principe que la concordance est complète. Pour le cas, il faut donc identifier la période concernée et son échéance dans le Portail AFC, plutôt que mémoriser une date unique.',
    'case5 timing',1)
rep("B) CHF 5'265 × 4,0% × 4/12 = CHF 70 — mais &lt; CHF 100 → en principe non perçu (art. 1 al. 3 Ord. DFF)",
    "B) Avec le taux 2026 vérifié de 4,0%, environ CHF 70 pour quatre mois; comme le total d’intérêt reste &lt; CHF 100, il n’est en principe pas perçu",1)
rep("Intérêts moratoires = supplément TVA × taux × période de retard. Taux 2026 = 4,0%/an (DFF RS 631.014). Retard depuis échéance Q4 (28.02.2026) jusqu'au dépôt (30.06.2026) ≈ 4 mois. Calcul : 5'265 × 4,0% × 4/12 ≈ <strong>CHF 70</strong>. Au seuil minimal CHF 100 (art. 1 al. 3 Ord. DFF) → <strong>en principe non perçu</strong>. Cas favorable : seul le supplément TVA est dû.",
    "État vérifié au 06.09.2026 : taux 2026 = 4,0%. Pour l’exercice, quatre mois de retard donnent environ CHF 70 selon la convention retenue. L’AFC ne perçoit en principe pas un intérêt inférieur à CHF 100. Le dossier réel doit reprendre l’échéance exacte, le calcul commercial AFC et le taux DFF de chaque période.",
    'case5 interest verified',1)

# Case 6: current three-year exceedance rule + correct transition relief
rep('<div class="case-context">📚 <strong>Objectif :</strong> appliquer la procédure de passage TDFN → effective et calculer la correction d\'entrée sur stocks (art. 32).</div>',
    '<div class="case-context">📚 <strong>Objectif :</strong> déterminer si le dépassement impose réellement un changement de méthode et, si un passage à l’effective intervient, appliquer correctement le dégrèvement ultérieur sur la valeur résiduelle.</div>',
    'case6 objective',1)
sub(r'<div class="case-step" id="m3c6s1">.*?</div>\n</div>\n<div class="case-step" id="m3c6s2">',
    '''<div class="case-step" id="m3c6s1">
<div class="step-question"><span class="step-q-num">Q1</span>Le seul dépassement prévu en 2026 entraîne-t-il automatiquement le passage à l’effective dès 2027 ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c6s1',this,false)">A) Oui — un seul exercice au-dessus du seuil suffit toujours</button>
<button class="step-opt" onclick="caseAnswer('m3c6s1',this,true)">B) Non — selon la règle actuelle, le dépassement des limites est apprécié sur trois périodes fiscales consécutives; il faut suivre les résultats effectifs et la pratique AFC</button>
<button class="step-opt" onclick="caseAnswer('m3c6s1',this,false)">C) Oui, et le changement est rétroactif au 1er janvier 2026</button>
<button class="step-opt" onclick="caseAnswer('m3c6s1',this,false)">D) Les seuils n’ont aucune importance</button>
</div>
<div class="step-explanation" id="m3c6s1-expl">La révision entrée en vigueur en 2025 a supprimé l’ancien automatisme fondé sur un dépassement ponctuel important. <strong>État 2026 :</strong> les limites doivent être dépassées pendant trois périodes fiscales consécutives pour imposer le changement. Une prévision 2026 au-dessus du seuil est donc un signal de suivi, pas à elle seule une bascule automatique au 01.01.2027. <div class="art-ref">📋 art. 37 LTVA · OTVA / pratique AFC TDFN actuelle</div></div>
</div>
<div class="case-step" id="m3c6s2">''','case6 threshold rewrite',1)
sub(r'<div class="case-step" id="m3c6s2">.*?</div>\n</div>\n<div class="case-step" id="m3c6s3">',
    '''<div class="case-step" id="m3c6s2">
<div class="step-question"><span class="step-q-num">Q2</span>Si La Trattoria passe ensuite valablement de TDFN à effective, quel traitement de principe s’applique aux biens encore présents ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,false)">A) Calculer automatiquement 8,1% sur toute la valeur comptable du stock</button>
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,true)">B) Déterminer la valeur résiduelle et l’impôt préalable qui n’avait pas été déduit sous TDFN; le dégrèvement ultérieur admissible se porte dans le premier décompte effectif, actuellement au ch. 410</button>
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,false)">C) Aucun dégrèvement n’est jamais possible</button>
<button class="step-opt" onclick="caseAnswer('m3c6s2',this,false)">D) Déduire le chiffre d’affaires TDFN du stock</button>
</div>
<div class="step-explanation" id="m3c6s2-expl">Le passage TDFN → effective peut ouvrir un <strong>dégrèvement ultérieur</strong> sur la valeur résiduelle des biens/services pour lesquels le DIP n’avait pas été déduit séparément sous TDFN. Le calcul exige les factures d’origine, la TVA grevant réellement les acquisitions, la valeur résiduelle et les règles de transition actuelles. Ce n’est donc pas « stock comptable × taux normal ». Le montant admissible se reporte au premier décompte effectif, actuellement au <strong>ch. 410</strong>. <div class="art-ref">📋 art. 37 LTVA · OTVA / pratique AFC TDFN · ch. 410 actuel</div></div>
</div>
<div class="case-step" id="m3c6s3">''','case6 relief rewrite',1)
rep('Les délais de changement ont fait l’objet de révisions et doivent être contrôlés dans l’OTVA / pratique AFC en vigueur. Le bon réflexe M03 est de vérifier la période minimale et le délai de demande <strong>avant</strong> de conseiller le passage.',
    'Depuis la réforme 2025, un changement de méthode peut en principe intervenir après <strong>une période fiscale complète</strong>, sous réserve des conditions et délais de demande applicables. Le bon réflexe reste de vérifier la pratique AFC de la période avant de conseiller le passage.',
    'case6 one-period change',1)

# Case 7: current interest calculation is verified, remove misleading "pedagogical only" tone
rep('Paiement effectué : 15.05.2026 (retard à calculer selon la convention de calcul donnée dans l’exercice)',
    'Paiement effectué : 15.05.2026 (retard à calculer selon la méthode commerciale 30/360)',1)
rep('Pour cet <strong>exercice pédagogique</strong>, l’énoncé fournit les taux 4,5% pour la portion 2025 et 4,0% pour la portion 2026. Dans un dossier réel, les taux doivent être contrôlés dans l’ordonnance DFF applicable.',
    'Taux vérifiés pour les périodes du cas : <strong>4,5% pour 2025</strong> et <strong>4,0% pour 2026</strong>. Pour des périodes ultérieures, contrôler l’ordonnance DFF en vigueur.',1)
t=t.replace('selon la convention de calcul donnée dans l’exercice','selon la méthode commerciale 30/360')
t=t.replace('convention pédagogique 30/360','méthode commerciale 30/360')

# Case 10 disclosure: clean current-law wording
rep('B) Auto-signalement complet chronologie à documenter et conditions légales à vérifier + collaboration AFC + paiement intégral des sommes dues',
    'B) Auto-signalement complet avant que l’AFC n’ait connaissance des faits concernés + collaboration complète + paiement des montants dus',1)
rep('Si le dossier présente un risque de soustraction, les conditions protectrices de l’art. 102 supposent un auto-signalement complet chronologie à documenter et conditions légales à vérifier, une collaboration avec l’AFC et le paiement intégral des sommes dues. Si l’effet net est nul, il s’agit au minimum d’une correction spontanée documentée ; l’AFC qualifiera ensuite la portée pénale éventuelle selon les circonstances.',
    'Si le dossier présente un risque de soustraction, l’art. 102 exige notamment un <strong>auto-signalement complet avant que l’AFC n’ait connaissance des faits concernés</strong>, ainsi qu’une collaboration complète et le paiement des montants dus. L’annonce d’un contrôle signifie en pratique que la spontanéité n’est en principe plus acquise pour les faits déjà visés. Si l’effet fiscal net est nul, une correction complète reste nécessaire; la portée pénale éventuelle dépend toujours du dossier.',
    'case10 disclosure clean',1)

# Error cards residual legal corrections
rep('Comparaison annuelle systématique (cas Marc Dubois M03 cas 2). Si découvert tardivement : attendre la fin du délai engagement, puis changer de méthode avec notification AFC. Correction d\'entrée sur stocks lors du passage TDFN → effective (art. 32 LTVA — favorable).',
    'Comparer régulièrement effective et TDFN. Si un changement est indiqué, vérifier le délai de demande et la période fiscale minimale. Lors du passage TDFN → effective, appliquer les règles actuelles de dégrèvement ultérieur sur la valeur résiduelle et, le cas échéant, le ch. 410 — pas une formule « stock × taux normal ».',
    'error3 transition',1)
rep('Le délai de 240 jours après clôture (art. 72 LTVA) expire sans dépôt du correction / concordance ePortal. Pour exercice 2025 clos le 31.12.2025 → délai 28.08.2026. Au-delà : l\'AFC peut considérer les décomptes périodiques comme définitifs (ATF 140 II 202). Toute correction ultérieure nécessite des motifs sérieux.',
    'La concordance n’est pas traitée dans la période contenant le 180e jour après la clôture et aucune rectification n’est transmise dans le repère pratique de 240 jours indiqué par l’AFC. Une correction découverte plus tard doit encore être examinée selon l’art. 43, la prescription et l’état de la créance fiscale.',
    'error4 timing',1)
rep('Discipline cabinet : <strong>checklist annuelle de clôture</strong> incluant la concordance. Délai de sécurité : déposer 3-4 mois avant les 240 jours (en juin/juillet pour clôture 31.12). Documentation : rapprochement comptable détaillé + liste des écarts identifiés. Si délai expiré et erreur significative : dénonciation spontanée art. 102.',
    'Discipline cabinet : <strong>checklist annuelle de clôture</strong>, identification de la période contenant le 180e jour et dépôt dans le délai du Portail AFC. Si une erreur est découverte plus tard : corriger fiscalement si la créance n’est pas définitive / prescrite et analyser séparément l’art. 102 uniquement si un risque pénal existe.',
    'error4 correction',1)
rep('L\'assujetti déclare la TVA collectée en méthode encaissement (art. 40) mais déduit l\'IP en méthode convenue (art. 39) — ou inversement.',
    'L’assujetti décompte les contre-prestations reçues selon l’art. 39 mais traite l’IP comme s’il appliquait le mode convenu — ou inversement.',
    'error5 art39',1)
rep('Audit interne des dates de naissance créance vs déduction IP. Aligner les deux méthodes via décompte rectificatif correction / concordance ePortal. Si passage formel d\'une méthode à l\'autre : demande à l\'AFC + correction d\'entrée sur créances clients et dettes fournisseurs (art. 39 al. 2 + 40 al. 2 LTVA).',
    'Auditer factures, encaissements et paiements puis corriger les périodes concernées. Lors d’un changement formel convenu ↔ reçu, appliquer les règles de transition LTVA/OTVA et documenter créances/dettes à la date de bascule afin d’éviter doubles déclarations ou omissions.',
    'error5 transition',1)
rep('Taux fixé par DFF RS 631.014 : taux DFF applicable à la période (4,5% en 2025, 4,75% en 2024). Seuil minimal de perception CHF 100 (art. 1 al. 3 Ord. DFF). Calcul selon la méthode commerciale 30/360 lorsque applicable.',
    'Le taux est fixé par le DFF et doit être lu pour chaque période. État vérifié au 06.09.2026 : 4,0% en 2026 et 4,5% en 2025. L’AFC utilise la méthode commerciale 30/360; les intérêts inférieurs à CHF 100 ne sont en principe pas perçus.',
    'error6 interest',1)
rep('Art. 102 al. 1 LTVA — conditions strictes : (1) vérification de toutes les conditions de l’art. 102, de la chronologie et de l’état de connaissance de l’autorité, (2) collaboration AFC, (3) paiement intégral. ATF 145 II 130 confirme la rigueur de la condition temporelle. Après annonce : l\'erreur découverte expose à l\'amende art. 96 (selon art. 96 du montant éludé).',
    'Art. 102 LTVA : l’effet pénal favorable suppose notamment que l’auto-signalement intervienne avant que l’AFC n’ait connaissance des faits concernés, puis une collaboration complète et le paiement des montants dus. Après annonce d’un contrôle portant sur ces faits, la spontanéité n’est en principe plus acquise; cela ne signifie toutefois pas qu’une amende est automatique — la faute et les éléments constitutifs restent à analyser.',
    'error7 disclosure',1)
rep('Anticipation : audit interne TVA annuel pour identifier les erreurs et déclencher la dénonciation avant tout contrôle. Si annonce déjà reçue : préparer une défense rigoureuse (démontrer bonne foi, négligence ordinaire et non grave, contester l\'extrapolation si justifié). Engager un avocat fiscaliste spécialisé.',
    'Mettre en place un audit TVA périodique afin de corriger rapidement les erreurs. Si un contrôle est déjà annoncé, coopérer, reconstituer les faits et analyser séparément la correction fiscale, la prescription et le risque pénal; un conseil spécialisé peut être requis selon l’enjeu.',
    'error7 response',1)
rep('Le dossier applique automatiquement « valeur des stocks × taux » au premier décompte effectif sans vérifier les règles de transition TDFN.',
    'Le dossier applique automatiquement « valeur comptable du stock × taux normal » au premier décompte effectif, au lieu de déterminer la valeur résiduelle et le DIP historiquement non déduit sous TDFN.',
    'error8 symptom',1)
rep('Documenter stocks, immobilisations, activités et date du changement; appliquer l’OTVA / pratique AFC actuelle relative au changement de méthode. L’art. 32 ne constitue pas à lui seul une autorisation de récupération automatique.',
    'Documenter biens/services encore présents, factures d’origine, TVA grevant les acquisitions et valeur résiduelle. En cas de passage TDFN → effective, appliquer le dégrèvement ultérieur admissible selon les règles actuelles et le reporter au premier décompte effectif, actuellement au ch. 410.',
    'error8 correction',1)

# QCM corrections
rep("q:'Quel formulaire utilise-t-on pour le décompte trimestriel standard ?',\n    opts:['Formulaire 100','correction / concordance ePortal','Formulaire 103','Formulaire 200'],\n    correct:0,\n    expl:'Le Formulaire 100 (décompte effectif) est le formulaire standard du décompte trimestriel/semestriel. Le correction / concordance ePortal est dédié à la concordance annuelle et aux décomptes rectificatifs (art. 72).'",
    "q:'Quel canal opérationnel utilise-t-on aujourd’hui pour remettre le décompte TVA standard ?',\n    opts:['Portail AFC · Décompte TVA pro','Un PDF Formulaire 100 à envoyer par e-mail','Un document Word libre','Aucun dépôt électronique'],\n    correct:0,\n    expl:'En état 2026, le décompte se remet via le Portail AFC, service Décompte TVA pro. Les anciens numéros de formulaires restent des repères historiques, mais le libellé du portail de la période est la référence opérationnelle.'",
    'q09 portal',1)
rep("expl:'Le taux TDFN intègre forfaitairement l\\'IP moyen de la branche (ex. 6,2% fiduciaires, 2,1% commerce, 5,3% restauration selon activité). Pas de déduction IP séparée — la formule est simplement CA brut TTC × taux TDFN = TVA nette due. Inconvénient majeur : si gros investissements ou achats lourds (IP réel élevé), la méthode effective devient plus favorable car elle permet la récupération réelle de l\\'IP. Avantage : simplicité administrative et gain de temps comptable considérable.'",
    "expl:'Le taux TDFN intègre forfaitairement le DIP et se détermine selon l’activité réellement exercée et la liste AFC en vigueur. Il n’y a pas de déduction séparée du DIP. Les investissements importants peuvent rendre l’effective plus favorable; il faut comparer les méthodes avec les taux attribués au client.'",
    'q13 rate examples',1)
sub(r"\{ id:'m03-q14'.*?\},\n  \{ id:'m03-q15'",
    "{ id:'m03-q14', diff:'med', art:'art. 39–40 LTVA',\n    q:'Quel est l’avantage principal du décompte selon les contre-prestations reçues ?',\n    opts:['Payer moins de TVA au total','Décaler la dette fiscale jusqu’à l’encaissement selon les règles applicables — utile lorsque les clients paient tard','Déduire le DIP deux fois','Éviter la concordance annuelle'],\n    correct:1,\n    expl:'Le choix du mode convenu/reçu relève de l’art. 39; l’art. 40 règle la naissance de la créance. Le mode reçu peut améliorer le cash-flow, mais doit être conservé au moins pendant une période fiscale complète et la comptabilité doit suivre les encaissements/paiements.'\n  },\n  { id:'m03-q15'",
    'q14 art39',1)
sub(r"\{ id:'m03-q17'.*?\},\n  \{ id:'m03-q18'",
    "{ id:'m03-q17', diff:'med', art:'art. 41 LTVA',\n    q:'Une créance déjà imposée en mode convenu devient définitivement irrécouvrable. Quel réflexe ?',\n    opts:['La TVA reste toujours définitivement due','Documenter la perte et traiter la modification ultérieure de la contre-prestation / dette fiscale selon l’art. 41 et la pratique AFC','Utiliser l’art. 27 comme règle générale des pertes sur débiteurs','Attendre 10 ans'],\n    correct:1,\n    expl:'Une perte sur débiteur peut modifier ultérieurement la contre-prestation. La correction repose sur l’art. 41 et la pratique AFC, avec preuve de l’irrécouvrabilité et écriture comptable cohérente. L’art. 27 concerne l’impôt facturé/mentionné à tort.'\n  },\n  { id:'m03-q18'",
    'q17 bad debt',1)
sub(r"\{ id:'m03-q18'.*?\},\n  \{ id:'m03-q19'",
    "{ id:'m03-q18', diff:'med', art:'art. 37 LTVA + pratique TDFN',\n    q:'Lors d’un passage TDFN → méthode effective, quel traitement est correct pour les biens encore présents ?',\n    opts:['Aucun DIP ne peut jamais être récupéré','Déterminer le dégrèvement ultérieur sur la valeur résiduelle et le DIP historiquement non déduit; le montant admissible se porte dans le premier décompte effectif, actuellement au ch. 410','Appliquer automatiquement 8,1% à toute valeur comptable du stock','Déduire le chiffre d’affaires TDFN'],\n    correct:1,\n    expl:'Le changement de méthode peut ouvrir un dégrèvement ultérieur, mais le calcul exige la TVA d’origine, la valeur résiduelle et les règles de transition. Ce n’est pas une formule « stock × taux normal ». En état actuel, le montant admissible est porté au ch. 410 du premier décompte effectif.'\n  },\n  { id:'m03-q19'",
    'q18 transition',1)
sub(r"\{ id:'m03-q21'.*?\},\n  \{ id:'m03-q22'",
    "{ id:'m03-q21', diff:'med', art:'art. 102 LTVA',\n    q:'Quel élément temporel est central pour l’effet favorable d’une dénonciation spontanée ?',\n    opts:['Le montant doit être inférieur à CHF 50’000','L’auto-signalement doit intervenir avant que l’AFC n’ait connaissance des faits concernés, avec collaboration complète et paiement des montants dus','L’erreur doit toujours être non intentionnelle','L’AFC doit donner son accord avant le signalement'],\n    correct:1,\n    expl:'L’art. 102 exige notamment que l’auto-signalement soit réellement spontané. Si l’AFC connaît déjà les faits — notamment après annonce d’un contrôle les visant — l’effet protecteur n’est en principe plus acquis. La faute et une éventuelle sanction restent néanmoins à analyser séparément.'\n  },\n  { id:'m03-q22'",
    'q21 disclosure',1)
sub(r"\{ id:'m03-q24'.*?\},\n  \{ id:'m03-q25'",
    "{ id:'m03-q24', diff:'med', art:'art. 35a LTVA',\n    q:'Pour le décompte annuel, quelle affirmation est correcte en état 2026 ?',\n    opts:['Il est automatique pour toute PME','Il est possible sous les conditions de l’art. 35a, notamment CA ≤ CHF 5’005’000 et comportement de remise/paiement conforme; effective/TaF ont 3 acomptes, TDFN 1 acompte','Il est réservé à la TDFN','Il supprime tout paiement intermédiaire'],\n    correct:1,\n    expl:'Le décompte annuel est une option encadrée. En état 2026, effective/TaF donnent lieu à trois acomptes et TDFN à un acompte; le décompte annuel régularise ensuite ces montants.'\n  },\n  { id:'m03-q25'",
    'q24 annual',1)
rep("expl:'TDFN : méthode simplifiée pour PME sous seuils AFC (CA imposable TVA comprise ≤ CHF 5\\'024\\'000 et impôt dû ≤ CHF 108\\'000). TaF : méthode forfaitaire pour certaines collectivités publiques/NPO selon les règles AFC. Les deux sont en principe semestrielles.'",
    "expl:'TDFN : méthode simplifiée pour PME sous seuils AFC, normalement semestrielle. TaF : méthode forfaitaire pour les catégories d’entités admises, normalement trimestrielle. Les deux restent soumises à la qualification correcte des activités.'",
    'q25 period',1)
sub(r"\{ id:'m03-q26'.*?\},\n  \{ id:'m03-q27'",
    "{ id:'m03-q26', diff:'hard', art:'art. 37 LTVA + OTVA / pratique AFC',\n    q:'Après combien de temps un changement de méthode peut-il en principe être envisagé selon les règles actuelles ?',\n    opts:['Après une période fiscale complète, sous réserve des conditions et délais de demande','Toujours après exactement 3 ans','Uniquement après 10 ans','Jamais'],\n    correct:0,\n    expl:'Depuis la réforme 2025, les anciennes durées rigides ont été assouplies. Le changement peut en principe être demandé après une période fiscale complète, en respectant les conditions et délais de la pratique AFC.'\n  },\n  { id:'m03-q27'",
    'q26 change period',1)
sub(r"\{ id:'m03-q27'.*?\},\n  \{ id:'m03-q28'",
    "{ id:'m03-q27', diff:'hard', art:'art. 42 LTVA',\n    q:'Dans quel cas la prescription fiscale est-elle suspendue selon l’art. 42 al. 4 ?',\n    opts:['Pendant toute réclamation ordinaire','Lorsqu’une procédure pénale fiscale est pendante et que l’assujetti en a été informé','À chaque appel téléphonique de l’AFC','Jamais'],\n    correct:1,\n    expl:'L’art. 42 distingue interruption et suspension. La suspension visée à l’al. 4 concerne notamment la procédure pénale fiscale notifiée; une simple réclamation/recours ne doit pas être mémorisée comme règle générale de suspension.'\n  },\n  { id:'m03-q28'",
    'q27 prescription suspension',1)
sub(r"\{ id:'m03-q28'.*?\},\n  \{ id:'m03-q29'",
    "{ id:'m03-q28', diff:'hard', art:'art. 42 + 78 LTVA',\n    q:'Quelles périodes l’AFC peut-elle contrôler ?',\n    opts:['Toujours exactement les 5 dernières années','Les périodes closes non prescrites, à déterminer selon l’art. 42 et la chronologie du dossier','Toujours 10 ans en cas d’erreur','Uniquement la dernière année'],\n    correct:1,\n    expl:'L’art. 78 organise le contrôle, mais l’étendue temporelle dépend des périodes non prescrites. Il faut appliquer l’art. 42, y compris interruptions, suspensions et prescription absolue, plutôt que mémoriser une règle « 5/10 ans ».'\n  },\n  { id:'m03-q29'",
    'q28 control periods',1)
sub(r"\{ id:'m03-q31'.*?\},\n  \{ id:'m03-q32'",
    "{ id:'m03-q31', diff:'hard', art:'contrôle / estimation LTVA',\n    q:'Lors d’un contrôle, une estimation ou extrapolation à partir d’un échantillon est-elle automatique ?',\n    opts:['Oui, toute erreur est multipliée par cinq','Non — la méthode doit être représentative, défendable et limitée aux périodes juridiquement ouvertes','Oui, même si les activités ont changé','Jamais possible'],\n    correct:1,\n    expl:'Une estimation n’est pas une multiplication mécanique d’un écart. Il faut examiner la qualité des données, la comparabilité des périodes et la représentativité de l’échantillon; l’assujetti peut documenter les différences entre périodes.'\n  },\n  { id:'m03-q32'",
    'q31 estimation',1)
sub(r"\{ id:'m03-q34'.*?\},\n  \{ id:'m03-q35'",
    "{ id:'m03-q34', diff:'hard', art:'art. 33 LTVA',\n    q:'Une subvention visée par l’art. 33 affecte le DIP. Quelle méthode est professionnelle ?',\n    opts:['Appliquer toujours subvention / (subvention + CA total)','Qualifier la contribution, affecter directement les coûts puis appliquer une méthode objective / simplification AFC admise aux coûts communs','Supprimer tout le DIP','Ignorer la subvention'],\n    correct:1,\n    expl:'L’art. 33 peut imposer une réduction du DIP, mais il n’existe pas de prorata universel dans M03. L’affectation directe vient d’abord; la méthode détaillée pour les coûts communs est traitée en M05.'\n  },\n  { id:'m03-q35'",
    'q34 subsidy',1)
sub(r"\{ id:'m03-q35'.*?\}\n\];",
    "{ id:'m03-q35', diff:'hard', art:'art. 102 LTVA',\n    q:'Une dénonciation spontanée déposée après l’annonce d’un contrôle portant sur les faits concernés garantit-elle l’absence d’amende ?',\n    opts:['Oui — toujours','Non — la spontanéité n’est en principe plus acquise lorsque l’AFC connaît déjà les faits; une sanction éventuelle doit néanmoins être analysée selon la faute et les éléments constitutifs','Oui si le montant est faible','Oui si l’amende n’a pas encore été notifiée'],\n    correct:1,\n    expl:'L’art. 102 protège une véritable auto-dénonciation spontanée. Si l’AFC a déjà connaissance des faits, notamment via un contrôle annoncé les visant, l’effet protecteur n’est en principe plus disponible. Cela ne rend toutefois pas l’amende automatique.'\n  }\n];",
    'q35 disclosure',1)

# Flashcards residuals
rep("def:'<strong>Réservée</strong> aux collectivités publiques, organisations sans but lucratif (NPO), institutions d\\'utilité publique, paroisses, hôpitaux. <strong>Aucun plafond</strong> de CA ou de dette fiscale. Plusieurs taux forfaitaires peuvent être possibles selon les activités et la pratique applicable. Périodicité semestrielle. Logique similaire au TDFN mais adaptée aux structures non commerciales.'",
    "def:'Méthode réservée aux catégories d’assujettis admises par l’art. 37 al. 5 et la pratique AFC (notamment collectivités publiques et certaines institutions/organisations). Plusieurs taux peuvent être nécessaires. <strong>Périodicité ordinaire : trimestrielle.</strong> Toujours vérifier l’éligibilité concrète de l’entité.'",
    'fc03 taf',1)
rep("term:'Convenue (art. 39) vs Encaissement (art. 40)',\n    def:'<strong>Convenue</strong> (défaut) : TVA due à la date de la facture. <strong>Encaissement</strong> (option) : TVA due à l\\'encaissement effectif. Cohérence obligatoire TVA / IP. Encaissement idéal pour BTP, B2B avec DSO long. Engagement 1 an. Récupération TVA art. 27 si créance irrécouvrable (uniquement en convenue).'",
    "term:'Contre-prestations convenues vs reçues (art. 39; effets art. 40)',\n    def:'<strong>Convenues</strong> : traitement lié aux factures. <strong>Reçues</strong> : traitement lié aux encaissements/paiements selon autorisation. Le choix se fait selon l’art. 39 et doit être maintenu au moins une période fiscale complète; l’art. 40 règle le moment de la créance. Une créance irrécouvrable en mode convenu se traite selon l’art. 41, pas l’art. 27.'",
    'fc04 art39',1)
rep("def:'<strong>Trimestrielle</strong> : méthode effective (défaut). 4 décomptes/an. <strong>Semestrielle</strong> : TDFN/TaF (défaut). 2 décomptes/an. <strong>Annuelle</strong> : option si CA ≤ CHF 5\\'005\\'000 + historique de remise/paiement dans les délais + demande via Portail AFC. 1 décompte + 3 acomptes trimestriels. <strong>Mensuelle</strong> (rare) : crédit IP récurrent (exportateurs, startups).'",
    "def:'<strong>Trimestrielle</strong> : effective et TaF en règle générale. <strong>Semestrielle</strong> : TDFN en règle générale. <strong>Annuelle</strong> : option art. 35a si conditions remplies; état 2026, 3 acomptes pour effective/TaF et 1 pour TDFN. <strong>Mensuelle</strong> : possible notamment en cas de crédit d’impôt récurrent selon conditions AFC.'",
    'fc05 periods',1)
rep("def:'<strong>Prescription relative</strong> : 5 ans dès naissance créance (art. 42 al. 1). <strong>Absolue</strong> : 10 ans (al. 6). <strong>Droit contrôle AFC</strong> : 5 ans, étendu à 10 ans en soustraction (art. 78). <strong>Conservation documents</strong> : 10 ans (20 ans immobilier — art. 70). Suspension prescription pendant procédures de recours (art. 42 al. 4).'",
    "def:'<strong>Prescription relative</strong> : 5 ans selon l’art. 42; interruption par les actes prévus par la loi et prescription absolue de 10 ans. Le contrôle porte sur les périodes closes non prescrites. La suspension de l’art. 42 al. 4 doit être appliquée selon ses conditions, notamment en matière de procédure pénale fiscale. Conservation documentaire : vérifier l’art. 70 selon le type de pièce.'",
    'fc08 prescription',1)
rep("def:'<strong>Ch. 405</strong> = correction IP affecté directement à activité exclue art. 21 (art. 30 LTVA — affectation directe). <strong>Ch. 410</strong> = réduction DIP pour subventions hors champ (art. 33 — prorata = subvention / (subvention + CA total)). Ces corrections sont systématiquement vérifiées par l\\'AFC en contrôle.'",
    "def:'Repères actuels : <strong>ch. 400</strong> = DIP sur matériel/prestations de services; <strong>405</strong> = DIP sur investissements et autres charges d’exploitation; <strong>410</strong> = dégrèvement ultérieur; <strong>415</strong> = corrections du DIP; <strong>420</strong> = réductions du DIP, notamment art. 33. Le montant au ch. 420 dépend de l’affectation/méthode appropriée — pas d’un prorata universel.'",
    'fc11 boxes',1)
rep("term:'Intérêts moratoires 2026 — Calcul',\n    def:'<strong>Taux 2026 : 4,0%/an</strong> (DFF RS 631.014). Évolution : 2024 : 4,75% · 2025 : 4,5% · 2026 : 4,0%. Départ : lendemain de l\\'échéance. Calcul : montant × taux × jours commerciaux/360. <strong>Seuil minimal de perception : CHF 100</strong> (art. 1 al. 3 Ord. DFF). Exemple : CHF 50\\'000 × 4,0% × 6 mois = CHF 1\\'000.'",
    "term:'Intérêts — état 2026 et méthode',\n    def:'État vérifié au 06.09.2026 : <strong>4,0% en 2026</strong> et 4,5% en 2025. L’AFC calcule commercialement 30/360; les intérêts inférieurs à CHF 100 ne sont en principe pas perçus/versés. Pour toute période future, recontrôler l’ordonnance DFF.'",
    'fc13 interest',1)
rep("def:'<strong>Conditions cumulatives</strong> (ATF 145 II 130) : (1) auto-signalement complet <strong>AVANT</strong> toute annonce de contrôle AFC, (2) collaboration au calcul exact, (3) paiement intégral TVA + intérêts moratoires. <strong>Effet</strong> : exempt d\\'amende art. 96 (selon art. 96). N\\'évite PAS le rappel TVA ni les intérêts moratoires. Outil principal de régularisation.'",
    "def:'L’effet favorable suppose notamment un auto-signalement complet <strong>avant que l’AFC n’ait connaissance des faits concernés</strong>, une collaboration complète et le paiement des montants dus. Après annonce d’un contrôle visant ces faits, la spontanéité n’est en principe plus acquise. Une éventuelle sanction doit néanmoins être analysée selon la faute et les éléments constitutifs.'",
    'fc14 disclosure',1)
rep("term:'ePortal AFC — Obligation depuis 2025',\n    def:'<strong>Depuis 01.01.2025</strong> (art. 71a LTVA) : dépôt obligatoire via ePortal AFC (eportal.admin.ch). Identification via <strong>AGOV</strong> (anciennement CH-LOGIN). Tous formulaires (100, 550_03) déposés électroniquement. Papier n\\'est plus admis pour les assujettis standards. Exceptions sur dérogation expresse de l\\'AFC.'",
    "term:'Portail AFC · Décompte TVA pro',\n    def:'En état 2026, le canal opérationnel est le <strong>Portail AFC · Décompte TVA pro</strong>. L’ancien service Décompte TVA easy a été supprimé en mai 2026. Les libellés et écrans du portail de la période priment sur les anciens numéros de formulaires.'",
    'fc15 portal',1)
sub(r"\{ id:'fc16'.*?\}\n\];",
    "{ id:'fc16', cat:'proc', catLabel:'Intérêts &amp; procédure',\n    term:'Contrôle — estimation / extrapolation',\n    def:'Une estimation n’est pas une multiplication automatique d’un écart d’une année. Vérifier représentativité de l’échantillon, comparabilité des périodes, qualité des données et prescription. Le dossier doit documenter les différences qui rendent une extrapolation injustifiée ou nécessitent un autre calcul.',\n    art:'art. 42 + contrôle LTVA'\n  }\n];",
    'fc16 estimation',1)

# Cheatsheet: replace brittle rate list and correct period/form/interest/mode/disclosure blocks
sub(r'<div class="cheat-card">\n<span class="cheat-title">3 — Taux TDFN.*?</div>\n</div>',
    '''<div class="cheat-card">
<span class="cheat-title">3 — TDFN : attribuer le bon taux</span>
<div class="cheat-body"><ol><li>Identifier les activités réellement exercées.</li><li>Vérifier l’éligibilité TDFN et les seuils de la période.</li><li>Utiliser la liste / pratique AFC actuelle pour attribuer le ou les taux.</li><li>Appliquer la règle des 10% et la séparation comptable des activités lorsqu’elle est pertinente.</li><li>Ne jamais mémoriser « branche = taux » depuis une ancienne cheatsheet.</li></ol></div>
</div>''','cheat tdfn rates',1)
sub(r'<div class="cheat-card">\n<span class="cheat-title">4 — Périodes et délais clés</span>.*?</div>\n</div>',
    '''<div class="cheat-card">
<span class="cheat-title">4 — Périodes et délais clés</span>
<div class="cheat-body"><ul><li><strong>Effective / TaF</strong> : trimestriel en règle générale.</li><li><strong>TDFN</strong> : semestriel en règle générale.</li><li><strong>Annuel art. 35a</strong> : état 2026, CA ≤ CHF 5’005’000 + conditions de conformité; 3 acomptes effective/TaF, 1 TDFN.</li><li><strong>Remise / paiement</strong> : 60 jours après fin de période, sauf échéance spéciale affichée par le portail.</li><li><strong>Concordance</strong> : période contenant le 180e jour après clôture; l’AFC utilise aussi le repère pratique de 240 jours.</li><li><strong>Prescription</strong> : calculer selon art. 42, interruptions/suspensions comprises.</li></ul></div>
</div>''','cheat periods',1)
rep('<span class="cheat-title">5 — Chiffres décompte clés (Formulaire 100)</span>',
    '<span class="cheat-title">5 — Chiffres clés du Décompte TVA pro (repères actuels)</span>',1)
sub(r'<div class="cheat-card">\n<span class="cheat-title">6 — Intérêts 2026.*?</div>\n</div>',
    '''<div class="cheat-card">
<span class="cheat-title">6 — Intérêts — état 2026</span>
<div class="cheat-body"><ul><li><strong>2026 : 4,0%</strong> · 2025 : 4,5% (état vérifié 06.09.2026).</li><li>Calcul AFC : méthode commerciale 30/360.</li><li>Les intérêts inférieurs à <strong>CHF 100</strong> ne sont en principe pas perçus/versés.</li><li>Pour une période future ou un dossier multi-années : vérifier le taux DFF de chaque période.</li></ul></div>
</div>''','cheat interest',1)
sub(r'<div class="cheat-card">\n<span class="cheat-title">7 — Méthode convenue vs encaissement</span>.*?</div>\n</div>',
    '''<div class="cheat-card">
<span class="cheat-title">7 — Contre-prestations convenues vs reçues</span>
<div class="cheat-body"><p><strong>Art. 39</strong> : choix du mode convenu/reçu; maintien au moins une période fiscale complète. <strong>Art. 40</strong> : naissance de la créance fiscale.</p><ul><li>Convenu : suivi par factures.</li><li>Reçu : suivi par encaissements/paiements, sur autorisation.</li><li>Créance irrécouvrable en mode convenu : modification ultérieure selon <strong>art. 41</strong>, avec preuve.</li><li>Changement de mode : appliquer les règles de transition et documenter créances/dettes.</li></ul></div>
</div>''','cheat art39',1)
sub(r'<div class="cheat-card">\n<span class="cheat-title">8 — Checklist concordance \+ dénonciation</span>.*?</div>\n</div>',
    '''<div class="cheat-card">
<span class="cheat-title">8 — Checklist concordance + correction spontanée</span>
<div class="cheat-body"><p><strong>Concordance art. 72</strong></p><ol><li>Rapprocher comptabilité, journaux TVA et décomptes.</li><li>Identifier la période contenant le 180e jour après la clôture.</li><li>Documenter chaque écart et corriger dans le Portail AFC.</li><li>Contrôler intérêts / échéances avec les taux de la période.</li></ol><p><strong>Art. 102</strong></p><ul><li>Analyser séparément correction fiscale et effet pénal.</li><li>Pour l’effet favorable : auto-signalement avant connaissance des faits par l’AFC, collaboration complète et paiement des montants dus.</li><li>Après annonce d’un contrôle visant les faits, la spontanéité n’est en principe plus acquise; aucune amende ne doit toutefois être présumée automatiquement.</li></ul></div>
</div>''','cheat disclosure',1)

# Audit note: record targeted current-source verification
rep('Le module a été révisé pour supprimer les automatismes dangereux : art. 39/40, créances irrécouvrables, périodicité TaF, changement TDFN, subventions/DIP, prescription/contrôle et taux d’intérêt volatils. Pour les <strong>numéros de rubriques ePortal, taux TDFN et taux d’intérêt</strong>, la source officielle de la période reste prioritaire sur tout mémo pédagogique.',
    'Contrôle ciblé effectué le <strong>06.09.2026</strong> contre les sources AFC/Fedlex actuelles pour : périodicité TDFN/TaF, changements de méthode dès 2025, décompte annuel art. 35a et ses acomptes, Portail AFC · Décompte TVA pro, taux d’intérêt 2025/2026, art. 39–41, art. 42/78 et cartographie actuelle des chiffres du décompte. Les taux TDFN, taux d’intérêt et écrans du portail restent <strong>datés</strong> : les recontrôler pour toute période future.',
    'audit note current verification',1)

# Clean remaining specific stale phrases globally
cleanup={
    'Formulaire 100 AFC':'Décompte TVA pro',
    'Formulaire 100':'Décompte TVA pro',
    'méthode encaissement (art. 40)':'mode selon les contre-prestations reçues (art. 39; effets art. 40)',
    'méthode encaissement art. 40':'mode selon les contre-prestations reçues (art. 39; effets art. 40)',
    'Récupération TVA art. 27 si créance irrécouvrable':'Correction selon art. 41 si créance irrécouvrable',
    'Droit contrôle AFC</strong> : 5 ans, étendu à 10 ans en soustraction (art. 78)':'Contrôle AFC</strong> : périodes closes non prescrites, à déterminer selon art. 42 + 78',
}
for a,b in cleanup.items():
    if a in t:
        t=t.replace(a,b); changes.append('cleanup:'+a[:25])

# Explicit sanity substitutions for any universal subsidy ratio remnants in didactic statements
t=t.replace('Prorata = subvention / (subvention + CA total générant DIP). Réduction au ch. 420. Exemple : subvention CHF 100\'000 + CA imposable CHF 1\'900\'000 → prorata = 100/2000 = 5% → IP commun réduit de 5%.',
            'Le ch. 420 reçoit la réduction déterminée selon l’art. 33. Commencer par l’affectation directe puis utiliser une méthode objective / simplification AFC admise pour les coûts communs; aucun prorata universel ne doit être appliqué par réflexe.')

p.write_text(t,encoding='utf-8')
print('Applied second-pass changes:',len(changes))
for c in changes: print(' -',c)
