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
        if required:
            raise SystemExit('Missing required: '+label)
        return
    t=t.replace(old,new)
    changes.append((label,n))

def sub(pattern,repl,label,count=0,flags=re.S,required=False):
    global t
    t2,n=re.subn(pattern,repl,t,count=count,flags=flags)
    if not n:
        print('WARN regex missing',label)
        if required:
            raise SystemExit('Missing required regex: '+label)
        return
    t=t2
    changes.append((label,n))

# ------------------------------------------------------------------
# Product / pedagogy / UX
# ------------------------------------------------------------------
rep('<span class="sidebar-version">v4.5</span>','<span class="sidebar-version">v5.0</span>','visible sidebar version',True)
rep('<span class="version-badge">v4.5 — Dossier DIP premium</span>','<span class="version-badge">v5.0 — DIP &amp; corrections</span>','visible top version',True)
rep('<div class="hero-title">DIP — Le cœur de la TVA suisse</div>',
    '<h1 class="hero-title">DIP — Déduire, affecter, corriger et défendre l’impôt préalable</h1>',
    'semantic h1',True)
rep("<div class=\"hero-desc\">La déduction de l'impôt préalable (DIP) est le mécanisme central qui assure la <strong>neutralité TVA</strong> pour les entreprises assujetties (ATF 123 II 295). Comprendre le DIP, c'est maîtriser le pivot entre la collecte (ventes) et la déduction (achats). Module à risque ÉLEVÉ : sujet de prédilection des contrôles AFC et des questions d'examen professionnel.</div>",
    "<div class=\"hero-desc\">Le M05 transforme une facture fournisseur en une décision TVA défendable : <strong>quel impôt préalable existe, quand le droit naît, à quelle activité la dépense est affectée, quelle correction ou réduction appliquer et quelle preuve conserver</strong>. L’objectif n’est pas de maximiser mécaniquement le DIP, mais de déterminer le montant juridiquement admissible et traçable.</div>",
    'hero description')

objectives='''<div class="theory-block">
<h3><span class="num">✓</span>Objectifs professionnels de M05 <span class="block-risk risk-red">🔴 Compétence centrale</span></h3>
<p class="prose">À la fin de M05, vous devez pouvoir traiter un dossier DIP sans confondre <strong>droit à déduction, preuve, double affectation, prestation à soi-même, dégrèvement ultérieur et réduction liée aux subventions</strong>.</p>
<table class="comp-table">
<thead><tr><th>Vous devez savoir</th><th>Réflexe attendu</th></tr></thead>
<tbody>
<tr><td>Identifier la source de l’impôt préalable</td><td>art. 28 / 28a : opération suisse, acquisition, importation, impôt préalable fictif</td></tr>
<tr><td>Sécuriser le droit et la preuve</td><td>art. 28–29 + art. 81 al. 3 : substance, affectation, pièces et liberté des moyens de preuve</td></tr>
<tr><td>Traiter une utilisation mixte</td><td>art. 30 + OTVA 65–68 : affectation réelle et méthode appropriée, pas un prorata universel</td></tr>
<tr><td>Traiter les fonds publics</td><td>art. 33 + OTVA 75 : identifier l’affectation de la subvention avant de choisir la clé</td></tr>
<tr><td>Suivre un changement d’usage</td><td>art. 31–32 : valeur résiduelle, 1/5 mobilier/services, 1/20 immobilier</td></tr>
<tr><td>Produire un dossier défendable</td><td>pièce → écriture → affectation → décompte → note de calcul / preuve</td></tr>
</tbody>
</table>
<div class="box info"><div class="box-icon">🧭</div><div class="box-body"><div class="box-title">Limite pédagogique</div><p>M05 traite le <strong>DIP et ses corrections</strong>. Les lieux de prestation sont approfondis en M06, les holdings en M07, l’immobilier en M08 et la procédure de contrôle / droit pénal en M11. Lorsqu’un cas dépend d’un de ces domaines, M05 apprend à reconnaître la dépendance et à documenter le point à vérifier.</p></div></div>
</div>
'''
rep('<!-- ATELIER — Checklist DIP -->',objectives+'<!-- ATELIER — Checklist DIP -->','objectives insert',True)

rep('<div class="sidebar-footer">\n<a class="btn-home" href="index.html">← Retour au cours</a>\n</div>',
    '<div class="sidebar-footer">\n<a class="btn-home" href="index.html">← Retour au cours</a>\n<div style="font-size:10px;line-height:1.5;color:rgba(255,255,255,.45);text-align:center;margin-top:9px">Conception : <a href="https://www.linkedin.com/in/mariia-lobur/" target="_blank" rel="noopener noreferrer" style="color:var(--gold)">Mariia Lobur</a> · <a href="https://github.com/mariialobur" target="_blank" rel="noopener noreferrer" style="color:var(--gold)">GitHub</a></div>\n</div>',
    'sidebar author',True)

# Remove a dangerous universal subsidy mini-formula from the opening dossier.
rep("<strong>4. Subvention publique</strong> : CHF 20’000 → ch. 900 ; si IP commun CHF 3’000 et base économique totale CHF 200’000, réduction indicative = 3’000 × 20’000 / 200’000 = CHF 300 → ch. 420.<br/>",
    "<strong>4. Subvention publique</strong> : CHF 20’000 → mouvement de fonds à qualifier ; déterminer d’abord <strong>quel projet / domaine / déficit</strong> elle finance, puis calculer la réduction du DIP sur les dépenses concernées selon art. 33 LTVA et art. 75 OTVA → ch. 420 si une réduction est due.<br/>",
    'opening subsidy formula')

# ------------------------------------------------------------------
# Art. 28 / 28a — sources of input tax
# ------------------------------------------------------------------
old_table='''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Les 5 types d'IP déductibles (art. 28 al. 1)</h4>
<table class="comp-table">
<thead><tr><th>Type d'IP</th><th>Référence</th><th>Chiffre décompte</th></tr></thead>
<tbody>
<tr><td>IP sur prestations imposables par d'autres assujettis (factures CH)</td><td class="art-cell">art. 28 al. 1 let. a</td><td>ch. 400</td></tr>
<tr><td>IP sur acquisitions étrangères auto-imposées (art. 45)</td><td class="art-cell">art. 28 al. 1 let. b</td><td>Impôt dû : ch. 383 ; IP éventuel : ch. 400/405 selon nature</td></tr>
<tr><td>IP sur importation de biens (TVA douanière OFDF)</td><td class="art-cell">art. 28 al. 1 let. c</td><td>ch. 400/405 selon nature de l’achat</td></tr>
<tr><td>IP fictif sur reprise de stocks (achat occasion à non-assujetti)</td><td class="art-cell">art. 28 al. 2-3</td><td>ch. 400</td></tr>
<tr><td>Correction de l’IP / prestation à soi-même (art. 31)</td><td class="art-cell">art. 31 LTVA</td><td>ch. 415</td></tr>
</tbody>
</table>'''
new_table='''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Sources de l’impôt préalable — ne pas mélanger art. 28, 28a et corrections</h4>
<table class="comp-table">
<thead><tr><th>Source</th><th>Référence</th><th>Réflexe pratique</th></tr></thead>
<tbody>
<tr><td>Impôt suisse facturé par un autre assujetti</td><td class="art-cell">art. 28 al. 1 let. a</td><td>Vérifier droit, affectation et preuve ; ch. 400/405 selon nature</td></tr>
<tr><td>Impôt déclaré sur les acquisitions</td><td class="art-cell">art. 28 al. 1 let. b</td><td>Impôt dû au ch. 383 ; DIP éventuel au ch. 400/405 si admis</td></tr>
<tr><td>Impôt sur les importations acquitté ou dû</td><td class="art-cell">art. 28 al. 1 let. c</td><td>Preuve OFDF + affectation ; ch. 400/405 selon nature</td></tr>
<tr><td>Produits agricoles / sylvicoles / horticoles, bétail ou lait acquis auprès de certains fournisseurs non assujettis</td><td class="art-cell">art. 28 al. 2</td><td>Déduction légale spécifique au taux prévu par la loi ; ne pas confondre avec l’IP fictif</td></tr>
<tr><td>Impôt préalable fictif sur un bien mobilier identifiable acquis sans TVA répercutée, si les conditions sont remplies</td><td class="art-cell">art. 28a</td><td>Vérifier bien identifiable et exclusions (notamment marge / cas OTVA) avant déduction</td></tr>
</tbody>
</table>
<div class="box warning"><div class="box-icon">⚠️</div><div class="box-body"><div class="box-title">Art. 31 n’est pas une « cinquième source de DIP »</div><p>L’art. 31 règle la <strong>prestation à soi-même</strong> lorsque les conditions de la déduction cessent d’être remplies. L’art. 32 règle le <strong>dégrèvement ultérieur</strong> lorsque ces conditions sont remplies plus tard. Ce sont des mécanismes de correction dans le temps, pas des catégories supplémentaires de l’art. 28.</p></div></div>'''
rep(old_table,new_table,'art28 table',True)

# Replace over-strong old-law jurisprudence slogan near art.28.
rep('<div class="box-title">Lien intime entre IP et activité imposable (ATF 132 II 353)</div>\n<p>L\'IP n\'est déductible que s\'il existe un <strong>lien direct entre la dépense et l\'activité économique imposable</strong>. Cette jurisprudence fondatrice du Tribunal fédéral (ATF 132 II 353) impose à l\'assujetti de démontrer ce lien. Une dépense purement privée, ou sans rapport avec l\'activité, n\'ouvre <strong>aucun</strong> droit au DIP, même si la facture est conforme.</p>',
    '<div class="box-title">Affectation entrepreneuriale et droit au DIP</div>\n<p>Le point de départ actuel est l’<strong>art. 28 LTVA</strong> : l’impôt préalable est déductible dans le cadre de l’activité entrepreneuriale, sous réserve notamment des art. 29 et 33. Une dépense privée ou affectée à une prestation ne donnant pas droit au DIP doit être exclue ou corrigée. En cas de litige, l’assujetti supporte le fardeau de la preuve pour les faits qui diminuent l’impôt.</p>',
    'remove direct-link slogan')

# ------------------------------------------------------------------
# Invoice / proof — current law is not a one-document formalism
# ------------------------------------------------------------------
start=t.find('<!-- BLOC 2 — Conditions matérielles et formelles -->')
end=t.find('<!-- BLOC 3 — Facture et IP récupérable -->',start)
if start!=-1 and end!=-1:
    block='''<!-- BLOC 2 — Droit et preuve -->
<div class="theory-block">
<h3><span class="num">2</span>Droit au DIP &amp; preuve — art. 26, 28–29 et 81 al. 3 <span class="block-risk risk-orange">🟠 Orange</span></h3>
<div class="box fidu"><div class="box-icon">💼</div><div class="box-body"><div class="box-title">Réalité fiduciaire</div><p>Une facture bien établie est la meilleure pièce de départ, mais le droit suisse actuel ne fonctionne pas selon « une mention manque = DIP automatiquement perdu ». Il faut distinguer <strong>les exigences de facturation de l’art. 26</strong>, <strong>les conditions matérielles des art. 28–29</strong> et <strong>la liberté des moyens de preuve de l’art. 81 al. 3</strong>.</p></div></div>
<table class="comp-table"><thead><tr><th>Question</th><th>Base</th><th>Contrôle</th></tr></thead><tbody>
<tr><td>L’impôt préalable existe-t-il ?</td><td class="art-cell">art. 28 / 28a</td><td>Impôt suisse facturé, acquisition, importation ou IP fictif admis</td></tr>
<tr><td>La dépense appartient-elle à l’activité entrepreneuriale ?</td><td class="art-cell">art. 28–30</td><td>Identifier affectation imposable, étrangère ouvrant droit, exclue ou privée</td></tr>
<tr><td>Existe-t-il une exclusion ou réduction ?</td><td class="art-cell">art. 29 / 33</td><td>Prestations exclues, fonds publics, autres limitations</td></tr>
<tr><td>Le droit est-il né dans cette période ?</td><td class="art-cell">art. 40</td><td>Selon contre-prestations convenues ou reçues</td></tr>
<tr><td>Le dossier prouve-t-il le fait fiscal ?</td><td class="art-cell">art. 26 + 81 al. 3</td><td>Facture, contrat, paiement, livraison/prestation, registre TVA, correspondance, données comptables</td></tr>
</tbody></table>
<div class="box info"><div class="box-icon">🧾</div><div class="box-body"><div class="box-title">Art. 26 — facture : ce qu’il faut contrôler</div><p>La facture doit permettre d’identifier clairement fournisseur, destinataire et prestation et mentionne en règle générale le statut / numéro TVA du fournisseur, le destinataire, la date ou période de prestation, la nature / étendue, la contre-prestation ainsi que le taux et l’impôt. Pour un ticket de caisse, le destinataire peut être omis jusqu’au seuil fixé par le Conseil fédéral. Une lacune doit être <strong>corrigée ou compensée par un dossier de preuve suffisant</strong>, pas transformée automatiquement en refus du DIP.</p></div></div>
<div class="box gold"><div class="box-icon">⭐</div><div class="box-body"><div class="box-title">Checklist 30 secondes</div><ul><li>✓ fournisseur et statut TVA plausibles ; vérifier le registre IDE en cas de doute</li><li>✓ prestation réellement reçue et décrite de façon vérifiable</li><li>✓ destinataire / activité de l’entreprise identifiables</li><li>✓ base, taux et montant de TVA arithmétiquement cohérents</li><li>✓ paiement / naissance du droit cohérents avec la méthode de décompte</li><li>✓ affectation documentée : déductible, non déductible ou mixte</li></ul></div></div>
<div class="box afc"><div class="box-icon">🏛️</div><div class="box-body"><div class="box-title">Liberté des moyens de preuve</div><p>L’art. 81 al. 3 interdit de faire dépendre l’acceptation d’une preuve <strong>exclusivement d’un moyen précis</strong>. L’AFC apprécie l’ensemble des preuves. Le fardeau de la preuve du DIP reste toutefois à l’assujetti : une facture corrigée et une piste d’audit propre restent la stratégie la plus sûre.</p></div></div>
</div>
'''
    t=t[:start]+block+t[end:]
    changes.append(('rebuild proof/invoice block',1))
else:
    raise SystemExit('Missing invoice block boundaries')

rep("<div class=\"formula-note\">Toujours <strong>arrondir au centime</strong> sur la facture finale (art. 24 al. 1 LTVA). Les arrondis cumulés sont admis dans les ERP modernes.</div>",
    "<div class=\"formula-note\">Appliquer une règle d’arrondi cohérente avec la facture et l’ERP, puis réconcilier base, taux et taxe. <strong>L’art. 24 règle la base de calcul de l’impôt</strong> ; il ne crée pas une règle universelle « toujours arrondir au centime ».</div>",
    'rounding note')
rep("Justificatifs : <strong>quittance e-dec ou décision de taxation OFDF</strong>. Inscription au ch. 400 du décompte.",
    "Justificatif : <strong>décision / quittance OFDF ou preuve électronique disponible dans le système douanier applicable</strong>. La rubrique de DIP dépend ensuite de la nature de l’achat (ch. 400/405).",
    'import proof')

# ------------------------------------------------------------------
# Art. 30 — mixed use: no universal turnover key, no art.39 method lock
# ------------------------------------------------------------------
old_formula='''<div class="formula-box">
<div class="formula-title">🧮 Formules art. 30 — Méthodes de correction DIP</div>
<div class="formula-body">
<strong>1. Méthode de l'affectation directe</strong> (priorité, art. 30 al. 2 LTVA) :<br/>
            Identifier ce qui est imposable / exclu / commun<br/>
            IP imposable → 100% déductible<br/>
            IP exclu → 0% déductible<br/>
            IP commun → proratisé<br/><br/>
<strong>2. Prorata CA (méthode standard)</strong> :<br/>
            Prorata = CA imposable (+ exonéré art. 23) / CA total<br/>
            IP commun déductible = IP commun × Prorata<br/><br/>
<strong>3. Méthodes forfaitaires AFC</strong> (pratique AFC applicable) :<br/>
            Forfaits sectoriels disponibles (médecins, écoles, etc.)
      </div>
<div class="formula-note">Le choix de méthode doit être <strong>cohérent dans le temps</strong> (engagement min. 1 an, art. 39 al. 3 LTVA). Documentation OBLIGATOIRE des calculs.</div>
</div>'''
new_formula='''<div class="formula-box">
<div class="formula-title">🧮 Art. 30 + OTVA 65–68 — ordre de travail</div>
<div class="formula-body">
<strong>1. Affecter directement ce qui peut l’être</strong><br/>
            Dépense uniquement liée à des prestations donnant droit au DIP → déduction selon art. 28<br/>
            Dépense uniquement liée à des prestations ne donnant pas droit → pas de DIP<br/><br/>
<strong>2. Pour les coûts réellement communs</strong><br/>
            Choisir une méthode qui reflète <strong>l’utilisation effective / la réalité économique</strong><br/>
            Exemples possibles : chiffre d’affaires, surfaces, heures, unités, méthode forfaitaire AFC ou calcul propre<br/><br/>
<strong>3. Tester la plausibilité</strong><br/>
            La clé doit être appropriée au cas concret et documentée ; aucun « prorata CA » n’est universel par défaut
      </div>
<div class="formula-note">L’art. 30 al. 2 ne prescrit pas l’affectation directe : il permet, en cas d’utilisation <strong>prépondérante</strong> pour des prestations donnant droit au DIP, une déduction intégrale avec correction à la fin de la période fiscale. Les modalités de calcul sont précisées aux art. 65–68 OTVA.</div>
</div>'''
rep(old_formula,new_formula,'art30 formula',True)
rep("L'ATF 142 II 488 a confirmé que l'AFC peut <strong>imposer une méthode</strong> si celle de l'assujetti aboutit à un résultat manifestement inéquitable. La méthode doit refléter la <strong>réalité économique</strong>.",
    "L’AFC vérifie si la <strong>clé de correction est appropriée</strong>. Selon les art. 65–68 OTVA, l’assujetti peut recourir aux méthodes prévues ou à ses propres calculs, à condition que le résultat soit correct, économiquement compréhensible et que l’affectation soit plausible.",
    'art30 control wording')

# Medical example: keep numbers only as an explicitly assumed key, not legal default.
rep('Prorata = 120\'000 / 920\'000</span><span class="calc-val">13,04%</span>',
    'Clé CA retenue pour cet exemple = 120\'000 / 920\'000</span><span class="calc-val">13,04%</span>',
    'medical calc key label')
rep('Calcul du prorata = enjeu financier majeur.', 'Choix d’une clé appropriée et défendable = enjeu financier majeur.','art30 intro phrase')

# ------------------------------------------------------------------
# Art. 33 + OTVA 75 — allocation first, no universal cascading formula
# ------------------------------------------------------------------
rep("L'<strong>art. 33 LTVA</strong> impose une <strong>réduction proportionnelle</strong> du DIP lorsque l'assujetti reçoit des <strong>flux hors champ TVA</strong> visés à l'art. 18 al. 2 : subventions et autres contributions de droit public visées par l’art. 18 al. 2 let. a à c. La logique : ces flux financent partiellement l'activité sans générer de TVA collectée, donc ils ne doivent pas générer de DIP <em>\"gratuit\"</em>. Très fréquent : <strong>associations, fondations, startups (Innosuisse), médias, sport</strong>.",
    "L'<strong>art. 33 LTVA</strong> distingue les fonds hors contre-prestation. En principe, les montants de l’art. 18 al. 2 <strong>ne réduisent pas</strong> le DIP (art. 33 al. 1). Une réduction proportionnelle est toutefois requise pour les fonds visés à l’art. 18 al. 2 let. <strong>a à c</strong>. La question pratique n’est donc pas seulement « combien de subvention ? », mais <strong>à quel objet, domaine ou déficit ce financement est imputable</strong>.",
    'art33 intro')

sub(r'<div class="formula-box">\n<div class="formula-title">🧮 Formule art\. 33 — Réduction DIP pour subvention</div>.*?</div>\n</div>\n<h4 style="font-size:14px;color:var\(--navy\);margin:18px 0 8px;font-weight:600">Distinction CRUCIALE',
'''<div class="formula-box">
<div class="formula-title">🧮 Art. 33 LTVA + art. 75 OTVA — méthode correcte</div>
<div class="formula-body">
<strong>1. Identifier la nature du fonds</strong> → art. 18 al. 2 let. a à c ou autre mouvement de fonds ?<br/>
<strong>2. Identifier son affectation</strong> → objet / projet, domaine d’activité, déficit d’exploitation, autre<br/>
<strong>3. Affecter les dépenses</strong> → aucune réduction sur un domaine sans DIP ou ne donnant déjà pas droit au DIP ; réduction sur les dépenses du domaine financé lorsqu’il est identifiable<br/>
<strong>4. Déficit d’exploitation</strong> → art. 75 al. 3 OTVA prévoit une réduction globale selon le rapport entre les fonds concernés et l’ensemble des recettes<br/>
<strong>5. Reporter la réduction documentée</strong> → ch. 420
</div>
<div class="formula-note">Il n’existe pas une formule universelle « subvention / (subvention + CA) » pour tous les dossiers. La clé dépend de l’imputabilité du financement. Si art. 30 et art. 33 interviennent tous deux, traiter séparément <strong>l’utilisation</strong> des dépenses et <strong>le financement</strong>, sans appliquer mécaniquement deux pourcentages en cascade.</div>
</div>
<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Distinction CRUCIALE''',
'art33 formula block',count=1,required=True)

rep("Les <strong>subventions à fonds perdu</strong> (Innosuisse, RIE III, soutiens cantonaux) entrent dans art. 33.",
    "Une aide publique ne doit pas être classée par son étiquette commerciale : vérifier qu’elle constitue bien un fonds de l’art. 18 al. 2 let. a à c et <strong>comment elle est affectée</strong> avant de calculer l’impact art. 33.",
    'subsidy label nuance')

# ------------------------------------------------------------------
# Art. 31 / private shares and art. 32 residual value
# ------------------------------------------------------------------
rep("Les <strong>prestations à soi-même</strong> (Eigenverbrauch) sont une <strong>\"TVA virtuelle\"</strong> que l'assujetti doit auto-imposer quand il <strong>change l'usage</strong> d'un bien acquis avec DIP.",
    "La <strong>prestation à soi-même</strong> de l’art. 31 corrige un DIP lorsque les conditions de déduction cessent ultérieurement d’être remplies. Elle ne doit pas être confondue avec une <strong>part privée facturée / déclarée comme chiffre d’affaires par une personne morale</strong>.",
    'art31 intro')

# Replace the vehicle row with a legal-form-aware row.
rep('<tr><td>Voiture de société utilisée à titre privé</td><td class="art-cell">art. 31 al. 2 let. a + Info TVA 08</td><td>0,9%/mois × valeur d\'achat HT</td></tr>',
    '<tr><td>Utilisation privée d’un véhicule d’entreprise</td><td class="art-cell">art. 31 + pratique AFC Parts privées</td><td>Distinguer entreprise individuelle (correction / ch. 415) et personne morale (part privée comme chiffre d’affaires) ; forfait 0,9% ou méthode effective selon pratique applicable</td></tr>',
    'vehicle row')

sub(r'<div class="formula-box">\n<div class="formula-title">🧮 Calcul prestation à soi-même — Voiture privée</div>.*?</div>\n</div>',
'''<div class="formula-box">
<div class="formula-title">🚗 Véhicule — commencer par la forme juridique</div>
<div class="formula-body">
<strong>Entreprise individuelle / indépendant</strong> : l’utilisation privée peut entraîner une correction de l’impôt préalable / prestation à soi-même, notamment au ch. 415.<br/>
<strong>SA / Sàrl / autre personne morale</strong> : la part privée du collaborateur / détenteur est en principe traitée comme une <strong>prestation / chiffre d’affaires</strong>, pas comme la prestation à soi-même personnelle du propriétaire d’une raison individuelle.<br/>
<strong>Forfait</strong> : l’AFC indique que le forfait de 0,9% est applicable en TVA depuis 2022 ; une méthode effective peut aussi être pertinente selon le dossier.
</div>
<div class="formula-note">Ne calculez jamais « 0,9% × prix × 8,1% → ch. 415 » sans d’abord identifier <strong>qui utilise le véhicule et sous quelle forme juridique</strong>.</div>
</div>''','vehicle formula',count=1,required=True)

rep("<div class=\"box-title\">Coordination avec l'impôt sur le revenu (LIFD)</div>","<div class=\"box-title\">Coordination avec les règles de part privée</div>",'vehicle direct tax title')
sub(r'<div class="box-title">Coordination avec les règles de part privée</div>\n<p>.*?</p>',
    '<div class="box-title">Coordination avec les règles de part privée</div>\n<p>Le forfait de 0,9% est utilisé en matière de TVA depuis 2022. La mise en œuvre dépend toutefois du statut du véhicule et de la forme juridique. M05 retient donc un <strong>réflexe de qualification</strong> plutôt qu’une identité automatique entre TVA, certificat de salaire et impôt direct.</p>',
    'vehicle coordination paragraph',count=1)

rep("L'<strong>art. 32 LTVA</strong> est le <strong>\"miroir\" de l'art. 31</strong> : il s'applique lors d'un <strong>changement d'affectation</strong> d'un bien d'investissement (acquis avec ou sans DIP) pendant la <strong>période de régularisation</strong>. Sujet ultra-complexe : <strong>5 ans pour biens mobiliers, 20 ans pour biens immobiliers</strong>.",
    "L'<strong>art. 32 LTVA</strong> règle le <strong>dégrèvement ultérieur</strong> lorsque les conditions du DIP sont remplies plus tard. La valeur résiduelle est calculée en réduisant l’IP de <strong>1/5 par année écoulée pour les biens mobiliers et les prestations de services</strong>, et de <strong>1/20 pour les biens immobiliers</strong>. L’art. 31 traite le mouvement inverse lorsque le droit cesse.",
    'art32 intro')

# ------------------------------------------------------------------
# Legislation / doctrine section: current OTVA and evidence, remove risky jurisprudence slogans
# ------------------------------------------------------------------
rep('<div class="leg-ref">Art. 66-72 OTVA — RS 641.201</div>\n<div class="leg-title">Double affectation — Modalités de calcul</div>\n<div class="leg-desc">Précise les méthodes de correction art. 30 LTVA : prorata CA (art. 67), prorata par unités (m², heures, postes — art. 68), méthodes propres approuvées (art. 65). Liste des forfaits sectoriels reconnus (art. 79-80).</div>',
    '<div class="leg-ref">Art. 65-68 OTVA — RS 641.201</div>\n<div class="leg-title">Double affectation — Méthodes de correction</div>\n<div class="leg-desc"><strong>Art. 65</strong> : correction selon l’utilisation effective, méthodes forfaitaires AFC ou calculs propres. <strong>Art. 67</strong> encadre les calculs propres. <strong>Art. 68</strong> permet de choisir une ou plusieurs méthodes si le résultat est correct et économiquement compréhensible et si l’affectation est plausible.</div>',
    'OTVA 65-68 card')
rep('📄 OTVA art. 66-72','📄 OTVA art. 65-68','OTVA link label')

rep('<div class="leg-ref">Art. 73-81 OTVA — RS 641.201</div>\n<div class="leg-title">Régularisation et corrections d\'affectation</div>\n<div class="leg-desc">Art. 78 : modalités précises du dégrèvement ultérieur (art. 32 LTVA). Art. 79 : forfaits sectoriels. Art. 81 : engagement minimum dans la méthode choisie (1 an effective, 3 ans TDFN). Les art. 79 à 81 OTVA règlent les passages entre méthode effective et TDFN ; les corrections de valeur résiduelle doivent être analysées selon le sens du changement.</div>',
    '<div class="leg-ref">Art. 75 OTVA + règles de changement de méthode 2025+</div>\n<div class="leg-title">Subventions et changements de méthode</div>\n<div class="leg-desc"><strong>Art. 75 OTVA</strong> précise l’imputation des fonds art. 18 al. 2 let. a à c : domaine sans DIP, domaine déterminé ou déficit d’exploitation. Depuis 2025, les passages entre méthode effective et TDFN/TaF impliquent une analyse de la <strong>valeur résiduelle</strong>; le changement est possible après une période fiscale complète sous réserve des délais et conditions AFC applicables.</div>',
    'OTVA 75 transition card')
rep('📄 OTVA art. 73-81','📄 OTVA / pratique actuelle','OTVA transition link label')

# Neutralize fragile exact Info TVA numbering in the source cards.
for old,new in [
('Info TVA 08 — AFC','Pratique AFC — Parts privées'),
('Info TVA 14 — AFC','Pratique AFC — Hôtellerie / restauration'),
('Info TVA 17 — AFC','Pratique AFC — Immobilier'),
('Info TVA 20 — AFC','Pratique AFC — Formation'),
('Info TVA 21 — AFC','Pratique AFC — Santé')]:
    rep(old,new,'practice label '+old)

# Replace jurisprudence subsection wholesale with current-law proof framework.
sub(r'<h4 style="font-size:14px;color:var\(--navy\);margin:24px 0 12px;font-weight:600">Jurisprudence essentielle DIP</h4>.*?<div class="section-nav">',
'''<h4 style="font-size:14px;color:var(--navy);margin:24px 0 12px;font-weight:600">Réflexes de preuve et pratique actuelle</h4>
<div class="leg-card"><div class="leg-icon red">⚖️</div><div class="leg-content"><div class="leg-ref">Art. 81 al. 3 LTVA</div><div class="leg-title">Liberté des moyens de preuve</div><div class="leg-desc">L’acceptation d’une preuve ne peut pas dépendre exclusivement d’un document précis. L’AFC apprécie les preuves disponibles; l’assujetti supporte le fardeau de la preuve des faits diminuant l’impôt, notamment le DIP.</div><div class="leg-links"><a class="leg-link" href="https://www.estv.admin.ch/fr/liberte-des-moyens-de-preuve-tva" target="_blank" rel="noopener noreferrer">🔗 AFC — Liberté des moyens de preuve</a></div></div></div>
<div class="leg-card"><div class="leg-icon red">🏛️</div><div class="leg-content"><div class="leg-ref">Contrôle TVA — AFC</div><div class="leg-title">Double affectation, changements d’affectation et parts privées</div><div class="leg-desc">Lors d’un contrôle, l’AFC vérifie notamment les prestations ne donnant pas droit au DIP, les changements et doubles affectations ainsi que les parts privées. La qualité du tableau d’affectation et de la piste d’audit est donc aussi importante que le calcul arithmétique.</div><div class="leg-links"><a class="leg-link" href="https://www.estv.admin.ch/fr/deroulement-dun-controle-tva" target="_blank" rel="noopener noreferrer">🔗 AFC — Contrôle TVA</a></div></div></div>
<div class="leg-card"><div class="leg-icon red">📚</div><div class="leg-content"><div class="leg-ref">M12 — Jurisprudence Lab</div><div class="leg-title">Ne pas transformer un ancien arrêt en règle universelle</div><div class="leg-desc">M05 s’appuie d’abord sur la LTVA, l’OTVA et la pratique AFC actuelle. Les arrêts sont étudiés en M12 avec leur contexte temporel, leur question juridique exacte et leur portée, plutôt que comme slogans (« lien direct », « prorata imposé », etc.).</div></div></div>
<div class="section-nav">''',
'jurisprudence rebuild',count=1,required=True)

# ------------------------------------------------------------------
# Cases
# ------------------------------------------------------------------
# Case 1: remove dubious LIFD 50% comparison.
rep("B) CHF 6'553 (= 80'900 × 8,1%, frais représentation 100% déductibles si liés à l'activité art. 28)",
    "B) CHF 6'553 (= 80'900 × 8,1%), sous réserve que les repas soient réellement affectés à l’activité entrepreneuriale et suffisamment prouvés",
    'case1 answer')
rep("Les <strong>frais de représentation</strong> sont <strong>intégralement déductibles en TVA</strong> s'ils sont liés à l'activité commerciale (art. 28 al. 1 LTVA) — contrairement à l'impôt direct LIFD qui limite à 50%. <strong>Différence majeure</strong> entre LTVA et LIFD à retenir.",
    "Il n’existe pas, dans la LTVA actuelle, une réduction automatique de 50% du DIP sur les repas de représentation. Le dossier doit toutefois établir l’<strong>affectation entrepreneuriale</strong> et la réalité de la dépense. Si une part est privée ou non entrepreneuriale, elle doit être exclue ou corrigée.",
    'case1 explanation')

# Case 2: invoice missing VAT number is a proof problem, not automatic no-DIP.
rep("B) Non — facture non conforme art. 26 al. 2 let. b LTVA (N° TVA manquant) → IP contestable par AFC",
    "B) Le dossier doit être sécurisé : vérifier l’assujettissement du fournisseur et la réalité de la prestation, puis demander une facture corrigée ; le N° manquant n’entraîne pas à lui seul un refus automatique du DIP",
    'case2 q1 answer')
sub(r'<div class="step-explanation" id="m5c2s1-expl">.*?</div>\n</div>',
'''<div class="step-explanation" id="m5c2s1-expl">L’art. 26 prévoit que la facture mentionne en règle générale l’inscription / numéro TVA du fournisseur. Une lacune est un <strong>signal de contrôle</strong>, surtout parce qu’il faut vérifier que l’impôt facturé est juridiquement plausible. Mais l’art. 81 al. 3 consacre la liberté des moyens de preuve : le DIP ne peut pas être refusé <strong>uniquement</strong> parce qu’une mention formelle manque si les conditions des art. 28–33 et les faits sont suffisamment prouvés. Procédure : vérifier le registre IDE, contrat / prestation / paiement, demander une facture corrigée et conserver la piste d’audit.<div class="art-ref">📋 art. 26 + 28–33 + 81 al. 3 LTVA</div></div>
</div>''','case2 q1 explanation',count=1,required=True)

# Case 5: make turnover ratio an assumed, justified key for the case.
rep('Quel est le prorata CA selon art. 30 al. 2 + pratique AFC applicable ?',
    'Si le cabinet documente que le chiffre d’affaires est une clé appropriée pour ces coûts communs, quel pourcentage résulte de cette clé ?',
    'case5 q1')
rep("Prorata art. 30 = <strong>CA donnant droit au DIP / CA total</strong>.",
    "Dans <strong>ce cas pédagogique uniquement</strong>, la clé de chiffre d’affaires est supposée appropriée aux coûts communs. Elle donne :",
    'case5 explanation start')
rep('📋 art. 30 al. 2 LTVA + pratique AFC applicable','📋 art. 30 LTVA + art. 65–68 OTVA','case5 ref')

# Case 6: rebuild the exact-number subsidy question and follow-up.
sub(r'<div class="case-step" id="m5c6s2">.*?</div>\n</div>\n<div class="case-step" id="m5c6s3">.*?</div>\n</div>',
'''<div class="case-step" id="m5c6s2">
<div class="step-question"><span class="step-q-num">Q2</span>Peut-on calculer le DIP net à partir des seuls montants « CA 350’000 / subvention 200’000 / IP 32’400 » ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c6s2',this,false)">A) Oui : 200 / 550 = 36,36% dans tous les cas</button><button class="step-opt" onclick="caseAnswer('m5c6s2',this,true)">B) Non : il faut d’abord savoir à quel projet / domaine / déficit la subvention est affectée et quels coûts elle finance</button><button class="step-opt" onclick="caseAnswer('m5c6s2',this,false)">C) Oui : 200’000 × 8,1%</button><button class="step-opt" onclick="caseAnswer('m5c6s2',this,false)">D) Oui : tout le DIP est perdu</button></div>
<div class="step-explanation" id="m5c6s2-expl">L’art. 33 al. 2 impose une réduction pour les fonds visés, mais <strong>l’art. 75 OTVA détermine comment l’imputation fonctionne</strong>. Si la subvention finance un domaine déterminé, seul le DIP des dépenses de ce domaine est réduit. Si elle couvre un déficit d’exploitation, une clé globale selon l’ensemble des recettes devient pertinente. Les trois montants du scénario ne suffisent donc pas à produire un DIP net fiable.<div class="art-ref">📋 art. 33 LTVA + art. 75 OTVA</div></div>
</div>
<div class="case-step" id="m5c6s3">
<div class="step-question"><span class="step-q-num">Q3</span>Que faire si l’entreprise découvre plusieurs périodes avec une réduction art. 33 potentiellement omise ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c6s3',this,false)">A) Appliquer automatiquement cinq fois le même montant</button><button class="step-opt" onclick="caseAnswer('m5c6s3',this,true)">B) Reconstituer période par période l’affectation des fonds et du DIP, corriger les périodes encore ouvertes et analyser séparément intérêts / procédure</button><button class="step-opt" onclick="caseAnswer('m5c6s3',this,false)">C) Attendre obligatoirement un contrôle</button><button class="step-opt" onclick="caseAnswer('m5c6s3',this,false)">D) Corriger uniquement l’année courante</button></div>
<div class="step-explanation" id="m5c6s3-expl">Une omission historique n’autorise pas un rappel « forfaitaire » construit sur une clé inventée. Il faut reconstituer les faits et la méthode correcte pour chaque période, puis utiliser les mécanismes de correction prévus par la LTVA. Si aucune procédure de contrôle n’est annoncée, les conditions d’une éventuelle dénonciation spontanée peuvent être examinées en M11 ; ce n’est ni automatique ni un substitut au calcul fiscal.<div class="art-ref">📋 art. 42 + 72 + 81 + 102 LTVA · M11</div></div>
</div>''','case6 rebuild',count=1,required=True)

# Case 7: change SA vehicle question into legal-form distinction, and fix employee-event misuse of CHF500 gift rule.
rep('<div class="case-title">Mobilière Conseil SA — Voiture &amp; cadeaux clients</div>',
    '<div class="case-title">Véhicule, parts privées &amp; cadeaux — forme juridique d’abord</div>','case7 title')
sub(r'<div class="case-step" id="m5c7s1">.*?</div>\n</div>',
'''<div class="case-step" id="m5c7s1">
<div class="step-question"><span class="step-q-num">Q1</span>Pour la voiture utilisée par le CEO de Mobilière Conseil SA, quel est le premier réflexe TVA ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c7s1',this,false)">A) Appliquer automatiquement art. 31 et ch. 415</button><button class="step-opt" onclick="caseAnswer('m5c7s1',this,true)">B) Identifier qu’il s’agit d’une personne morale : la part privée du collaborateur / détenteur est en principe traitée comme prestation / chiffre d’affaires selon la pratique AFC, puis choisir forfait 0,9% ou méthode effective</button><button class="step-opt" onclick="caseAnswer('m5c7s1',this,false)">C) Rembourser immédiatement tout le DIP du véhicule</button><button class="step-opt" onclick="caseAnswer('m5c7s1',this,false)">D) Utiliser uniquement le pourcentage comptable de 30%</button></div>
<div class="step-explanation" id="m5c7s1-expl">La pratique AFC distingue la <strong>personne exerçant une activité indépendante</strong>, pour laquelle la part privée peut constituer une correction de l’IP / prestation à soi-même au ch. 415, de la <strong>personne morale</strong>, pour laquelle la part privée est déclarée comme chiffre d’affaires. Le forfait de 0,9% est applicable en TVA depuis 2022, mais la forme juridique doit être qualifiée avant le calcul.<div class="art-ref">📋 art. 31 LTVA · pratique AFC Parts privées</div></div>
</div>''','case7 vehicle',count=1,required=True)
sub(r'<div class="case-step" id="m5c7s3">.*?</div>\n</div>',
'''<div class="case-step" id="m5c7s3">
<div class="step-question"><span class="step-q-num">Q3</span>Repas d’équipe annuel : la limite de CHF 500 pour les cadeaux suffit-elle à conclure « aucune TVA » ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m5c7s3',this,false)">A) Oui, toujours</button><button class="step-opt" onclick="caseAnswer('m5c7s3',this,true)">B) Non : la limite de l’art. 31 al. 2 let. c concerne la présomption de motif entrepreneurial pour les cadeaux ; un événement du personnel doit être qualifié selon sa nature et la pratique Parts privées / personnel</button><button class="step-opt" onclick="caseAnswer('m5c7s3',this,false)">C) Toute dépense de personnel est privée</button><button class="step-opt" onclick="caseAnswer('m5c7s3',this,false)">D) 50% de TVA doit toujours être corrigé</button></div>
<div class="step-explanation" id="m5c7s3-expl">Ne transposez pas mécaniquement le seuil des <strong>cadeaux</strong> à toutes les prestations au personnel. Le dossier doit distinguer événement d’entreprise, avantage privé, cadeau et éventuelle prestation à soi-même / part privée. Le bon réflexe est de documenter le bénéficiaire, le motif entrepreneurial et la nature de la prestation, puis d’appliquer la pratique AFC correspondante.<div class="art-ref">📋 art. 31 LTVA · pratique AFC Parts privées</div></div>
</div>''','case7 employee meal',count=1,required=True)

# Case 8 method reference current.
rep('📋 art. 81 al. 3 OTVA','📋 pratique AFC TDFN / TaF 2025+ · règles de changement','case8 method ref')

# Case 10 procedure: remove invented fixed PV/deadline/cost wording if present.
rep('<strong>Réception du procès-verbal</strong> (PV) du contrôle → délai standard 30j pour réagir.',
    '<strong>Réception des constatations / de la notification</strong> → identifier précisément l’acte reçu, ses effets et le délai applicable avant de répondre.',
    'case10 procedure act')
sub(r'<strong>Coût stratégie défense</strong> : honoraires fiduciaire \+ avocat \(typiquement CHF 5\'000-25\'000\) vs économies sur rappel\. <strong>Évaluation coût/bénéfice</strong> systématique\.',
    '<strong>Évaluation coût/bénéfice</strong> : proportionner le niveau de documentation et de recours à l’enjeu, sans utiliser de fourchette d’honoraires présentée comme norme.',
    'case10 costs')

# Holding case wording bug: correct answer says "Oui" although legal conclusion is no automatic reduction.
rep('B) Oui — art. 18 al. 2 let. f LTVA : dividendes = flux hors contre-prestation, sans réduction automatique art. 33 des frais communs holding',
    'B) Non — les dividendes sont hors contre-prestation, mais ils ne déclenchent pas automatiquement une réduction art. 33 ; analyser art. 29 et l’affectation des frais',
    'holding answer wording')

# Case 12: avoid universal subsidy final arithmetic if present by converting objective to analysis.
rep('<div class="case-context">📚 <strong>Objectif :</strong> calculer le DIP net 2026 en cumulant toutes les corrections.</div>',
    '<div class="case-context">📚 <strong>Objectif :</strong> construire l’ordre d’analyse du DIP 2026 et identifier quelles données manquent avant tout calcul final.</div>',
    'case12 objective')

# ------------------------------------------------------------------
# QCM — replace the most dangerous learning traps
# ------------------------------------------------------------------
# q02
sub(r"\{ id:'m05-q02'.*?\n  \},",'''{ id:'m05-q02', diff:'easy', art:'art. 26 + 81 al. 3 LTVA',
    q:'Une facture fournisseur ne mentionne pas son N° TVA. Quel réflexe est correct ?',
    opts:['Refuser automatiquement le DIP','Vérifier l’assujettissement et la réalité de la prestation, demander une facture corrigée et apprécier l’ensemble des preuves','Déduire sans contrôle','Déduire seulement 50%'],
    correct:1,
    expl:'L’art. 26 prévoit en règle générale la mention de l’inscription / numéro TVA du fournisseur. Mais l’art. 81 al. 3 interdit de faire dépendre la preuve exclusivement d’un document précis. Le professionnel sécurise donc la substance et la preuve, tout en obtenant une facture corrigée si possible.'
  },''','q02 proof',count=1,required=True)
# q09 art30
sub(r"\{ id:'m05-q09'.*?\n  \},",'''{ id:'m05-q09', diff:'easy', art:'art. 30 + OTVA 65–68',
    q:'En double affectation, quel principe guide le choix de la méthode de correction ?',
    opts:['Le prorata CA est toujours obligatoire','La méthode doit refléter l’utilisation réelle / la réalité économique et produire un résultat approprié et documenté','Toujours 50%','L’ERP décide seul'],
    correct:1,
    expl:'L’art. 30 exige une correction proportionnelle à l’utilisation. Les art. 65–68 OTVA admettent différentes méthodes, y compris des calculs propres, si le résultat est correct et économiquement compréhensible. L’affectation directe est un excellent réflexe de travail mais n’est pas le contenu de l’art. 30 al. 2.'
  },''','q09 art30',count=1,required=True)
# q13 representation
sub(r"\{ id:'m05-q13'.*?\n  \},",'''{ id:'m05-q13', diff:'med', art:'art. 28–30 LTVA',
    q:'Repas de représentation avec clients : quel réflexe TVA ?',
    opts:['Réduction automatique de 50% du DIP','Vérifier l’affectation entrepreneuriale et la preuve ; aucune réduction forfaitaire de 50% n’est prévue par la LTVA actuelle','DIP toujours interdit','DIP toujours admis sans justificatif'],
    correct:1,
    expl:'La TVA ne prévoit pas une coupe automatique de 50% pour les frais de représentation. Il faut prouver la réalité et l’affectation entrepreneuriale de la dépense; une part privée ou non entrepreneuriale doit être exclue ou corrigée.'
  },''','q13 representation',count=1,required=True)
# q14 mixed use
sub(r"\{ id:'m05-q14'.*?\n  \},",'''{ id:'m05-q14', diff:'med', art:'art. 30 + OTVA 65–68',
    q:'Cabinet médical : CA exclu 800k, ventes imposables 200k, IP commun 5’400. Peut-on conclure automatiquement à un DIP commun de 1’080 ?',
    opts:['Oui, le chiffre d’affaires est toujours la clé légale','Seulement si la clé de chiffre d’affaires est appropriée et documentée pour ces coûts communs ; sinon une autre clé peut être requise','Non, DIP toujours 0','Oui, sans autre analyse'],
    correct:1,
    expl:'200/1’000 = 20% et 5’400 × 20% = 1’080 uniquement si le chiffre d’affaires reflète correctement l’utilisation des coûts communs. L’OTVA permet différentes méthodes; la plausibilité de la clé est essentielle.'
  },''','q14 mixed use',count=1,required=True)
# q23/q32 holdings already good, keep.
# q24 ticket formalism nuance
sub(r"\{ id:'m05-q24'.*?\n  \},",'''{ id:'m05-q24', diff:'med', art:'art. 26 al. 3 + OTVA',
    q:'Sur un ticket de caisse jusqu’au seuil fixé par le Conseil fédéral, quelle simplification vise l’art. 26 al. 3 ?',
    opts:['Le fournisseur peut rester anonyme','Le destinataire de la prestation peut ne pas être mentionné','Le taux de TVA n’a jamais besoin d’apparaître','Aucune preuve n’est nécessaire'],
    correct:1,
    expl:'L’art. 26 al. 3 prévoit que le destinataire ne doit pas être mentionné sur un ticket de caisse lorsque la contre-prestation ne dépasse pas le seuil réglementaire. Cette simplification de facture ne supprime ni les conditions du DIP ni le fardeau de la preuve.'
  },''','q24 ticket',count=1,required=True)
# q27 voluntary disclosure
sub(r"\{ id:'m05-q27'.*?\n  \},",'''{ id:'m05-q27', diff:'med', art:'art. 72 + 102 LTVA',
    q:'Une PME découvre plusieurs anciennes périodes potentiellement erronées sur le DIP. Quel ordre de travail est correct ?',
    opts:['Attendre un contrôle','Reconstituer les périodes, corriger les erreurs encore ouvertes et, avant toute procédure annoncée, analyser séparément si les conditions de l’art. 102 sont remplies','Appliquer un forfait unique sur cinq ans','Liquider la société'],
    correct:1,
    expl:'La priorité est le calcul fiscal exact et la correction des périodes concernées. La dénonciation spontanée est une question procédurale distincte, soumise à des conditions; elle ne remplace ni le rappel ni les intérêts. M11 approfondit ce point.'
  },''','q27 disclosure',count=1,required=True)
# q28 no cascade formula
sub(r"\{ id:'m05-q28'.*?\n  \},",'''{ id:'m05-q28', diff:'hard', art:'art. 30 + 33 LTVA · art. 75 OTVA',
    q:'Association avec activité mixte et subvention : quel ordre d’analyse du DIP est professionnel ?',
    opts:['Appliquer automatiquement CA imposable/CA total puis subvention/(subvention+CA)','Affecter d’abord les dépenses selon leur utilisation, choisir une clé appropriée pour les coûts communs, puis analyser séparément à quel domaine / objet / déficit la subvention est imputable','Refuser tout le DIP','Déduire tout le DIP'],
    correct:1,
    expl:'Les art. 30 et 33 répondent à deux questions distinctes : utilisation des prestations préalables et financement par certains fonds publics. Il n’existe pas une formule universelle en cascade; l’art. 75 OTVA impose d’examiner l’imputabilité de la subvention.'
  },''','q28 no universal cascade',count=1,required=True)
# q29 unambiguous 13/20
sub(r"\{ id:'m05-q29'.*?\n  \},",'''{ id:'m05-q29', diff:'hard', art:'art. 31–32 LTVA',
    q:'Immeuble : IP initial CHF 200’000. Après 7 années complètes d’utilisation donnant droit au DIP, les conditions cessent définitivement. Quelle valeur résiduelle sert de base ?',
    opts:['CHF 200’000','CHF 130’000 (= 200’000 × 13/20)','CHF 70’000','CHF 0'],
    correct:1,
    expl:'Pour les biens immobiliers, l’IP est réduit linéairement de 1/20 par année écoulée. Après 7 années complètes, la valeur résiduelle est 13/20 de l’IP initial, soit CHF 130’000. L’amortissement comptable ne détermine pas cette valeur TVA.'
  },''','q29 residual',count=1,required=True)
# q33 unambiguous machine residual
sub(r"\{ id:'m05-q33'.*?\n  \},",'''{ id:'m05-q33', diff:'hard', art:'art. 31 LTVA',
    q:'Machine : IP initial CHF 8’100. Après deux années complètes, les conditions du DIP cessent définitivement. Quel ordre de grandeur de correction sur valeur résiduelle ?',
    opts:['CHF 8’100','CHF 4’860 (= 8’100 × 3/5)','CHF 5’670 selon valeur comptable 70%','CHF 0'],
    correct:1,
    expl:'Pour un bien mobilier, l’IP est réduit de 1/5 par année écoulée. Après deux années complètes, 3/5 subsistent : CHF 4’860. La valeur résiduelle comptable n’est pas la base TVA.'
  },''','q33 residual',count=1,required=True)
# q34 positive relief unambiguous
sub(r"\{ id:'m05-q34'.*?\n  \},",'''{ id:'m05-q34', diff:'hard', art:'art. 32 LTVA',
    q:'Immeuble : IP non déduit initialement CHF 162’000. Après deux années complètes, les conditions du DIP sont remplies. Dégrèvement maximal sur valeur résiduelle ?',
    opts:['CHF 162’000','CHF 145’800 (= 162’000 × 18/20)','CHF 81’000','CHF 0'],
    correct:1,
    expl:'Art. 32 : pour un immeuble, la valeur résiduelle diminue de 1/20 par année écoulée. Après deux années complètes, 18/20 peuvent encore être pris en compte, soit CHF 145’800, sous réserve que les conditions du DIP soient effectivement remplies.'
  },''','q34 residual positive',count=1,required=True)

# ------------------------------------------------------------------
# Vocab / cheatsheet
# ------------------------------------------------------------------
rep('<div class="vc-use">Facture respectant les mentions obligatoires de l\'art. 26. Condition formelle pour déduire l\'IP.</div>',
    '<div class="vc-use">Facture qui documente correctement l’opération selon l’art. 26. Pièce de preuve centrale, mais le droit au DIP s’apprécie avec les art. 28–33 et la liberté des moyens de preuve (art. 81 al. 3).</div>',
    'vocab invoice')
rep('<div class="vc-use">Méthode standard pour ventiler l\'IP commun entre activités. Prorata = CA imposable / CA total.</div>',
    '<div class="vc-use">Une clé possible pour les coûts communs si le chiffre d’affaires reflète correctement l’utilisation. Pas une méthode universelle imposée par l’art. 30.</div>',
    'vocab turnover key')
rep('<div class="vc-use">Méthode prioritaire art. 30 : identifier directement chaque IP comme imposable, exclu, ou commun à proratiser.</div>',
    '<div class="vc-use">Réflexe pratique : attribuer directement les dépenses lorsque c’est possible, puis choisir une méthode appropriée pour les coûts réellement communs. À distinguer de l’art. 30 al. 2 sur l’utilisation prépondérante.</div>',
    'vocab direct allocation')
rep('<div class="vc-use">Régularisation du DIP lors du changement d\'usage d\'un bien d\'investissement. 5 ans mobilier, 20 ans immobilier.</div>',
    '<div class="vc-use">Utiliser la terminologie légale avec précision : art. 31 = prestation à soi-même lorsque le droit cesse ; art. 32 = dégrèvement ultérieur lorsque le droit naît plus tard. Valeur résiduelle : 1/5 mobilier/services, 1/20 immobilier par année écoulée.</div>',
    'vocab art32')
rep('<div class="vc-use">Tableau obligatoire de suivi des biens d\'investissement pour application art. 32 sur 5/20 ans.</div>',
    '<div class="vc-use">Outil de contrôle fortement recommandé pour suivre IP initial, date, usage et valeur résiduelle. La LTVA exige la preuve et la conservation nécessaires ; elle n’impose pas un modèle unique de registre.</div>',
    'vocab register')

# Rebuild cheat card 2.
sub(r'<div class="cheat-card">\n<div class="cheat-title">2 — 4 conditions cumulatives DIP</div>.*?</div>\n</div>',
'''<div class="cheat-card">
<div class="cheat-title">2 — Test professionnel du DIP</div>
<div class="cheat-body"><ol style="margin-left:18px"><li><strong>Source de l’impôt</strong> : art. 28 / 28a</li><li><strong>Activité entrepreneuriale / affectation</strong> : art. 28–30</li><li><strong>Exclusions / réductions</strong> : art. 29 et 33</li><li><strong>Moment du droit</strong> : art. 40 selon la méthode</li><li><strong>Preuve</strong> : facture art. 26 + ensemble des preuves, art. 81 al. 3</li></ol><p>Une facture parfaite ne crée pas un DIP matériel inexistant ; une lacune formelle n’entraîne pas automatiquement un refus si le fait fiscal est suffisamment prouvé.</p></div>
</div>''','cheat card2',count=1,required=True)

# Replace cheat card 3 if it still calls turnover method standard.
rep('<p><strong>Méthode standard :</strong></p>', '<p><strong>Pour les coûts communs :</strong></p>','cheat art30 label')
rep('<li>Prorata = CA imposable (+ exonéré art. 23) / CA total</li>',
    '<li>Choisir une clé appropriée : CA, surfaces, heures, unités ou autre méthode plausible selon le dossier</li>',
    'cheat art30 formula')

# Current TDFN thresholds can stay, but remove stale generic method commitment language if any.
rep('Méthode encaissement art. 39 al. 2 : autorisation AFC requise.','Décompte selon les contre-prestations reçues : option / autorisation selon art. 39; suivre les règles de transition et de période applicables.','cheat received method')

# ------------------------------------------------------------------
# End UX + completion sync
# ------------------------------------------------------------------
old_end='''<div class="cheat-final">
<button class="btn btn-primary btn-lg" onclick="window.print()">🖨️ Imprimer la cheatsheet</button>
</div>
<div class="section-nav">
<button class="btn btn-ghost" onclick="goto('vocab')">← Vocabulaire</button>
<button class="btn btn-gold" onclick="goto('theory')">⬡ Recommencer M05</button>
</div>'''
new_end='''<div class="cheat-final">
<button class="btn btn-primary btn-lg" onclick="window.print()">🖨️ Imprimer la cheatsheet</button>
<p style="font-size:12px;color:var(--muted);margin-top:12px">Fin de M05 : vous devez pouvoir justifier <strong>pourquoi</strong> un DIP est déductible, corrigé ou réduit. La suite logique est M06 — Territorialité &amp; TVA internationale.</p>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:14px"><a class="btn btn-ghost" href="index.html" style="text-decoration:none">← Retour au cours</a><button class="btn btn-primary" onclick="finishModule()">✓ Terminer M05</button><button class="btn btn-gold" onclick="goNextModule()">Continuer avec M06 →</button></div>
<div id="m05-complete" class="box success" style="display:none;text-align:left;margin-top:16px"><div class="box-icon">✅</div><div class="box-body"><div class="box-title">M05 enregistré comme terminé</div><p>La progression du module est à 100% et le cours principal est synchronisé. Le résultat du quiz reste enregistré séparément : terminer le module ne transforme pas un quiz non réussi en quiz réussi.</p><div style="margin-top:10px"><a class="btn btn-primary" href="m06-territorialite-tva-internationale.html" style="text-decoration:none">Aller à M06 — Territorialité →</a></div></div></div>
<p style="font-size:11px;color:var(--muted);margin-top:16px">Conception : <a href="https://www.linkedin.com/in/mariia-lobur/" target="_blank" rel="noopener noreferrer">Mariia Lobur</a> · <a href="https://github.com/mariialobur" target="_blank" rel="noopener noreferrer">GitHub</a></p>
</div>
<div class="section-nav">
<button class="btn btn-ghost" onclick="goto('vocab')">← Vocabulaire</button>
<button class="btn btn-gold" onclick="goto('theory')">⬡ Revoir M05</button>
</div>'''
rep(old_end,new_end,'M05 completion UI',True)

# Add schemaVersion without changing storage key, and make progress honor completed state.
rep("const KEY='tva_m05_v4_5';\nconst SRSKEY='tva_m05_v4_5_srs';",
    "const KEY='tva_m05_v4_5'; // clé historique conservée pour ne pas perdre la progression\nconst SRSKEY='tva_m05_v4_5_srs';",
    'storage comment',True)
# state initializer: add schemaVersion/completed if absent.
sub(r'let state=\{(?!schemaVersion)',"let state={schemaVersion:'v5_0',completed:0,",'state schema',count=1,flags=0,required=True)
# updateProg percentage logic: tolerate different current implementation via exact pattern.
rep("const pct=Math.round(done/sections.length*100);","const pct=state.completed?100:Math.round(done/sections.length*100);",'progress complete')

completion_js='''
// ============ MODULE COMPLETION / DASHBOARD SYNC ============
function syncDashboardDone(){
  try{
    const k='tvaSpecialisteTvaDashboardV1';
    const d=JSON.parse(localStorage.getItem(k)||'{}');
    d.M05='done';
    localStorage.setItem(k,JSON.stringify(d));
  }catch(e){}
}
function finishModule(){
  state.completed=1;
  save();
  syncDashboardDone();
  const box=document.getElementById('m05-complete');
  if(box)box.style.display='flex';
  updateProg();
}
function goNextModule(){
  finishModule();
  window.location.href='m06-territorialite-tva-internationale.html';
}
'''
rep('// ============ INIT ============',completion_js+'\n// ============ INIT ============','completion JS insert',True)
rep("  updateProg();\n});","  updateProg();\n  if(state.completed){const box=document.getElementById('m05-complete');if(box)box.style.display='flex';}\n});",'completion init')

# ------------------------------------------------------------------
# Broad cleanup of known stale / over-strong claims
# ------------------------------------------------------------------
replacements=[
("en pratique : pour une entreprise avec activité immobilière, conserver TOUT pendant 20 ans pour simplifier la gestion.","la durée prolongée vise les documents commerciaux nécessaires aux corrections / dégrèvements immobiliers ; elle ne transforme pas tout le dossier de l’entreprise en archive de 20 ans."),
("Art. 32 al. 3 LTVA : 20 ans pour les biens immobiliers","Art. 32 al. 2 LTVA : réduction de 1/20 par année écoulée pour les biens immobiliers"),
("art. 81 OTVA — engagement de 3 ans minimum en effective avant retour TDFN","pratique AFC TDFN/TaF 2025+ — changement possible après une période fiscale complète sous réserve des conditions et délais applicables"),
("3 ans en effective avant retour à TDFN","une période fiscale complète avant changement, sous réserve des conditions / délais AFC applicables"),
("PDF/A", "format lisible et durable adapté au système d’archivage"),
("Dossier DIP premium", "Dossier DIP professionnel"),
]
for old,new in replacements:
    rep(old,new,'broad cleanup '+old[:28])

p.write_text(t,encoding='utf-8')
print('M05 changes:',len(changes))
for c in changes:
    print(' -',c)
