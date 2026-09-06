from pathlib import Path
import re

p=Path('m06-territorialite-tva-internationale.html')
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

# ------------------------------------------------------------------
# Product / pedagogy / UX
# ------------------------------------------------------------------
rep('<span class="sidebar-version">v4.3</span>','<span class="sidebar-version">v5.0</span>','sidebar version',True)
rep('<span class="version-badge">v4.3 — Dossier expert 10/10</span>','<span class="version-badge">v5.0 — Territorialité &amp; flux transfrontaliers</span>','top version',True)
rep('<div class="hero-title">Territorialité — Le pivot international de la TVA suisse</div>',
    '<h1 class="hero-title">Territorialité — Localiser avant de taxer</h1>','semantic h1',True)
rep('<div class="sidebar-footer">\n<a class="btn-home" href="index.html">← Retour au cours</a>\n</div>',
    '<div class="sidebar-footer">\n<a class="btn-home" href="index.html">← Retour au cours</a>\n<div style="font-size:10px;line-height:1.5;color:rgba(255,255,255,.45);text-align:center;margin-top:9px">Conception : <a href="https://www.linkedin.com/in/mariia-lobur/" target="_blank" rel="noopener noreferrer" style="color:var(--gold)">Mariia Lobur</a> · <a href="https://github.com/mariialobur" target="_blank" rel="noopener noreferrer" style="color:var(--gold)">GitHub</a></div>\n</div>',
    'author sidebar',True)

objectives='''<div class="theory-block">
<h3><span class="num">✓</span>Objectifs professionnels de M06 <span class="block-risk risk-red">🔴 Compétence centrale</span></h3>
<p class="prose">À la fin de M06, vous devez pouvoir transformer un flux international en une <strong>qualification suisse défendable</strong> sans confondre lieu de prestation, exonération, impôt sur les acquisitions, importation et assujettissement d’une entreprise étrangère.</p>
<table class="comp-table"><thead><tr><th>Vous devez savoir</th><th>Réflexe attendu</th></tr></thead><tbody>
<tr><td>Déterminer le territoire pertinent</td><td>art. 3–4 : Confédération + Liechtenstein + Büsingen ; traiter séparément les particularités douanières de Samnaun/Sampuoir</td></tr>
<tr><td>Localiser un bien</td><td>art. 7 : remise / départ du transport + règles spéciales vente par correspondance / engagement pour l’étranger</td></tr>
<tr><td>Localiser un service</td><td>art. 8 : tester d’abord les exceptions al. 2, sinon lieu du destinataire al. 1</td></tr>
<tr><td>Distinguer les statuts</td><td>art. 23 exonéré ≠ art. 8 lieu à l’étranger ≠ art. 21 exclu</td></tr>
<tr><td>Traiter un achat étranger</td><td>art. 45 : vérifier la catégorie d’acquisition, le lieu, le statut du fournisseur et les exclusions/exonérations</td></tr>
<tr><td>Traiter un bien importé</td><td>art. 50 ss : OFDF, base art. 54, DTe / e-bordereau et DIP éventuel</td></tr>
<tr><td>Tester l’assujettissement étranger</td><td>prestation sur territoire suisse + CA mondial déterminant + exceptions propres aux entreprises étrangères</td></tr>
</tbody></table>
<div class="box info"><div class="box-icon">🧭</div><div class="box-body"><div class="box-title">Frontière pédagogique</div><p>M06 tranche la <strong>TVA suisse</strong>. Lorsqu’un flux est localisé à l’étranger, la conclusion suisse est « hors territoire suisse » ; l’existence d’une TVA française, allemande, UE ou autre devient une <strong>deuxième analyse de droit étranger</strong>. M06 signale ce contrôle sans transformer une règle étrangère en règle LTVA. Les plateformes et e-commerce sont approfondis en M10.</p></div></div>
</div>
'''
rep('<!-- BLOC 1 — Principe de territorialité -->',objectives+'<!-- BLOC 1 — Principe de territorialité -->','objectives insert',True)

# ------------------------------------------------------------------
# Territory / proof framework
# ------------------------------------------------------------------
rep('(CH + Liechtenstein + enclaves Büsingen et Campione)',
    '(territoire de la Confédération + Principauté de Liechtenstein + commune allemande de Büsingen)','territory Campione',True)

# Add Samnaun nuance after the territoriality prose.
needle='Une opération localisée à l\'étranger échappe à la TVA suisse — mais peut être soumise à une TVA étrangère (UE, USA, etc.). La <strong>localisation est déterminée par la loi</strong> (art. 7-9 LTVA), <em>pas</em> par le lieu d\'émission de la facture ou la nationalité des parties.</p>'
replace='Une opération localisée à l\'étranger échappe à la TVA suisse — mais peut être soumise à une TVA étrangère. La <strong>localisation est déterminée par la loi</strong> (art. 7-9 LTVA), <em>pas</em> par le lieu d\'émission de la facture ou la nationalité des parties.</p><div class="box warning"><div class="box-icon">🗺️</div><div class="box-body"><div class="box-title">Samnaun / Sampuoir : ne pas confondre territoire TVA et territoire douanier</div><p>Pour les <strong>livraisons de biens</strong>, les vallées de Samnaun et Sampuoir sont traitées comme territoire étranger parce qu’elles sont hors territoire douanier suisse. Pour les <strong>prestations de services</strong>, elles sont considérées comme territoire suisse. Cette nuance est précisément le type de piège que M06 doit apprendre à repérer.</p></div></div>'
rep(needle,replace,'Samnaun nuance')

old_proof='''<div class="box-title">Vision AFC — Charge de la preuve de la localisation</div>
<p>La <strong>charge de la preuve</strong> de la localisation à l'étranger (= non-soumission TVA suisse) incombe à <strong>l'assujetti</strong> (art. 81 al. 3 LTVA). En contrôle, l'AFC exige des <strong>preuves matérielles</strong> : (1) contrat précisant le siège du destinataire, (2) <strong>extrait du registre du commerce étranger</strong> du destinataire, (3) justification de la nature B2B (N° TVA étranger), (4) preuve de la prestation effectivement reçue à l'étranger. <strong>Sans preuves</strong> : présomption de localisation suisse → TVA 8,1% rétroactive sur 5 ans.</p>'''
new_proof='''<div class="box-title">Vision AFC — Liberté des moyens de preuve, mais fardeau à l’assujetti</div>
<p>L’art. 81 al. 3 LTVA applique la <strong>liberté des moyens de preuve</strong>. L’assujetti supporte les conséquences d’une preuve insuffisante lorsqu’il invoque un fait diminuant l’impôt, par exemple une prestation fournie à l’étranger. Il n’existe donc pas une liste de documents « obligatoires dans tous les cas ». Un dossier solide combine selon le flux : <strong>contrat, identité et adresse du destinataire / établissement stable concerné, factures, correspondances, livrables, données de paiement, VAT ID ou registre lorsqu’ils sont pertinents</strong>. Si les faits restent non prouvés, la position fiscale peut être corrigée ; le taux et la période se déterminent ensuite selon le cas concret.</p>'''
rep(old_proof,new_proof,'proof framework',True)

# Workshop proof wording: VAT ID isn't mandatory universal proof of economic activity.
rep('Contrat, siège / établissement stable concerné, preuve d\'activité économique',
    'Contrat, siège / établissement stable concerné, éléments prouvant le destinataire et l’affectation de la prestation','workshop service proof')
rep('Pays du client, type exact de service, règles étrangères / OSS si UE',
    'Pays du destinataire, type exact de service, éléments de localisation ; droit étranger / OSS à analyser séparément','workshop B2C')

# ------------------------------------------------------------------
# Art. 23 exports / proof
# ------------------------------------------------------------------
old_export='''<div class="box-title">Sans preuve OFDF = pas d'exonération</div>
<p>La <strong>preuve matérielle de l'export</strong> est un <em>prérequis impératif</em> pour l'exonération art. 23 ch. 1. En contrôle, l'AFC vérifie la <strong>chaîne logistique complète</strong> : facture → bon de livraison → e-dec export OFDF → preuve de réception étrangère. <strong>Maillon manquant</strong> = exonération refusée = <strong>TVA 8,1% rétroactive</strong> sur 5 ans. Pour les <strong>petits envois</strong> (&lt; CHF 5'000), les justificatifs sont plus souples (LRE, suivi DHL/UPS), mais ils doivent exister.</p>'''
new_export='''<div class="box-title">Export : preuve forte, sans formalisme artificiel</div>
<p>Pour une livraison de biens transportés ou expédiés directement à l’étranger, l’exonération art. 23 doit être <strong>prouvée</strong>. La <strong>DTe d’exportation OFDF</strong> est un moyen de preuve particulièrement fort et doit être reliée à la facture et à la livraison. Mais l’art. 81 al. 3 interdit de faire dépendre toute preuve d’un seul document précis. Si une pièce manque, le professionnel <strong>reconstitue le dossier</strong> avant de conclure à une reprise : DTe / e-bordereau, transport, livraison, client, paiement et autres éléments pertinents. Une correction n’est chiffrée qu’après cette analyse.</p>'''
rep(old_export,new_export,'export evidence',True)

old_art23='''<div class="box-title">Vision AFC — Limites strictes de l’art. 23 LTVA</div>
<p>L'art. 23 LTVA exonère <strong>UNIQUEMENT</strong> les services <em>limitativement énumérés</em> par l'art. 13 OTVA : (a) prestations d'intermédiaires liées à des prestations à l'étranger, (b) prestations relatives à des foires/expositions à l'étranger, (c) prestations dans le cadre de la coopération internationale. <strong>Ce N'EST PAS</strong> une exonération générale pour tous les services B2B exportés ! Pour ces derniers, utiliser <strong>art. 8 al. 1 LTVA</strong> (hors champ, lieu = siège destinataire étranger). Confusion classique source de redressements AFC (10-50% de la matière des contrôles internationaux).</p>'''
new_art23='''<div class="box-title">Vision AFC — Art. 23 n’est pas le synonyme de « client étranger »</div>
<p>L’art. 23 contient une <strong>liste légale d’exonérations</strong> : notamment exportations de biens, certaines prestations de transport et de logistique internationales, opérations d’intermédiaires et autres cas prévus par la loi / l’ordonnance. Il n’est donc ni limité à trois services, ni une exonération générale de toute prestation internationale. Pour un service ordinaire soumis à l’art. 8 al. 1 et fourni à un destinataire à l’étranger, la conclusion suisse est généralement <strong>lieu à l’étranger / hors territoire suisse</strong>, et non « exonéré art. 23 ».</p>'''
rep(old_art23,new_art23,'art23 scope',True)

# ------------------------------------------------------------------
# Acquisition tax — broader than one SaaS template
# ------------------------------------------------------------------
rep('Le <strong>reverse charge</strong> est le <em>miroir inversé</em> de l\'art. 8 al. 1 : quand une entreprise CH <strong>reçoit</strong> un service B2B d\'un prestataire étranger non assujetti en CH, c\'est <strong>l\'acquéreur suisse qui doit auto-imposer</strong> la TVA. C\'est une erreur fréquente et coûteuse en contrôle, surtout lorsque les comptes informatiques, consulting ou marketing contiennent des factures étrangères sans TVA suisse. Exemple type : abonnement Microsoft 365 facturé depuis l\'Irlande à une PME genevoise = la PME doit déclarer la TVA suisse 8,1% en auto-imposition.',
    'L’<strong>impôt sur les acquisitions</strong> vise notamment certaines prestations de services régies par le principe du lieu du destinataire et fournies par des entreprises étrangères non inscrites en Suisse. Il peut aussi concerner <strong>certaines livraisons / travaux sans matériel importé par le prestataire</strong>, les supports de données sans valeur marchande et, depuis 2025, certains droits et certificats d’émission. Le réflexe professionnel n’est donc pas « facture étrangère = 8,1% », mais <strong>nature du flux → lieu → statut du fournisseur → exclusion / exonération → art. 45</strong>.','acquisition intro')

old_conditions='''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Mécanisme du reverse charge — 4 conditions cumulatives</h4>
<table class="comp-table">
<thead><tr><th>Condition</th><th>Détail</th></tr></thead>
<tbody>
<tr><td><strong>1. Service reçu</strong></td><td>Acquisition par entreprise CH d'un service (pas un bien)</td></tr>
<tr><td><strong>2. Prestataire étranger</strong></td><td>Siège à l'étranger ET non inscrit au registre AFC</td></tr>
<tr><td><strong>3. Lieu = Suisse</strong></td><td>Selon art. 8 al. 1 (siège du destinataire CH)</td></tr>
<tr><td><strong>4. Statut du destinataire</strong></td><td>Assujetti TVA : déclaration des acquisitions concernées. Non inscrit : seuil CHF 10'000/an déclenche l’obligation liée à l’impôt sur les acquisitions (art. 45 al. 2).</td></tr>
</tbody>
</table>'''
new_conditions='''<h4 style="font-size:14px;color:var(--navy);margin:18px 0 8px;font-weight:600">Impôt sur les acquisitions — test en 5 questions</h4>
<table class="comp-table"><thead><tr><th>Question</th><th>Contrôle</th></tr></thead><tbody>
<tr><td><strong>1. Quel flux ?</strong></td><td>Service art. 8 al. 1, certains travaux / livraisons visés, support sans valeur marchande ou droit / certificat concerné</td></tr>
<tr><td><strong>2. Où est le lieu ?</strong></td><td>Le flux doit tomber dans une catégorie imposable en Suisse pour l’impôt sur les acquisitions</td></tr>
<tr><td><strong>3. Qui fournit ?</strong></td><td>Entreprise étrangère non inscrite en Suisse, sauf règles spéciales 2025+ pour certains droits / certificats</td></tr>
<tr><td><strong>4. Exclu ou exonéré ?</strong></td><td>Pas d’impôt sur les acquisitions si la prestation est exclue ou exonérée</td></tr>
<tr><td><strong>5. Qui reçoit ?</strong></td><td>Inscrit TVA : déclarer les acquisitions concernées ; non inscrit : seuil CHF 10’000/an pour l’assujettissement à l’impôt sur les acquisitions</td></tr>
</tbody></table>'''
rep(old_conditions,new_conditions,'acquisition test',True)

# Decision tree wording to keep SaaS example but not define all acquisition tax.
rep('Question 1 : Vous recevez un service d\'un prestataire étranger ?', 'Exemple SaaS : vous recevez une prestation art. 8 al. 1 d’un prestataire étranger ?','acquisition tree title')
rep('→ <strong>REVERSE CHARGE applicable</strong> art. 45 al. 1 let. a', '→ <strong>Impôt sur les acquisitions à déclarer</strong> si les autres conditions art. 45 sont remplies','acquisition tree result')

# Microsoft status: do not assert a named multinational's Swiss registration status as timeless fact.
rep('Microsoft Ireland n\'est <em>pas</em> inscrit au registre AFC suisse.',
    'Pour l’exercice, on suppose que le fournisseur irlandais <strong>n’est pas inscrit</strong> au registre TVA suisse ; dans un dossier réel, vérifier le registre au moment de la prestation.','Microsoft assumption theory')
rep('Microsoft Ireland n\'est <strong>pas inscrite au registre AFC suisse</strong>.',
    'Hypothèse pédagogique : le fournisseur irlandais <strong>n’est pas inscrit</strong> au registre TVA suisse ; en pratique, le statut se vérifie à la date pertinente.','Microsoft assumption case')
rep('✓ <strong>Non-assujetti CH</strong> (Microsoft Ireland pas inscrite au registre AFC)',
    '✓ <strong>Non-inscrit CH</strong> dans l’hypothèse du cas (à vérifier dans le registre pour un dossier réel)','Microsoft case status')
rep('confirmé par ATF 138 II 465 Adobe','à qualifier selon sa nature et la règle de lieu applicable','remove SaaS case-law slogan')

# ------------------------------------------------------------------
# Import tax / OFDF — current DTe, correct base wording
# ------------------------------------------------------------------
rep('Cette TVA d\'importation est ensuite <strong>déductible</strong> comme IP (art. 28 al. 1 let. c) si les biens servent à l\'activité imposable. <strong>Justificatif clé</strong> : quittance <strong>e-dec OFDF</strong> avec N° de décision de taxation.',
    'Cette TVA d’importation peut ensuite être déduite comme impôt préalable (art. 28 al. 1 let. c) si les conditions sont remplies. <strong>Justificatif clé</strong> : décision de taxation électronique <strong>DTe / e-bordereau OFDF</strong> ou autre pièce douanière applicable, reliée à l’importateur, à l’acquittement et à l’affectation.','import intro DTe')
rep('<div class="formula-title">🧮 Base de calcul TVA importation (art. 54 LTVA)</div>\n<div class="formula-body">\n<strong>VALEUR EN DOUANE</strong> = Prix d\'achat HT',
    '<div class="formula-title">🧮 Base de calcul de l’impôt sur les importations — art. 54</div>\n<div class="formula-body">\n<strong>BASE</strong> = contre-prestation (vente / commission) ou valeur déterminée par l’art. 54 selon le cas','import base title')
rep('= <strong>Valeur en douane (base TVA)</strong>', '= <strong>Base de calcul TVA importation</strong>','import base label')
rep('Le calcul est effectué par OFDF dans l\'e-dec ; l\'importateur peut <strong>vérifier l\'exactitude</strong> et contester si erreur (recours à OFDF, délai 30 jours).',
    'L’OFDF établit la taxation d’importation. Le professionnel vérifie <strong>contre-prestation / valeur retenue, frais accessoires, taux, importateur et destination</strong>. Toute contestation suit la procédure et le délai indiqués dans l’acte douanier reçu ; M06 n’enseigne pas un délai unique sans identifier l’acte.','import appeal')

# Replace legacy procedure table labels without claiming one system is universal.
rep('<tr><td><strong>e-dec Import</strong></td><td>Déclaration douanière électronique standard</td><td>Importations courantes B2B</td></tr>',
    '<tr><td><strong>Déclaration douanière / Passar selon flux</strong></td><td>Procédure électronique OFDF applicable au type de trafic</td><td>Importations courantes ; conserver la décision / preuve électronique</td></tr>','import procedure modern')

# Broad e-dec cleanup in visible learning content.
for old,new in [
    ('Quittance e-dec OFDF','DTe / preuve électronique OFDF'),
    ('quittance e-dec OFDF','DTe / preuve électronique OFDF'),
    ('e-dec export OFDF','DTe d’exportation / preuve électronique OFDF'),
    ('preuve OFDF e-dec OBLIGATOIRE','preuve d’exportation OFDF / dossier probant'),
    ('e-dec Import','déclaration douanière électronique'),
    ('dans l\'e-dec','dans la taxation OFDF')]:
    rep(old,new,'legacy customs '+old[:24])

# ------------------------------------------------------------------
# Foreign businesses / representatives
# ------------------------------------------------------------------
rep('CHF 100\'000 de CA mondial annuel (ATF 140 II 202). Inclut TOUS les flux : imposable + hors champ + exonéré.',
    'CHF 100’000 de chiffre d’affaires mondial déterminant provenant de prestations qui ne sont pas exclues ; les dons, subventions, domaine non entrepreneurial et prestations qui seraient exclues en Suisse ne sont pas ajoutés comme « tous flux ».','vocab threshold',True)
rep('Personne domiciliée en CH désignée par une entreprise étrangère pour la représenter auprès de l\'AFC. Solidairement responsable.',
    'Personne physique ou morale ayant domicile / siège en Suisse, désignée pour les obligations de procédure. <strong>La créance fiscale reste à la charge de l’entreprise étrangère</strong> ; la représentation ne crée pas automatiquement une responsabilité solidaire.','vocab representative',True)

# Add a professional foreign-company test near any existing foreign-company section via safe insertion before legislation marker if available.
foreign_box='''<div class="box warning"><div class="box-icon">🌐</div><div class="box-body"><div class="box-title">Entreprise étrangère : CA mondial ≠ assujettissement suisse automatique</div><p>Le seuil de CHF 100’000 se calcule sur le <strong>chiffre d’affaires mondial déterminant</strong>, mais une entreprise étrangère ne devient assujettie en Suisse que si elle fournit aussi une prestation sur le territoire suisse et qu’aucune libération spécifique ne s’applique. Les entreprises étrangères qui ne fournissent en Suisse que certaines prestations exonérées ou des prestations de services soumises à l’impôt sur les acquisitions peuvent être libérées. La séquence correcte est donc : <strong>prestation en Suisse ? → CA mondial déterminant ? → exception / libération ? → date de début → représentant fiscal si requis</strong>.</p></div></div>'''
# insert before BLOC 9 if found, otherwise before legislation section
if '<!-- BLOC 9' in t:
    t=t.replace('<!-- BLOC 9',foreign_box+'<!-- BLOC 9',1); changes.append(('foreign company box',1))
elif '<!-- ══════════════════ LÉGISLATION' in t:
    t=t.replace('<!-- ══════════════════ LÉGISLATION',foreign_box+'<!-- ══════════════════ LÉGISLATION',1); changes.append(('foreign company box',1))
else:
    print('WARN no insertion point foreign company box')

# ------------------------------------------------------------------
# EU / foreign-law overreach — Swiss module should separate foreign verification
# ------------------------------------------------------------------
# Case 5 Q3/Q4: replace exact German VAT conclusion and mandatory docs.
sub(r'<div class="case-step" id="m6c5s3">.*?</div>\n</div>',
'''<div class="case-step" id="m6c5s3">
<div class="step-question"><span class="step-q-num">Q3</span>La LTVA suisse permet-elle à elle seule de conclure que Siemens doit auto-liquider exactement 19% en Allemagne ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m6c5s3',this,false)">A) Oui, l’art. 8 LTVA fixe aussi la TVA allemande</button><button class="step-opt" onclick="caseAnswer('m6c5s3',this,true)">B) Non — la conclusion suisse s’arrête au lieu à l’étranger ; le reverse charge, le taux et les mentions de facture relèvent du droit UE / allemand à vérifier séparément</button><button class="step-opt" onclick="caseAnswer('m6c5s3',this,false)">C) L’AFC perçoit la TVA allemande</button><button class="step-opt" onclick="caseAnswer('m6c5s3',this,false)">D) Aucune TVA étrangère ne peut jamais exister</button></div>
<div class="step-explanation" id="m6c5s3-expl">Du point de vue suisse, une prestation soumise à l’art. 8 al. 1 et fournie à l’établissement destinataire en Allemagne est <strong>hors territoire suisse</strong>. Une autoliquidation allemande est plausible pour de nombreuses prestations B2B, mais sa base, son taux et les mentions obligatoires doivent être vérifiés dans le droit UE / allemand applicable à la date de l’opération. M06 apprend précisément à séparer ces deux couches d’analyse.<div class="art-ref">📋 art. 8 al. 1 LTVA · droit étranger à vérifier séparément</div></div>
</div>''','case5 q3 foreign law',count=1,required=True)
sub(r'<div class="case-step" id="m6c5s4">.*?</div>\n</div>',
'''<div class="case-step" id="m6c5s4">
<div class="step-question"><span class="step-q-num">Q4</span>Quel dossier conserver pour défendre le lieu à l’étranger au regard de la LTVA ?</div>
<div class="step-options"><button class="step-opt" onclick="caseAnswer('m6c5s4',this,false)">A) Une liste fermée de cinq documents est toujours obligatoire</button><button class="step-opt" onclick="caseAnswer('m6c5s4',this,true)">B) Un faisceau de preuves adapté : contrat, identité / adresse du destinataire ou établissement stable concerné, facture, correspondances / livrable, paiement et VAT ID / registre si pertinents</button><button class="step-opt" onclick="caseAnswer('m6c5s4',this,false)">C) Seulement le numéro VAT UE</button><button class="step-opt" onclick="caseAnswer('m6c5s4',this,false)">D) Une décision OFDF d’importation</button></div>
<div class="step-explanation" id="m6c5s4-expl">L’art. 81 al. 3 LTVA consacre la <strong>liberté des moyens de preuve</strong>. Pour défendre le lieu à l’étranger, l’assujetti doit rendre crédibles le destinataire, l’établissement concerné et la nature de la prestation. Un VAT ID ou un extrait de registre peut être utile, mais aucun document unique n’est une condition universelle. La conservation suit les règles applicables aux pièces du dossier TVA.<div class="art-ref">📋 art. 70 + 81 al. 3 LTVA</div></div>
</div>''','case5 q4 proof',count=1,required=True)

# Case 6 foreign France outcome — replace over-specific registration/representative claims.
rep('B) Risque d\'assujettissement TVA en France (services immobiliers locaux), consulter expert TVA français + représentant fiscal',
    'B) La prestation est hors territoire suisse ; déterminer ensuite selon le droit français qui est redevable, si une immatriculation est requise et quelles mentions de facture s’appliquent','case6 France option')
sub(r'<div class="step-explanation" id="m6c6s3-expl">.*?</div>\n</div>',
'''<div class="step-explanation" id="m6c6s3-expl">La LTVA suisse permet de conclure : <strong>lieu de l’immeuble = France, donc pas de TVA suisse</strong>. Elle ne permet pas de décider à elle seule si le prestataire suisse doit s’immatriculer en France, si le client auto-liquide, quel taux s’applique ou si un représentant fiscal est requis. Ces questions dépendent du droit français et du statut concret des parties à la date de la prestation. Le dossier suisse doit donc comporter une <strong>note de hand-off</strong> : « TVA suisse : hors territoire ; TVA France : vérification locale requise ».<div class="art-ref">📋 art. 8 al. 2 let. f LTVA · droit français à vérifier</div></div>
</div>''','case6 q3 foreign law',count=1,required=True)

# ------------------------------------------------------------------
# E-commerce/platform nuances
# ------------------------------------------------------------------
rep('Régime spécial pour vendeurs étrangers livrant petits envois à particuliers CH. Seuil : 100k CHF/an déclenche assujettissement.',
    'Régime spécial pour les biens expédiés ou transportés depuis l’étranger vers des acheteurs sur le territoire suisse lorsque le fournisseur réalise au moins CHF 100’000/an de petits envois. Une fois assujetti sous ce régime, toutes ses livraisons concernées vers la Suisse sont localisées en Suisse.','vocab distance sales')
rep('Marketplace numérique (Amazon, eBay, etc.) réputée fournir les biens des vendeurs tiers ("deemed supplier") depuis 01.01.2025.',
    'Exploitant d’une plateforme numérique qui, lorsque les conditions de l’art. 20a sont remplies, est réputé fournisseur à l’égard de l’acheteur pour les livraisons facilitées. Les exceptions et le rôle contractuel doivent être vérifiés.','vocab platform')

rep('<li>Seuil : 100k CHF/an petits envois B2C</li>', '<li>Seuil : CHF 100’000/an provenant des petits envois transportés ou expédiés depuis l’étranger</li>','cheat distance sales')
rep('<li>"Petit envoi" : TVA &lt; CHF 5</li>', '<li>« Petit envoi » : impôt sur les importations de CHF 5 au plus, donc non perçu</li>','cheat small shipment')
rep('<li>"Deemed supplier" pour ventes des tiers</li>','<li>« Deemed supplier » uniquement si les conditions de facilitation art. 20a sont remplies</li>','cheat platform conditional')
rep('<li>La plateforme = assujettie TVA CH</li>','<li>L’attribution des ventes à la plateforme peut entraîner son assujettissement ; test art. 10 / art. 7 selon les flux</li>','cheat platform liability')

# ------------------------------------------------------------------
# Vocabulary precision
# ------------------------------------------------------------------
rep('Opération entre deux entreprises assujetties TVA. Lieu de prestation = siège du destinataire (preuve par N° TVA).',
    'Relation entre entreprises. En droit suisse, l’art. 8 al. 1 localise en principe la prestation au siège / établissement stable du destinataire même si l’étiquette « B2B » ou un N° TVA n’est pas, à elle seule, la règle juridique.','vocab B2B')
rep('Pour la territorialité : l\'assujetti doit prouver que le lieu de prestation est à l\'étranger (sinon présomption suisse → TVA 8,1%).',
    'Pour un fait diminuant l’impôt, l’assujetti supporte les conséquences d’une preuve insuffisante. L’art. 81 al. 3 impose toutefois la liberté des moyens de preuve ; une reprise n’est pas une formule automatique « preuve manquante = 8,1% ».','vocab proof')
rep('Service livré automatiquement par internet (SaaS, téléchargement). Règles spéciales de localisation possibles (B2C destinataire).',
    'Prestation fournie par voie électronique / automatisée selon les définitions et la pratique applicables. La qualification exacte est importante pour l’assujettissement étranger et certaines règles de lieu ; ne pas utiliser « SaaS = une catégorie unique » sans examiner le service.','vocab electronic service')

# ------------------------------------------------------------------
# Cheatsheet current-law precision
# ------------------------------------------------------------------
rep('<li>CH → CH : TVA 8,1%</li>', '<li>CH → CH : prestation sur territoire suisse ; déterminer ensuite exclusion / exonération / taux (pas toujours 8,1%)</li>','cheat CH goods')
rep('<li>Étranger → CH : <strong>Hors champ + TVA importation OFDF</strong></li>', '<li>Étranger → CH : analyser lieu de la livraison, importateur, règle art. 7 al. 3 éventuelle et TVA d’importation OFDF</li>','cheat foreign goods')
rep('<p>• N° TVA + contrat preuve</p>', '<p>• Faisceau de preuves sur le destinataire / établissement concerné ; VAT ID utile si pertinent</p>','cheat service proof')
rep('<p><strong>POINT COMMUN :</strong> DIP possible selon affectation à 100% ✓</p>', '<p><strong>POINT COMMUN :</strong> DIP potentiellement conservé selon art. 28–29, affectation et preuve ; pas de « 100% » automatique</p>','cheat DIP nuance')

# Acquisition card should not say service-only globally.
rep('<li>Service reçu (pas un bien)</li>', '<li>Identifier la catégorie visée par l’art. 45 : services art. 8 al. 1 et autres acquisitions prévues par la loi</li>','cheat acquisition scope')
rep('<p>Ch. 405 : DIP simultané</p>', '<p>Ch. 400/405 : DIP éventuel selon nature et affectation</p>','cheat acquisition DIP')

# Import card DTe and base.
rep('<p><strong>Valeur en douane (base) :</strong></p>', '<p><strong>Base art. 54 :</strong> contre-prestation / valeur applicable + frais accessoires jusqu’au lieu de destination en Suisse, selon le cas</p>','cheat import base')
rep('<p><strong>Justificatif :</strong> DTe / preuve électronique OFDF</p>', '<p><strong>Justificatif :</strong> DTe / e-bordereau / décision OFDF applicable</p>','cheat import DTe')

# ------------------------------------------------------------------
# Quiz: replace several dangerous simplifications while preserving 35 questions
# ------------------------------------------------------------------
# q01 territory nuance
sub(r'\{"id": "m06-q01".*?\}, \{"id": "m06-q02"',
'''{"id": "m06-q01", "diff": "easy", "art": "art. 3–4 LTVA", "q": "Quel ensemble décrit correctement le territoire suisse au sens TVA dans le réflexe M06 ?", "opts": ["Confédération + Campione", "Confédération + Liechtenstein + Büsingen, avec particularités pour Samnaun/Sampuoir selon biens ou services", "Uniquement territoire politique suisse", "Toute l’UE"], "correct": 1, "expl": "Le territoire TVA comprend notamment la Confédération, la Principauté de Liechtenstein et Büsingen. Samnaun/Sampuoir nécessitent une nuance : biens et services ne sont pas traités de la même façon en raison de leur situation douanière."}, {"id": "m06-q02"''','q01 territory',count=1,required=True)
# q06 evidence freedom
sub(r'\{"id": "m06-q06".*?\}, \{"id": "m06-q07"',
'''{"id": "m06-q06", "diff": "easy", "art": "art. 23 + 81 al. 3", "q": "Export de biens : quelle approche de preuve est correcte ?", "opts": ["Une facture sans TVA suffit toujours", "La DTe OFDF est une preuve forte ; relier le dossier douanier à la facture / livraison et, si une pièce manque, apprécier l’ensemble des moyens de preuve", "Sans DTe, reprise automatique 8,1% sans examen", "Une photo du colis suffit toujours"], "correct": 1, "expl": "L’export doit être prouvé. La DTe est particulièrement probante, mais la LTVA applique la liberté des moyens de preuve : le dossier se juge dans son ensemble."}, {"id": "m06-q07"''','q06 evidence',count=1,required=True)
# q08 broader acquisition
sub(r'\{"id": "m06-q08".*?\}, \{"id": "m06-q09"',
'''{"id": "m06-q08", "diff": "easy", "art": "art. 45 LTVA", "q": "Quel réflexe décrit correctement l’impôt sur les acquisitions ?", "opts": ["Toute facture étrangère est auto-imposée à 8,1%", "Identifier d’abord une catégorie visée par l’art. 45, son lieu, le statut du fournisseur et l’absence d’exclusion / exonération", "Il concerne uniquement les biens à la douane", "Il ne concerne jamais les non-inscrits"], "correct": 1, "expl": "L’art. 45 couvre notamment des services soumis au principe du destinataire et d’autres acquisitions prévues par la loi. La qualification précède le calcul."}, {"id": "m06-q09"''','q08 acquisition',count=1,required=True)
# q19 representative responsibility in explanation
sub(r'\{"id": "m06-q19".*?\}, \{"id": "m06-q20"',
'''{"id": "m06-q19", "diff": "med", "art": "art. 67 LTVA", "q": "Entreprise étrangère assujettie en Suisse sans siège / domicile / établissement stable CH : quel dispositif de procédure faut-il en principe prévoir ?", "opts": ["Ouvrir obligatoirement une SA suisse", "Désigner un représentant fiscal ayant domicile ou siège en Suisse, sauf renonciation admise par l’AFC selon la loi", "Transférer la dette au représentant", "Aucun interlocuteur suisse n’est possible"], "correct": 1, "expl": "Le représentant sert aux obligations de procédure et comme point de contact. La créance fiscale reste à la charge de l’entreprise étrangère ; sa désignation ne crée pas automatiquement un établissement stable ni une responsabilité solidaire."}, {"id": "m06-q20"''','q19 representative',count=1,required=True)
# q20 direct current formulation
sub(r'\{"id": "m06-q20".*?\}, \{"id": "m06-q21"',
'''{"id": "m06-q20", "diff": "med", "art": "représentation fiscale", "q": "Qui reste responsable du paiement de la créance TVA d’une entreprise étrangère représentée en Suisse ?", "opts": ["Toujours le représentant fiscal", "L’entreprise étrangère assujettie ; le représentant assure les obligations de représentation / contact", "Le canton du représentant", "Le client suisse"], "correct": 1, "expl": "Le formulaire AFC de représentation fiscale précise que la responsabilité du paiement de la créance incombe à l’entreprise étrangère assujettie."}, {"id": "m06-q21"''','q20 responsibility',count=1,required=True)

# q17 platform keep but sharpen
sub(r'\{"id": "m06-q17".*?\}, \{"id": "m06-q18"',
'''{"id": "m06-q17", "diff": "med", "art": "art. 20a LTVA", "q": "Que change l’art. 20a LTVA depuis 2025 ?", "opts": ["Toute plateforme devient automatiquement assujettie", "Sous conditions, l’exploitant qui facilite une livraison est réputé fournisseur à l’égard de l’acheteur, ce qui peut modifier son assujettissement", "Il supprime l’importation", "Il remplace l’art. 7"], "correct": 1, "expl": "Le mécanisme de fournisseur réputé dépend du rôle de facilitation et des conditions légales. L’attribution des ventes à la plateforme peut ensuite entraîner l’assujettissement."}, {"id": "m06-q18"''','q17 platform',count=1,required=True)

# ------------------------------------------------------------------
# Visible completion and M07 transition
# ------------------------------------------------------------------
old_end='''<div class="cheat-final">
<button class="btn btn-primary btn-lg" onclick="window.print()">🖨️ Imprimer la cheatsheet</button>
</div>
<div class="section-nav">
<button class="btn btn-ghost" onclick="goto('vocab')">← Vocabulaire</button>
<button class="btn btn-gold" onclick="goto('theory')">⬡ Recommencer M06</button>
</div>'''
new_end='''<div class="cheat-final">
<button class="btn btn-primary btn-lg" onclick="window.print()">🖨️ Imprimer la cheatsheet</button>
<p style="font-size:12px;color:var(--muted);margin-top:12px">Fin de M06 : vous devez savoir conclure séparément <strong>TVA suisse</strong> puis <strong>contrôle du droit étranger</strong>. La suite logique est M07 — Holdings &amp; groupes TVA.</p>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:14px"><a class="btn btn-ghost" href="index.html" style="text-decoration:none">← Retour au cours</a><button class="btn btn-primary" onclick="finishModule()">✓ Terminer M06</button><button class="btn btn-gold" onclick="goNextModule()">Continuer avec M07 →</button></div>
<div id="m06-complete" class="box success" style="display:none;text-align:left;margin-top:16px"><div class="box-icon">✅</div><div class="box-body"><div class="box-title">M06 enregistré comme terminé</div><p>La progression du module est à 100% et le cours principal est synchronisé. Le quiz reste une validation interne distincte.</p><div style="margin-top:10px"><a class="btn btn-primary" href="m07-holdings-groupes-tva.html" style="text-decoration:none">Aller à M07 — Holdings &amp; groupes →</a></div></div></div>
<p style="font-size:11px;color:var(--muted);margin-top:16px">Conception : <a href="https://www.linkedin.com/in/mariia-lobur/" target="_blank" rel="noopener noreferrer">Mariia Lobur</a> · <a href="https://github.com/mariialobur" target="_blank" rel="noopener noreferrer">GitHub</a></p>
</div>
<div class="section-nav">
<button class="btn btn-ghost" onclick="goto('vocab')">← Vocabulaire</button>
<button class="btn btn-gold" onclick="goto('theory')">⬡ Revoir M06</button>
</div>'''
rep(old_end,new_end,'completion UI',True)

# Preserve legacy storage key and extend state completion.
# Find state initializer dynamically.
if "completed:0" not in t and 'let state=' in t:
    t=t.replace('let state={','let state={schemaVersion:"v5_0",completed:0,',1); changes.append(('state completion',1))
elif 'schemaVersion' not in t and 'let state=' in t:
    t=t.replace('let state={','let state={schemaVersion:"v5_0",',1); changes.append(('state schema',1))
rep('const pct=Math.min(100, Math.round(done/total*100));','const pct=state.completed?100:Math.min(100, Math.round(done/total*100));','completion progress',True)

completion_js='''
function syncDashboardDone(){
  try{
    const k='tvaSpecialisteTvaDashboardV1';
    const d=JSON.parse(localStorage.getItem(k)||'{}');
    d.M06='done';
    localStorage.setItem(k,JSON.stringify(d));
  }catch(e){}
}
function finishModule(){
  state.completed=1;
  save();
  syncDashboardDone();
  const box=document.getElementById('m06-complete');
  if(box)box.style.display='flex';
  updateProgress();
}
function goNextModule(){
  finishModule();
  window.location.href='m07-holdings-groupes-tva.html';
}
'''
rep("document.addEventListener('DOMContentLoaded',()=>{",completion_js+"\ndocument.addEventListener('DOMContentLoaded',()=>{",'completion JS',True)
rep("renderCard(); });","renderCard(); if(state.completed){const box=document.getElementById('m06-complete');if(box)box.style.display='flex';} });",'completion init',True)
rep('window.nextCard=nextCard;','window.nextCard=nextCard; window.finishModule=finishModule; window.goNextModule=goNextModule;','completion exports',True)

# ------------------------------------------------------------------
# Broad cleanups of overclaims and legacy labels
# ------------------------------------------------------------------
for old,new in [
    ('Dossier expert 10/10','Territorialité & flux transfrontaliers'),
    ('source de redressements AFC (10-50% de la matière des contrôles internationaux)','source classique de confusion entre lieu, exonération et assujettissement'),
    ('l\'erreur la plus rentable à contrôler','un point classique de contrôle'),
    ('sujet n°1 contrôles AFC','point fréquent de revue'),
    ('preuve par N° TVA','preuve du destinataire / établissement concerné'),
    ('N° TVA + contrat preuve','preuves adaptées au destinataire / établissement concerné'),
    ('DIP intégral','DIP selon les conditions et l’affectation'),
]:
    rep(old,new,'broad '+old[:28])

p.write_text(t,encoding='utf-8')
print('M06 changes',len(changes))
for c in changes: print(' -',c)
