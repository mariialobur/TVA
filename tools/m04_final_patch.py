from pathlib import Path

p=Path('m04-tva-comptabilite-suisse.html')
t=p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label,required=True):
    global t
    n=t.count(old)
    if not n:
        msg='MISSING '+label
        if required:
            raise RuntimeError(msg)
        print('WARN',msg)
        return
    t=t.replace(old,new)
    changes.append((label,n))

def section(start_marker,end_marker,new,label):
    global t
    a=t.find(start_marker)
    if a<0:
        raise RuntimeError('MISSING START '+label)
    b=t.find(end_marker,a)
    if b<0:
        raise RuntimeError('MISSING END '+label)
    t=t[:a]+new+'\n'+t[b:]
    changes.append((label,1))

# ------------------------------------------------------------------
# CASE 7 — distinguish mode (art. 39) from timing (art. 40), and use
# OTVA art. 106 for transition under the effective method.
# ------------------------------------------------------------------
case7='''<!-- CAS 7 — Mode de décompte selon les contre-prestations reçues -->
<div class="case-block">
<div class="case-header">
<div class="case-num">07</div>
<div class="case-meta">
<div class="case-title">Consulting Pro SA — Passage aux contre-prestations reçues</div>
<div class="case-subtitle">Consulting B2B · Vaud · 2026 · 🟡 Risque moyen</div>
</div>
</div>
<div class="case-body">
<div class="case-scenario">
<strong>Contexte :</strong> Consulting Pro SA, conseil aux PME, DSO de 90 jours. Décompte selon les <strong>contre-prestations convenues</strong> jusqu'à fin 2025. La société a demandé à l'AFC l'autorisation de décompter selon les <strong>contre-prestations reçues</strong> au sens de l'art. 39 al. 2 LTVA; le changement prend effet au 01.01.2026.
<br/><br/><strong>Au 01.01.2026 :</strong>
<br/>• Créances clients ouvertes : <strong>CHF 540'000 TTC</strong>, déjà prises en compte sous l'ancien mode
<br/>• Dettes fournisseurs ouvertes : <strong>CHF 162'000 TTC</strong>, dont l'impôt préalable a déjà été pris en compte sous l'ancien mode
</div>
<div class="case-context">📚 <strong>Objectif :</strong> sécuriser la bascule sans double déclaration ni double déduction.</div>
<div class="case-step" id="m4c7s1">
<div class="step-question"><span class="step-q-num">Q1</span>Quel est le premier contrôle à effectuer lors du passage convenues → reçues ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c7s1',this,false)">A) Annuler toutes les factures ouvertes</button>
<button class="step-opt" onclick="caseAnswer('m4c7s1',this,true)">B) Établir l'état des débiteurs et créanciers ouverts à la date de bascule et appliquer les règles transitoires de l'art. 106 OTVA</button>
<button class="step-opt" onclick="caseAnswer('m4c7s1',this,false)">C) Redéclarer toutes les créances au premier encaissement</button>
<button class="step-opt" onclick="caseAnswer('m4c7s1',this,false)">D) Modifier uniquement le compte bancaire</button>
</div>
<div class="step-explanation" id="m4c7s1-expl">Pour la <strong>méthode effective</strong>, l'art. 106 OTVA règle le changement de mode. Lors du passage des contre-prestations convenues aux contre-prestations reçues, les postes débiteurs existants sont neutralisés dans le décompte suivant afin qu'un encaissement ultérieur ne soit pas imposé une seconde fois; de même, les postes créanciers déjà pris en compte sont neutralisés pour éviter une double déduction de l'impôt préalable. La liste d'ouverture est donc une pièce de contrôle essentielle. <div class="art-ref">📋 art. 39 LTVA · art. 106 al. 2 OTVA</div></div>
</div>
<div class="case-step" id="m4c7s2">
<div class="step-question"><span class="step-q-num">Q2</span>En février 2026, une créance de 2025 de CHF 108'000 TTC est encaissée. Quel traitement ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c7s2',this,false)">A) Déclarer à nouveau la TVA parce que l'encaissement a lieu en 2026</button>
<button class="step-opt" onclick="caseAnswer('m4c7s2',this,true)">B) Comptabiliser l'encaissement et s'assurer que la transition art. 106 neutralise cette ancienne créance dans le décompte TVA</button>
<button class="step-opt" onclick="caseAnswer('m4c7s2',this,false)">C) Annuler la facture 2025</button>
<button class="step-opt" onclick="caseAnswer('m4c7s2',this,false)">D) Reporter l'encaissement en 2027</button>
</div>
<div class="step-explanation" id="m4c7s2-expl">L'écriture de trésorerie reste <strong>D 1020 Banque / C 1100 Débiteurs</strong>. Sur le plan TVA, la créance figurait déjà dans l'ancien mode convenu; la mécanique transitoire de l'art. 106 al. 2 OTVA empêche de l'imposer une seconde fois lorsque le paiement arrive. Le contrôle doit être fait sur le décompte et sur la liste des postes ouverts, pas uniquement par une écriture standardisée. <div class="art-ref">📋 art. 106 al. 2 let. a OTVA</div></div>
</div>
<div class="case-step" id="m4c7s3">
<div class="step-question"><span class="step-q-num">Q3</span>Une nouvelle facture 2026 est payée en juin. Quand naît la créance fiscale sous le nouveau mode ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c7s3',this,false)">A) Toujours à la date de facture</button>
<button class="step-opt" onclick="caseAnswer('m4c7s3',this,true)">B) Au moment de l'encaissement, conformément aux effets temporels de l'art. 40 al. 2 LTVA</button>
<button class="step-opt" onclick="caseAnswer('m4c7s3',this,false)">C) Seulement au bouclement annuel</button>
<button class="step-opt" onclick="caseAnswer('m4c7s3',this,false)">D) À une date choisie librement par l'ERP</button>
</div>
<div class="step-explanation" id="m4c7s3-expl">L'art. 39 définit le <strong>mode de décompte</strong>; l'art. 40 en règle les effets temporels. Avec les contre-prestations reçues, la créance fiscale naît lors de l'encaissement et le droit au DIP lors du paiement, sous réserve des règles particulières. Le mode choisi doit être conservé pendant au moins une période fiscale (art. 39 al. 3). <div class="art-ref">📋 art. 39 al. 2-3 + art. 40 al. 2 LTVA</div></div>
</div>
<div class="calc-box">
<div class="calc-title">📊 Dossier de bascule — pièces à conserver</div>
<div class="calc-row"><span class="calc-label">Débiteurs ouverts au 01.01.2026</span><span class="calc-val">liste nominative + TVA déjà déclarée</span></div>
<div class="calc-row"><span class="calc-label">Créanciers ouverts au 01.01.2026</span><span class="calc-val">liste + DIP déjà pris en compte</span></div>
<div class="calc-row"><span class="calc-label">Premier décompte 2026</span><span class="calc-val">contrôle art. 106 OTVA</span></div>
<div class="calc-row total"><span class="calc-label">Objectif</span><span class="calc-val">0 double imposition · 0 double DIP</span></div>
</div>
</div>
</div>'''
section('<!-- CAS 7 — Méthode encaissement -->','<!-- CAS 8 — Subvention -->',case7,'rebuild case7 mode transition')

# Case 8 Q1: donations are not automatically treated like subsidies for DIP.
rep('''<strong>Conséquence DIP</strong> : l'art. 33 LTVA impose une <strong>réduction du DIP par prorata</strong> car la subvention finance partiellement l'activité (cumul avec art. 30 si activité exclue présente). Distinguer subvention (art. 18 al. 2 let. a) vs don (let. d) — même traitement mais qualification juridique différente.''',
'''<strong>Conséquence DIP</strong> : une subvention ou contribution assimilée au sens de l'art. 18 al. 2 let. a à c peut entraîner une <strong>réduction du DIP selon l'art. 33 al. 2</strong>; la méthode dépend de son affectation et des coûts concernés. Il faut la distinguer d'un <strong>don</strong> au sens de l'art. 18 al. 2 let. d : les éléments hors contre-prestation n'ont en principe pas d'effet sur le DIP, sous réserve précisément de l'exception prévue pour les subventions et contributions assimilées.''',
'case8 subsidy vs donation')
rep('📋 art. 18 al. 2 + 33 LTVA + ch. 420 / 900-910','📋 art. 18 al. 2 + art. 33 LTVA · ch. 420 / 900-910','case8 ref',required=False)

# ------------------------------------------------------------------
# CASE 11 — qualification of foreign services before acquisition tax.
# Exact ch. 383 depends on the nature of Stripe fees; under full DIP the
# mirror acquisition tax/DIP does not change the net liability.
# ------------------------------------------------------------------
case11='''<!-- CAS 11 — SaaS intégration ERP complète -->
<div class="case-block">
<div class="case-header">
<div class="case-num">11</div>
<div class="case-meta">
<div class="case-title">CloudWare Sàrl — Intégration ERP TVA d'un SaaS international</div>
<div class="case-subtitle">Startup SaaS B2B · Lausanne · Setup 2026 · 🔴 Risque élevé</div>
</div>
</div>
<div class="case-body">
<div class="case-scenario">
<strong>Contexte :</strong> CloudWare Sàrl, startup SaaS B2B, méthode effective selon les contre-prestations convenues. <strong>Activités 2026 :</strong>
<br/>• clients suisses : CHF 800'000 HT, prestations imposables 8,1%
<br/>• clients UE B2B : CHF 1'200'000, prestations localisées chez le destinataire à l'étranger
<br/>• clients USA B2B : CHF 600'000, prestations localisées chez le destinataire à l'étranger
<br/>• achats étrangers : AWS CHF 96'000, Stripe CHF 24'000 de frais à qualifier, Notion CHF 6'000
<br/>• bureau suisse : loyer CHF 36'000 HT + IT local CHF 12'000 HT, TVA 8,1% facturée
</div>
<div class="case-context">📚 <strong>Objectif :</strong> séparer lieu de prestation, impôt sur les acquisitions, DIP et mapping ERP.</div>
<div class="case-step" id="m4c11s1">
<div class="step-question"><span class="step-q-num">Q1</span>Comment ventiler les ventes dans le plan comptable ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c11s1',this,false)">A) Tout dans un seul compte sans distinction</button>
<button class="step-opt" onclick="caseAnswer('m4c11s1',this,true)">B) Séparer ventes suisses imposables et prestations UE/USA localisées à l'étranger, avec un mapping distinct vers le décompte</button>
<button class="step-opt" onclick="caseAnswer('m4c11s1',this,false)">C) Traiter les services UE/USA comme des exportations de biens art. 23</button>
<button class="step-opt" onclick="caseAnswer('m4c11s1',this,false)">D) Ne comptabiliser que les ventes suisses</button>
</div>
<div class="step-explanation" id="m4c11s1-expl">Les services B2B soumis au principe du destinataire sont localisés au siège du client selon l'art. 8 al. 1 LTVA. Les prestations à l'étranger sont distinguées des <strong>exportations de biens art. 23</strong>. Dans le décompte actuel, les prestations fournies à l'étranger sont notamment déduites au <strong>ch. 221</strong>, tandis que les exportations exonérées art. 23 relèvent du ch. 220. Les numéros de comptes internes sont libres; le mapping doit être documenté. <div class="art-ref">📋 art. 8 al. 1 LTVA · ch. 220/221 Décompte TVA pro</div></div>
</div>
<div class="case-step" id="m4c11s2">
<div class="step-question"><span class="step-q-num">Q2</span>Pour AWS, Stripe et Notion, peut-on appliquer automatiquement 8,1% d'impôt sur les acquisitions à CHF 126'000 ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">A) Oui — tout fournisseur étranger déclenche automatiquement l'art. 45</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,true)">B) Non — qualifier chaque prestation; AWS/Notion sont des cas typiques du principe du destinataire, tandis que les frais Stripe doivent être ventilés selon leur nature</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">C) Non — aucune prestation étrangère n'est concernée</button>
<button class="step-opt" onclick="caseAnswer('m4c11s2',this,false)">D) Seulement si le total dépasse CHF 100'000</button>
</div>
<div class="step-explanation" id="m4c11s2-expl">L'impôt sur les acquisitions n'est pas dû sur une prestation simplement parce que le fournisseur est étranger. Il faut vérifier la <strong>nature</strong>, le <strong>lieu</strong> et si la prestation est exclue ou exonérée. L'AFC précise qu'une prestation exclue du champ de l'impôt ou exonérée ne déclenche pas cet impôt. CloudWare étant déjà inscrite au registre TVA, le seuil CHF 10'000 applicable aux destinataires non inscrits n'est pas le test du cas. <div class="art-ref">📋 art. 45 LTVA · pratique AFC impôt sur les acquisitions</div></div>
</div>
<div class="case-step" id="m4c11s3">
<div class="step-question"><span class="step-q-num">Q3</span>Les dépenses du bureau suisse peuvent-elles ouvrir le droit au DIP malgré les clients étrangers ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c11s3',this,false)">A) Non — seule la part de chiffre d'affaires suisse ouvre le DIP</button>
<button class="step-opt" onclick="caseAnswer('m4c11s3',this,true)">B) En principe oui si les dépenses servent aux prestations suisses imposables et à des prestations étrangères qui ouvriraient le droit au DIP; vérifier l'affectation et l'art. 29</button>
<button class="step-opt" onclick="caseAnswer('m4c11s3',this,false)">C) Toujours exactement 50%</button>
<button class="step-opt" onclick="caseAnswer('m4c11s3',this,false)">D) Les prestations étrangères transforment automatiquement le DIP en charge</button>
</div>
<div class="step-explanation" id="m4c11s3-expl">Une prestation fournie à l'étranger ne fait pas automatiquement perdre le DIP. Pour les prestations qui seraient imposables si elles étaient fournies en Suisse, le droit à déduction peut être conservé dans les conditions légales, notamment selon l'art. 29. Il faut néanmoins contrôler l'affectation réelle et l'absence d'activités exclues ou non entrepreneuriales. Dans ce cas pédagogique, les CHF 48'000 HT de loyer/IT donnent un DIP suisse de <strong>CHF 3'888</strong> si toutes les conditions sont remplies. <div class="art-ref">📋 art. 28-30 LTVA · art. 29 pour prestations à l'étranger</div></div>
</div>
<div class="case-step" id="m4c11s4">
<div class="step-question"><span class="step-q-num">Q4</span>Peut-on déjà calculer un ch. 383 exact avec les seules données du cas ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c11s4',this,false)">A) Oui : CHF 10'206 obligatoirement</button>
<button class="step-opt" onclick="caseAnswer('m4c11s4',this,true)">B) Non : le montant exact dépend notamment de la qualification des frais Stripe; si tout impôt sur acquisitions admissible ouvre symétriquement le DIP, il est neutre dans le calcul net</button>
<button class="step-opt" onclick="caseAnswer('m4c11s4',this,false)">C) Oui : CHF 0 obligatoirement</button>
<button class="step-opt" onclick="caseAnswer('m4c11s4',this,false)">D) Le ch. 383 dépend uniquement du chiffre d'affaires suisse</button>
</div>
<div class="step-explanation" id="m4c11s4-expl">Le chiffre exact de l'impôt sur les acquisitions doit attendre la qualification des frais Stripe. En revanche, sous l'hypothèse que les acquisitions imposables sont <strong>entièrement affectées à une activité ouvrant le DIP</strong>, l'impôt sur les acquisitions et le DIP correspondant se neutralisent. La dette nette pédagogique peut alors être lue comme TVA sur ventes suisses CHF 64'800 moins DIP suisse sur loyer/IT CHF 3'888 = <strong>CHF 60'912</strong>, sous réserve des autres opérations et corrections du dossier. <div class="art-ref">📋 art. 28 + 45 LTVA · qualification avant calcul</div></div>
</div>
<div class="calc-box">
<div class="calc-title">📊 Décompte prévisionnel — logique, pas fausse précision</div>
<div class="calc-row"><span class="calc-label">Ch. 200 — contre-prestations mondiales du cas</span><span class="calc-val">CHF 2'600'000</span></div>
<div class="calc-row"><span class="calc-label">Ch. 221 — prestations localisées à l'étranger</span><span class="calc-val">CHF 1'800'000</span></div>
<div class="calc-row"><span class="calc-label">Base suisse 8,1%</span><span class="calc-val">CHF 800'000</span></div>
<div class="calc-row"><span class="calc-label">TVA sur ventes suisses</span><span class="calc-val">CHF 64'800</span></div>
<div class="calc-row"><span class="calc-label">Ch. 383 — acquisitions étrangères</span><span class="calc-val">à déterminer après qualification</span></div>
<div class="calc-row"><span class="calc-label">DIP suisse loyer + IT</span><span class="calc-val">CHF 3'888</span></div>
<div class="calc-row"><span class="calc-label">DIP sur acquisitions imposables</span><span class="calc-val">selon qualification + droit à déduction</span></div>
<div class="calc-row highlight"><span class="calc-label">Net pédagogique si acquisitions tax/DIP se neutralisent</span><span class="calc-val">CHF 60'912</span></div>
</div>
</div>
</div>'''
section('<!-- CAS 11 — SaaS intégration ERP complète -->','<!-- CAS 12 — Synthèse examen professionnel -->',case11,'rebuild case11 acquisition qualification')

# ------------------------------------------------------------------
# CASE 12 — ch. 200 gross considerations, ch. 235 separately; subsidy
# adjustment cannot be fabricated without allocation data.
# ------------------------------------------------------------------
case12='''<!-- CAS 12 — Synthèse examen professionnel -->
<div class="case-block">
<div class="case-header">
<div class="case-num">12</div>
<div class="case-meta">
<div class="case-title">Industries Romandes SA — Synthèse de clôture professionnelle</div>
<div class="case-subtitle">Industrie manufacturière · Vaud · Clôture 2025 · 🔴 Risque élevé</div>
</div>
</div>
<div class="case-body">
<div class="case-scenario">
<strong>Contexte :</strong> Industries Romandes SA, méthode effective selon les contre-prestations convenues. <strong>Données 2025 :</strong>
<br/>• ventes suisses 8,1% avant escomptes : CHF 2'780'000
<br/>• exportations de biens art. 23 : CHF 920'000, preuves OFDF disponibles
<br/>• escomptes accordés sur les ventes suisses : CHF 38'000
<br/>• subvention Innosuisse R&amp;D : CHF 145'000, mais le dossier fourni ne précise pas encore les coûts/projet financés
<br/>• DIP sur matières : CHF 142'000; DIP sur loyer : CHF 9'720
<br/>• SaaS étranger imposable au titre de l'art. 45 : CHF 18'000 HT; hypothèse pédagogique : DIP correspondant intégralement admis
</div>
<div class="case-context">📚 <strong>Objectif :</strong> séparer concordance du chiffre d'affaires, déductions, acquisitions et réduction du DIP liée à la subvention.</div>
<div class="case-step" id="m4c12s1">
<div class="step-question"><span class="step-q-num">Q1</span>Comment présenter la concordance ch. 200 / escomptes ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c12s1',this,false)">A) Déclarer directement CHF 3'662'000 au ch. 200 après escomptes</button>
<button class="step-opt" onclick="caseAnswer('m4c12s1',this,true)">B) Ch. 200 = CHF 3'700'000 de contre-prestations avant déductions; contrôler séparément CHF 920'000 au ch. 220 et CHF 38'000 de réductions au ch. 235</button>
<button class="step-opt" onclick="caseAnswer('m4c12s1',this,false)">C) Ajouter la subvention au ch. 200</button>
<button class="step-opt" onclick="caseAnswer('m4c12s1',this,false)">D) Ajouter l'impôt sur acquisitions au chiffre d'affaires</button>
</div>
<div class="step-explanation" id="m4c12s1-expl">Le ch. 200 reprend le <strong>total des contre-prestations</strong> avant les déductions du bloc chiffre d'affaires. Ici : CHF 2'780'000 + CHF 920'000 = <strong>CHF 3'700'000</strong>. Les exportations art. 23 sont ensuite déduites au ch. 220 et les diminutions de contre-prestation sont contrôlées au ch. 235. La subvention est un mouvement hors contre-prestation et ne doit pas être mélangée au ch. 200. <div class="art-ref">📋 Décompte TVA pro · art. 23 + 41 + 72 LTVA</div></div>
</div>
<div class="case-step" id="m4c12s2">
<div class="step-question"><span class="step-q-num">Q2</span>Peut-on calculer immédiatement la réduction du DIP art. 33 avec le seul montant de la subvention ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c12s2',this,false)">A) Oui — toujours subvention / (subvention + chiffre d'affaires)</button>
<button class="step-opt" onclick="caseAnswer('m4c12s2',this,true)">B) Non — il faut d'abord identifier l'affectation de la subvention Innosuisse et les coûts/domaines qu'elle finance</button>
<button class="step-opt" onclick="caseAnswer('m4c12s2',this,false)">C) Non — les subventions n'ont jamais d'effet sur le DIP</button>
<button class="step-opt" onclick="caseAnswer('m4c12s2',this,false)">D) Oui — toujours 50%</button>
</div>
<div class="step-explanation" id="m4c12s2-expl">L'art. 33 al. 2 prévoit une réduction du DIP pour les subventions et contributions assimilées, mais la <strong>méthode</strong> dépend de l'affectation. Pour une aide R&amp;D, le premier réflexe est d'identifier le projet ou domaine financé et les charges concernées. Une affectation directe prime lorsqu'elle est possible; une clé globale n'est retenue que si elle donne un résultat approprié et documenté. <div class="art-ref">📋 art. 33 LTVA · pratique AFC subventions</div></div>
</div>
<div class="case-step" id="m4c12s3">
<div class="step-question"><span class="step-q-num">Q3</span>Quel montant de DIP peut-on chiffrer avant la réduction art. 33 ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c12s3',this,false)">A) CHF 146'000 après un prorata automatique de 3,77%</button>
<button class="step-opt" onclick="caseAnswer('m4c12s3',this,true)">B) CHF 153'178 avant réduction art. 33 : 151'720 de DIP suisse + 1'458 de DIP sur acquisition étrangère, sous les hypothèses du cas</button>
<button class="step-opt" onclick="caseAnswer('m4c12s3',this,false)">C) CHF 142'000 uniquement</button>
<button class="step-opt" onclick="caseAnswer('m4c12s3',this,false)">D) CHF 0</button>
</div>
<div class="step-explanation" id="m4c12s3-expl">DIP suisse : CHF 142'000 + CHF 9'720 = <strong>CHF 151'720</strong>. Le SaaS étranger génère, dans l'hypothèse donnée, CHF 18'000 × 8,1% = <strong>CHF 1'458</strong> d'impôt sur acquisitions et un DIP miroir de même montant si le droit à déduction est intégral. Avant toute réduction liée à la subvention, le DIP chiffrable est donc <strong>CHF 153'178</strong>. Le ch. 420 reste à déterminer après analyse du financement. <div class="art-ref">📋 art. 28 + 33 + 45 LTVA</div></div>
</div>
<div class="case-step" id="m4c12s4">
<div class="step-question"><span class="step-q-num">Q4</span>Quel est le bon niveau de précision pour la dette TVA finale ?</div>
<div class="step-options">
<button class="step-opt" onclick="caseAnswer('m4c12s4',this,false)">A) CHF 79'180 exactement</button>
<button class="step-opt" onclick="caseAnswer('m4c12s4',this,true)">B) Calculer un net provisoire avant art. 33, puis ajouter la réduction DIP documentée au ch. 420 pour obtenir la dette finale</button>
<button class="step-opt" onclick="caseAnswer('m4c12s4',this,false)">C) Ignorer la subvention</button>
<button class="step-opt" onclick="caseAnswer('m4c12s4',this,false)">D) Appliquer 3,77% à tout le DIP sans autre pièce</button>
</div>
<div class="step-explanation" id="m4c12s4-expl">Après escomptes suisses de CHF 38'000, la base imposable 8,1% est CHF 2'742'000, soit <strong>CHF 222'102</strong> de TVA sur ventes. L'impôt sur acquisitions du SaaS est CHF 1'458, donc TVA due avant DIP = CHF 223'560. Avec un DIP avant réduction art. 33 de CHF 153'178, le <strong>net provisoire</strong> est CHF 70'382. La dette finale devient <strong>CHF 70'382 + la réduction DIP ch. 420 correctement documentée</strong>. <div class="art-ref">📋 calcul de clôture · art. 33 à finaliser</div></div>
</div>
<div class="calc-box">
<div class="calc-title">📊 Industries Romandes SA — état provisoire avant art. 33</div>
<div class="calc-row"><span class="calc-label">Ch. 200 — total contre-prestations</span><span class="calc-val">CHF 3'700'000</span></div>
<div class="calc-row"><span class="calc-label">Ch. 220 — exportations art. 23</span><span class="calc-val">CHF 920'000</span></div>
<div class="calc-row"><span class="calc-label">Ch. 235 — escomptes sur ventes suisses</span><span class="calc-val">CHF 38'000</span></div>
<div class="calc-row"><span class="calc-label">Base suisse 8,1% après escomptes</span><span class="calc-val">CHF 2'742'000</span></div>
<div class="calc-row"><span class="calc-label">TVA sur ventes</span><span class="calc-val">CHF 222'102</span></div>
<div class="calc-row"><span class="calc-label">Ch. 383 — SaaS étranger</span><span class="calc-val">CHF 1'458</span></div>
<div class="calc-row"><span class="calc-label">DIP avant art. 33</span><span class="calc-val">CHF 153'178</span></div>
<div class="calc-row"><span class="calc-label">Ch. 420 — réduction liée à la subvention</span><span class="calc-val">à déterminer après affectation</span></div>
<div class="calc-row highlight"><span class="calc-label">Net provisoire avant ch. 420</span><span class="calc-val">CHF 70'382</span></div>
</div>
<div class="box afc" style="margin-top:16px"><div class="box-icon">🏛️</div><div class="box-body"><div class="box-title">Dossier encore incomplet — c'est le bon diagnostic</div><p>La concordance du chiffre d'affaires, les exportations, les escomptes et le SaaS peuvent être contrôlés. En revanche, la réduction du DIP liée à la subvention Innosuisse ne doit pas être inventée à partir d'un ratio de chiffre d'affaires. Il faut obtenir la convention/décision de financement, identifier le projet et les coûts financés, puis documenter la méthode de réduction retenue.</p></div></div>
</div>
</div>'''
section('<!-- CAS 12 — Synthèse examen professionnel -->','<div class="section-nav">\n<button class="btn btn-ghost" onclick="goto(\'legis\')">',case12,'rebuild case12 closing synthesis')

# ------------------------------------------------------------------
# ERRORS — replace residual legacy shortcuts.
# ------------------------------------------------------------------
error2='''<!-- ERREUR 2 -->
<div class="error-block">
<div class="error-head"><div class="error-num">02</div><div class="error-title">Acquisition étrangère comptabilisée sans qualification TVA</div><div class="error-impact">Impact : déclaration inexacte / DIP erroné</div></div>
<div class="error-body">
<div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">Toutes les factures étrangères (AWS, Adobe, Stripe, Notion, conseil, finance, etc.) sont envoyées automatiquement au ch. 383 avec 8,1%, ou au contraire aucune n'est analysée.</div></div>
<div class="error-section"><div class="error-section-title">Base légale</div><div class="error-text">Art. 8 et 45 LTVA. L'impôt sur les acquisitions suppose une prestation entrant dans son champ; une prestation exclue ou exonérée n'est pas imposée au titre de l'art. 45.</div></div>
<div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Qualifier le type de prestation, son lieu, le statut du fournisseur et les éventuelles exclusions/exonérations; seulement ensuite calculer le ch. 383. Examiner séparément le droit au DIP. En cas d'erreur passée, corriger la période concernée via le Portail AFC selon les règles de rectification/finalisation applicables.</div></div>
</div>
</div>'''
section('<!-- ERREUR 2 -->','<!-- ERREUR 3 -->',error2,'rebuild error2 acquisitions')

error3='''<!-- ERREUR 3 -->
<div class="error-block">
<div class="error-head"><div class="error-num">03</div><div class="error-title">Finalisation annuelle mal comprise</div><div class="error-impact">Impact : écarts non corrigés dans le bon délai</div></div>
<div class="error-body">
<div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">La fiduciaire pense devoir envoyer chaque année un « formulaire de concordance » même sans erreur, ou mémorise uniquement un délai de 240 jours sans rattacher la correction à la période de décompte prévue par l'art. 72.</div></div>
<div class="error-section"><div class="error-section-title">Base légale</div><div class="error-text">Art. 72 LTVA : les différences constatées lors de la concordance annuelle doivent être corrigées au plus tard dans le décompte de la période pendant laquelle tombe le <strong>180e jour</strong> suivant la fin de l'exercice. Si aucune erreur n'est constatée, aucun décompte rectificatif n'est requis.</div></div>
<div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Conserver le tableau de concordance dans le dossier de clôture. Pour chaque écart, identifier la période d'origine et utiliser la correction appropriée sur le Portail AFC; documenter le contrôle même lorsque l'écart final est nul.</div></div>
</div>
</div>'''
section('<!-- ERREUR 3 -->','<!-- ERREUR 4 -->',error3,'rebuild error3 finalisation')

# Error 4: remove vendor automation claim.
rep('Vérifier le paramétrage ERP : Bexio/Abacus doivent lier automatiquement le compte 3800 au ch. 235.',
    'Vérifier le paramétrage ERP : la réduction de contre-prestation doit être mappée correctement vers le décompte; le nom du compte ou du code dépend du logiciel.',
    'error4 vendor-neutral mapping',required=False)

error5='''<!-- ERREUR 5 -->
<div class="error-block">
<div class="error-head"><div class="error-num">05</div><div class="error-title">Solde TVA au bilan non rapproché</div><div class="error-impact">Impact : piste d'audit incomplète</div></div>
<div class="error-body">
<div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">Un compte technique TVA affiche un solde important ou inhabituel à la date de clôture sans tableau expliquant les périodes non encore décomptées, paiements/remboursements en transit, corrections ou écritures de régularisation.</div></div>
<div class="error-section"><div class="error-section-title">Base légale</div><div class="error-text">Art. 957a CO : comptabilité complète, fidèle, systématique et justifiée. Art. 958 CO : les comptes doivent permettre à un tiers de se faire une opinion fondée sur la situation économique. Art. 70-72 LTVA : traçabilité entre livres et décomptes.</div></div>
<div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Rapprocher chaque compte TVA avec les décomptes, les périodes ouvertes et les mouvements AFC. Un solde inhabituel déclenche une investigation; il n'existe pas de règle universelle selon laquelle le 2200 doit « contenir Q4 uniquement ». Une mention en annexe n'est nécessaire que si les règles comptables l'exigent ou si l'information est significative.</div></div>
</div>
</div>'''
section('<!-- ERREUR 5 -->','<!-- ERREUR 6 -->',error5,'rebuild error5 VAT balance')

error6='''<!-- ERREUR 6 -->
<div class="error-block">
<div class="error-head"><div class="error-num">06</div><div class="error-title">Archivage électronique sans dispositif probant</div><div class="error-impact">Impact : preuve difficile à reconstituer</div></div>
<div class="error-body">
<div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">Les factures existent dans un cloud, un disque partagé ou un ERP, mais personne ne peut expliquer les droits d'accès, la traçabilité des modifications, la politique de conservation, les sauvegardes ni la manière de retrouver une pièce depuis une écriture TVA.</div></div>
<div class="error-section"><div class="error-section-title">Base légale</div><div class="error-text">Art. 958f CO, art. 70 LTVA et OLICO. La conformité ne se déduit ni du nom d'un fournisseur cloud ni d'un format de fichier unique; elle dépend du dispositif concret de conservation et de vérifiabilité.</div></div>
<div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Documenter les supports utilisés, droits et changements, sauvegardes, durées, procédures de migration et tests de restauration/recherche. Vérifier qu'un tiers peut suivre la piste <strong>pièce → comptabilité → décompte TVA</strong> et inversement pendant la durée de conservation applicable.</div></div>
</div>
</div>'''
section('<!-- ERREUR 6 -->','<!-- ERREUR 7 -->',error6,'rebuild error6 archiving')

error7='''<!-- ERREUR 7 -->
<div class="error-block">
<div class="error-head"><div class="error-num">07</div><div class="error-title">Investissements sans registre de suivi TVA</div><div class="error-impact">Impact : corrections d'affectation difficiles</div></div>
<div class="error-body">
<div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">Les acquisitions d'investissement ne sont pas identifiables séparément des charges courantes, de sorte que la date, le DIP initial et les changements d'utilisation ne peuvent plus être reconstitués.</div></div>
<div class="error-section"><div class="error-section-title">Base légale</div><div class="error-text">Art. 31-32 LTVA pour les corrections liées à l'affectation, complétés par les obligations générales de tenue et conservation. Les numéros de comptes 1170/1171 ne sont pas imposés par la loi.</div></div>
<div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Mettre en place un registre des investissements avec date, base, TVA, droit au DIP, affectation et changements ultérieurs. Un sous-compte distinct (p. ex. 1171) peut être utile, mais un registre auxiliaire fiable peut remplir la même fonction de contrôle.</div></div>
</div>
</div>'''
section('<!-- ERREUR 7 -->','<!-- ERREUR 8 -->',error7,'rebuild error7 investments')

error8='''<!-- ERREUR 8 -->
<div class="error-block">
<div class="error-head"><div class="error-num">08</div><div class="error-title">Changement TDFN ↔ effective sans dossier de transition</div><div class="error-impact">Impact : valeur résiduelle et premier décompte erronés</div></div>
<div class="error-body">
<div class="error-section"><div class="error-section-title">Symptôme</div><div class="error-text">L'entreprise change de méthode de décompte, mais aucun inventaire ne documente les biens et prestations encore présents, leur valeur résiduelle, le traitement du dernier/premier décompte et la date d'effet du changement.</div></div>
<div class="error-section"><div class="error-section-title">Base légale</div><div class="error-text">Art. 37 LTVA, OTVA et pratique AFC applicables aux TDFN. Depuis 2025, les changements entre méthode effective et TDFN entraînent des corrections sur la <strong>valeur résiduelle</strong>; l'ancienne règle pédagogique « trois ans en effective avant retour » ne doit plus être utilisée comme réflexe. Le changement peut intervenir après une période fiscale complète, sous réserve des conditions et délais applicables.</div></div>
<div class="error-section"><div class="error-section-title">Correction</div><div class="error-text">Conserver la demande/validation ou modalité du Portail AFC, l'inventaire de transition et le calcul de valeur résiduelle. Lors du passage effective → TDFN, contrôler la correction dans le dernier décompte effectif; lors du passage TDFN → effective, contrôler le dégrèvement admissible dans le premier décompte effectif (notamment ch. 410 selon la pratique actuelle). Mention en annexe seulement si les règles comptables l'exigent ou si l'information est significative.</div></div>
</div>
</div>'''
section('<!-- ERREUR 8 -->','<div class="section-nav">\n<button class="btn btn-ghost" onclick="goto(\'cases\')">',error8,'rebuild error8 TDFN transition')

# Final targeted cleanup of residual legacy wording where exact fragments remain.
rep('Art. 958 OR — image fidèle.','Art. 958 CO — objectif des comptes : permettre une opinion fondée.', 'residual image fidele', required=False)
rep('concordance annuelle non déposée (concordance annuelle)','finalisation annuelle non documentée', 'residual concordance title', required=False)

p.write_text(t,encoding='utf-8')
print('Applied final M04 corrections:',sum(n for _,n in changes))
for item in changes:
    print(' -',item)
