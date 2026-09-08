from pathlib import Path
import re

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
        print('WARN missing',label)

def sub(pattern,repl,label,flags=re.S):
    global t
    t2,n=re.subn(pattern,repl,t,flags=flags)
    if n:
        t=t2; changes.append((label,n))
    else:
        print('WARN missing regex',label)

# Public/professional wording and semantic structure.
rep('← Dashboard','← Tableau de bord','dashboard wording')
rep('Formation de spécialiste TVA suisse · M08 v4.3','Formation de spécialiste TVA suisse · M08','footer version')
rep('v4.3 — final 10/10 immobilier','Immobilier & construction · édition professionnelle','top version')
rep('12 blocs + dossier premium','12 blocs · dossier fiduciaire','hero premium')
rep('⬛ Risque Noir AFC','⚠️ Risque fiscal élevé','hero risk')
rep('🏛 Vision AFC chaque bloc','🏛 LTVA · OTVA · pratique AFC','hero afc')
rep('<div class="hero-h">TVA Immobilier &amp; Construction</div>','<h1 class="hero-h">TVA Immobilier &amp; Construction</h1>','semantic h1')
rep('<strong>8 cas pratiques</strong><br/>~1h30','<strong>9 cas pratiques</strong><br/>~1h30','case count')
rep('Dossier immobilier premium','Dossier immobilier professionnel','dossier wording')
rep('Dossier premium','Dossier professionnel','cards wording')
rep('Risque Noir','Risque critique','risk wording')

# Remove unverified / misattributed case-law claims from the whole module.
for old,new,label in [
 ('ATF 140 II 88','art. 30 LTVA · pratique AFC','fake mixed-use case'),
 ('ATAF A-2454/2020','art. 38 LTVA · Info TVA 11','unverified art38 case'),
 ('ATF 138 II 239','principe de substance économique et interdiction de l’abus','misapplied abuse case'),
 ('ATF 126 II 249','art. 70–72 LTVA · concordance','misapplied concordance case'),
 ('ATAF A-5106/2020','art. 21–22 LTVA · pratique AFC immobilier','unverified DDP case')]:
    rep(old,new,label)

# Option: legal exercise is invoice/receipt indication or VAT return declaration; contract is evidence, not a statutory third condition.
old='''<div class="box info"><div class="box-icon">📋</div><div class="box-body"><div class="box-title">Conditions de l'option art. 22 — 3 critères cumulatifs</div>
    1. <strong>Opération optionnable</strong> : prestations immobilières visées par art. 21 al. 2 ch. 20/21 LTVA, sous réserve de l'art. 22<br/>
    2. <strong>Usage non exclusivement résidentiel</strong> : l'option est exclue si le destinataire affecte ou compte affecter l'objet exclusivement à l'habitation<br/>
    3. <strong>Documentation claire</strong> : clause d'option, contrat, usage prévu, ventilation des surfaces et traitement comptable
    </div></div>'''
new='''<div class="box info"><div class="box-icon">📋</div><div class="box-body"><div class="box-title">Option art. 22 — règle légale et dossier de preuve</div>
    <strong>Règle :</strong> l'assujetti peut opter pour une prestation exclue lorsque l'art. 22 le permet. En immobilier, l'option est bloquée si le destinataire affecte ou compte affecter l'objet <strong>exclusivement à des fins d'habitation</strong>.<br/>
    <strong>Exercice de l'option :</strong> indication claire de la TVA sur la facture/quittance <em>ou</em> déclaration de l'imposition dans le décompte TVA.<br/>
    <strong>Preuve recommandée :</strong> bail/acte, clause TVA, usage prévu et réel, ventilation des surfaces et piste comptable. Ces pièces sécurisent le dossier mais ne constituent pas un « troisième critère légal cumulatif » inventé.
    </div></div>'''
rep(old,new,'option rule')

# Parking is taxable by default when not public-domain, except accessory to an excluded property rental.
rep("<tr><td>Place parking commerciale</td><td style=\"color:var(--amber)\">Exclu — optionnable séparément</td><td style=\"color:var(--sage)\">Oui si option</td><td style=\"color:var(--sage)\">Oui si option valable ; à documenter selon usage</td></tr>","<tr><td>Place de parc privée indépendante</td><td style=\"color:var(--sage)\">Imposable de plein droit au taux normal</td><td style=\"color:var(--sage)\">Selon affectation</td><td>Pas d'option nécessaire</td></tr>",'parking row')
rep("Un garage situé dans un immeuble résidentiel et loué au même locataire que l'appartement = accessoire résidentiel = exclu, pas d'option possible. En revanche, un parking dans un bâtiment commercial distinct loué à une entreprise assujettie = optionnable séparément.","Une place de parc n'appartenant pas au domaine public est en principe imposable au taux normal. Exception : lorsqu'elle constitue une prestation accessoire à une location immobilière exclue (par ex. appartement avec place liée), elle suit le traitement de la location principale.",'parking warning')
rep('Le bail de parking isolé peut être optionné séparément.','Une place de parc privée indépendante est en principe imposable de plein droit ; vérifier seulement si elle est l’accessoire d’une location immobilière exclue.','parking intro')

# Remove unsupported claims of systematic cross-checking with land registers/permits.
rep("L'AFC reçoit les avis des autorités du registre foncier pour chaque mutation immobilière. Elle croise avec les décomptes TVA du vendeur pour vérifier si une correction d'affectation art. 31 était due. Un vendeur qui a déduit du DIP récemment et vend sans option = point de contrôle important pour l'AFC.","Lors d'un contrôle, l'AFC peut demander les actes, l'historique du bien, les factures de travaux et le registre de l'impôt préalable. Une vente sans option après une période d'utilisation ouvrant droit au DIP impose donc de tester immédiatement l'art. 31 et la valeur résiduelle.",'land registry claim')
rep("Les permis de construire sont consultables et croisés avec les décomptes TVA.","Les permis, plans et actes peuvent constituer des pièces utiles pour documenter la destination prévue et l'usage réel de l'immeuble.",'permit cross-check claim')
rep("L'AFC peut rapprocher paiements étrangers, factures de chantier, permis de construire, décomptes TVA et registre des immobilisations.","Dans un contrôle, les contrats, factures étrangères, documents douaniers, preuves de paiement et registre des immobilisations doivent permettre de reconstituer le traitement TVA.",'foreign cross-check claim')

# Mixed use: direct allocation first, then objective residual key. Surface is not universally mandatory or priority.
rep('Clé surface (m²)</td><td>Surface imposable / Surface totale × DIP</td><td style="color:var(--sage)">✅ Prioritaire — simple et objective','Clé surface (m²)</td><td>Surface imposable / Surface totale × DIP commun</td><td style="color:var(--sage)">✅ Possible si elle reflète l’utilisation réelle','surface priority')
rep('Clé recettes</td><td>CA imposable / CA total × DIP</td><td style="color:var(--sage)">✅ Acceptable si commerces à loyers élevés','Clé recettes</td><td>Recettes pertinentes / recettes totales × DIP commun</td><td style="color:var(--sage)">✅ Possible si elle est économiquement représentative','revenue key')
rep('Clé combinée par poste</td><td>Chaque charge selon son usage réel (ascenseur, chauffage)</td><td style="color:var(--sage)">✅ Idéale mais complexe','Affectation directe + clé résiduelle</td><td>Charges directes d’abord ; clé seulement pour les vrais coûts communs</td><td style="color:var(--sage)">✅ Réflexe professionnel','direct allocation')

# Replace the invented jurisprudence block with a hierarchy-of-sources block.
sub(r'<!-- B8 -->.*?<div class="block">\s*<div class="block-h"><span class="bnum">9</span>', '''<!-- B8 -->
<div class="block">
<div class="block-h"><span class="bnum">8</span><h3>Hiérarchie des sources — ne pas inventer une jurisprudence « de référence »</h3></div>
<div class="box fidu"><div class="box-icon">⚖️</div><div class="box-body"><div class="box-title">Méthode juridique</div>Pour chaque dossier : <strong>LTVA → OTVA → pratique AFC en vigueur → jurisprudence réellement pertinente et vérifiée</strong>. Un numéro d'arrêt ne doit apparaître dans le cours que si son objet et son considérant soutiennent précisément la règle enseignée.</div></div>
<table class="tbl"><thead><tr><th>Niveau</th><th>Usage dans M08</th></tr></thead><tbody>
<tr><td>LTVA</td><td>Art. 21–22 : exclusion/option ; art. 24 al. 6 let. c : valeur du sol ; art. 28–32 : DIP et changements d'affectation ; art. 38 : procédure de déclaration ; art. 45 : acquisitions.</td></tr>
<tr><td>OTVA</td><td>Art. 69–74 : correction/dégrèvement, valeur résiduelle, biens fabriqués par l'assujetti et rénovations importantes.</td></tr>
<tr><td>Pratique AFC</td><td>Info TVA 17 Immeubles, Info TVA 09/10 sur le DIP, Info TVA 11 procédure de déclaration, Info TVA 14 impôt sur les acquisitions.</td></tr>
<tr><td>Jurisprudence</td><td>À utiliser seulement après vérification du texte de l'arrêt et de sa pertinence pour le cas concret.</td></tr>
</tbody></table>
<div class="box ok"><div class="box-icon">✅</div><div class="box-body"><div class="box-title">Compétence visée</div>L'apprenant doit pouvoir défendre la qualification avec la norme correcte, sans transformer une pratique administrative ou un simple outil de preuve en condition légale.</div></div>
</div>
<div class="block">
<div class="block-h"><span class="bnum">9</span>''','source hierarchy')

# Add current residual-value / major-renovation rules to block 11.
rep("<div class=\"box warn\"><div class=\"box-icon\">⚠️</div><div class=\"box-body\"><div class=\"box-title\">Ne pas confondre</div>La prescription de créance fiscale n'est pas la même chose que la période économique de surveillance de 20 ans pour les immeubles. Le registre doit permettre de recalculer rapidement la valeur résiduelle en cas de vente, location, option, changement d'usage ou art. 38.</div></div>","<div class=\"box warn\"><div class=\"box-icon\">⚠️</div><div class=\"box-body\"><div class=\"box-title\">Valeur résiduelle et grosses rénovations</div>Pour les immeubles, art. 31 et 32 appliquent une réduction linéaire de <strong>1/20 par année écoulée</strong>. Selon l'OTVA, la valeur du sol est exclue du calcul de la valeur résiduelle. Si les coûts d'une phase de rénovation dépassent <strong>5% de la valeur d'assurance du bâtiment avant rénovation</strong>, les règles des art. 71/74 OTVA imposent une analyse sur l'ensemble des coûts de la phase, y compris les dépenses de maintien de valeur.</div></div>",'residual rules')

# Case 1: private use from the outset means the original deduction was wrong; do not fabricate a later art.31 change.
sub(r'<!-- CAS 1 -->.*?<!-- CAS 2 -->', '''<!-- CAS 1 -->
<div class="case-card"><div class="case-head"><div class="case-n">1</div><div class="case-meta"><div class="case-title">Villa privée — DIP déduit à tort dès l'origine</div><div class="case-sub">Art. 28–29 LTVA · affectation privée/exclue</div></div><span class="risk risk-g">🟢 Qualification</span></div><div class="case-body">
<div class="scenario">M. Rochat exploite une entreprise de maçonnerie assujettie. Il rénove sa villa utilisée exclusivement à titre privé et fait comptabiliser CHF 18'200 de TVA comme DIP de l'entreprise.</div>
<div class="step" id="c1s1"><div class="step-q"><span class="step-qn">Q1</span> Le DIP est-il déductible ?</div><div class="step-opts"><button class="opt" onclick="CASES.answer('c1s1',this,true,'Correct. L’affectation privée ne donne pas droit au DIP de l’entreprise.')">A) Non, l'affectation privée ne donne pas droit au DIP</button><button class="opt" onclick="CASES.answer('c1s1',this,false,'Non. L’assujettissement de l’entreprise ne transforme pas une dépense privée en input déductible.')">B) Oui, car M. Rochat est assujetti</button></div><div class="step-expl" id="c1s1-expl">Le problème existe dès la déduction initiale : il ne faut pas créer artificiellement un « changement d'affectation » deux ans plus tard alors que la villa était privée dès le début.<span class="art-tag">art. 28–29 LTVA</span></div></div>
<div class="step" id="c1s2"><div class="step-q"><span class="step-qn">Q2</span> Quel réflexe de correction ?</div><div class="step-opts"><button class="opt" onclick="CASES.answer('c1s2',this,true,'Correct. Corriger le DIP indûment revendiqué dans la période pertinente et traiter intérêts/procédure selon le dossier.')">A) Corriger la déduction indue ; documenter période et intérêts</button><button class="opt" onclick="CASES.answer('c1s2',this,false,'Non. La règle 1/20 vise la valeur résiduelle lorsqu’un droit au DIP cesse après une utilisation antérieure ouvrant droit.')">B) Appliquer automatiquement 18/20 parce que la rénovation date de deux ans</button></div><div class="step-expl" id="c1s2-expl">La règle de valeur résiduelle art. 31 n'est pas un moyen de légitimer une déduction initiale qui n'avait jamais de base entrepreneuriale donnant droit au DIP.<span class="art-tag">art. 28–31 LTVA</span></div></div>
</div></div>
<!-- CAS 2 -->''','case1')

# Case 5: foreign construction supplier requires a decision tree (registration/import/acquisition), not automatic acquisition tax.
sub(r'<!-- CAS 5 -->.*?<!-- CAS 6 -->', '''<!-- CAS 5 -->
<div class="case-card"><div class="case-head"><div class="case-n">5</div><div class="case-meta"><div class="case-title">Sous-traitant étranger — importation, inscription ou impôt sur les acquisitions ?</div><div class="case-sub">Art. 45 LTVA · entreprise étrangère · douane</div></div><span class="risk risk-o">🟡 Intermédiaire</span></div><div class="case-body">
<div class="scenario">Construction SA mandate une entreprise polonaise non inscrite au registre TVA suisse pour des travaux sur un chantier genevois. Le dossier ne précise pas encore si l'entreprise étrangère apporte ses propres matériaux.</div>
<div class="step" id="c5s1"><div class="step-q"><span class="step-qn">Q1</span> Peut-on conclure immédiatement « acquisition art. 45 » ?</div><div class="step-opts"><button class="opt" onclick="CASES.answer('c5s1',this,false,'Non. Il faut d’abord qualifier le contrat, le matériel importé et l’assujettissement éventuel du fournisseur étranger.')">A) Oui, toute facture étrangère de chantier est une acquisition art. 45</button><button class="opt" onclick="CASES.answer('c5s1',this,true,'Correct. Le traitement dépend notamment du matériel importé, du statut TVA du fournisseur et de la nature de la prestation.')">B) Non, appliquer un arbre de décision</button></div><div class="step-expl" id="c5s1-expl">Si l'entreprise étrangère importe du matériel pour exécuter les travaux, l'impôt à l'importation peut porter sur la valeur totale de la prestation. Si aucun matériel n'est importé ou qu'il est fourni par le destinataire suisse, l'impôt sur les acquisitions peut être dû sous conditions. Il faut en parallèle tester l'assujettissement suisse du fournisseur étranger.<span class="art-tag">art. 45 LTVA · pratique AFC</span></div></div>
<div class="step" id="c5s2"><div class="step-q"><span class="step-qn">Q2</span> Une fois l'impôt correct identifié, le DIP est-il automatiquement intégral ?</div><div class="step-opts"><button class="opt" onclick="CASES.answer('c5s2',this,false,'Non. Le DIP dépend de l’affectation de l’immeuble.')">A) Oui, toujours</button><button class="opt" onclick="CASES.answer('c5s2',this,true,'Correct. L’affectation imposable/optionnée, exclue ou mixte détermine la déduction.')">B) Non, la déduction suit l'affectation</button></div><div class="step-expl" id="c5s2-expl">Un chantier résidentiel exclu peut conduire à un coût TVA définitif, alors qu'un chantier entièrement affecté à des prestations donnant droit au DIP peut permettre une déduction correspondante.<span class="art-tag">art. 28–30 LTVA</span></div></div>
</div></div>
<!-- CAS 6 -->''','case5')

# Common wrong formulations in cases/errors/cards/questions.
rep("Art. 45 LTVA : le maitre d'ouvrage assujetti declare l'imposition a l'acquisition (montant x 8,1%) et la deduit selon la destination de l'immeuble.","Pour une entreprise étrangère active sur un chantier suisse, tester d'abord son assujettissement, l'importation éventuelle de matériel et seulement ensuite l'impôt sur les acquisitions. La déduction suit l'affectation.",'quiz foreign blanket')
rep("Art. 45 LTVA : entrepreneur etranger non inscrit CH travaillant en Suisse => maitre d'ouvrage assujetti declare acquisition (montant x 8,1%) ET deduit selon destination immeuble.","Entreprise étrangère sur chantier CH : tester inscription suisse, matériel importé / impôt à l'importation, puis acquisition art. 45 lorsque ses conditions sont réunies. Le DIP suit l'affectation.",'card foreign blanket')
rep("Art. 31 LTVA : travaux propres sur bien à usage exclu → TVA 8,1% sur coût de revient (MO + matériaux, sans marge). L'AFC détecte via les livres de paie et les factures matériaux.","Art. 31 LTVA ne signifie pas une taxation mécanique de toute main-d'œuvre interne au coût de revient. Pour les biens fabriqués par l'assujetti, l'art. 69 OTVA prévoit notamment une correction fondée sur l'impôt préalable grevant les matériaux et travaux de tiers, avec supplément forfaitaire de 33% pour l'utilisation de l'infrastructure, sous réserve de la preuve effective.",'own work error')
rep("CHF 80'000 HT de coût de revient × 8,1% = CHF 6'480 de TVA omise + intérêts.","Recalculer l'impôt préalable effectivement concerné selon art. 31 LTVA et art. 69 OTVA ; ne pas appliquer 8,1% à toute la masse salariale interne.",'own work impact')

# Invoice formalism: evidence matters; a missing VAT number does not justify an automatic substantive denial without analysis.
rep("<strong>Facture conforme :</strong> art. 26 LTVA → n° TVA entrepreneur à vérifier pour déduire le DIP","<strong>Justificatif :</strong> art. 26 LTVA → vérifier les éléments de la facture et le statut TVA du fournisseur ; si un élément manque, obtenir une correction et conserver aussi la preuve matérielle de la prestation et de son affectation",'invoice formalism')
rep("DIP contestable tant que non corrigé","DIP à documenter ; demander une facture corrigée et conserver la preuve matérielle",'invoice workshop')

# Land value wording.
rep('Terrain / valeur du sol</td><td>À ventiler séparément ; valeur du sol hors base TVA','Terrain / valeur du sol</td><td>Part de contre-prestation afférente au sol exclue de la base de calcul (art. 24 al. 6 let. c)','land table')

# Completion UX matching M07 pattern.
if '.finish-box{' not in t:
    rep('.btn:disabled{opacity:.5;cursor:not-allowed}', '.btn:disabled{opacity:.5;cursor:not-allowed}\n.finish-box{display:none;margin-top:16px;padding:16px 18px;border-radius:8px;background:var(--sage2);border:1px solid rgba(42,107,72,.25);align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap}.finish-copy strong{display:block;color:var(--sage);font-size:14px;margin-bottom:4px}.finish-copy span{font-size:12.5px;color:#2C2C3E}.finish-actions{display:flex;gap:8px;flex-wrap:wrap}', 'finish css')
rep('''<div class="sec-nav">
<button class="btn btn-g" onclick="NAV.go('vocab')">← Vocabulaire</button>
<button class="btn btn-gold" onclick="PROG.finish()">✓ Terminer M08 Immobilier ✓</button>
</div>''','''<div class="sec-nav">
<button class="btn btn-g" onclick="NAV.go('vocab')">← Vocabulaire</button>
<button class="btn btn-gold" onclick="PROG.finish()">✓ Terminer M08</button>
</div>
<div class="finish-box" id="m08-complete"><div class="finish-copy"><strong>✅ M08 terminé</strong><span>Votre progression est enregistrée. Étape suivante : M09 — Secteurs sensibles.</span></div><div class="finish-actions"><a class="btn btn-g" href="index.html" style="text-decoration:none">← Tableau de bord</a><button class="btn btn-p" onclick="goNextModule()">Continuer avec M09 →</button></div></div>''','completion html')
rep("const pct=Math.round(n/SECS.length*100);","const pct=state.completed?100:Math.round(n/SECS.length*100);",'completed 100')
rep("finish(){state.completed=1;PROG.save();alert('Module M08 Immobilier termine !\\n\\nPassez au Module M09 - TVA Sectorielle III (SaaS, e-commerce, Transport).');}","finish(){state.completed=1;SECS.forEach(function(s){state[s]=1;});PROG.save();syncDashboardDone();const box=document.getElementById('m08-complete');if(box)box.style.display='flex';PROG.update();}",'finish handler')
if 'function syncDashboardDone()' not in t:
    rep('const CASES={', "function syncDashboardDone(){try{const k='tvaSpecialisteTvaDashboardV1';const d=JSON.parse(localStorage.getItem(k)||'{}');d.M08='done';localStorage.setItem(k,JSON.stringify(d));}catch(e){}}\nfunction goNextModule(){PROG.finish();window.location.href='m09-secteurs-sensibles-tva.html';}\n\nconst CASES={", 'dashboard sync')
if "document.getElementById('m08-complete')" not in t.split('</script>')[0][-1500:]:
    # restore completion state on reload
    rep("NAV.go('theory');\nPROG.update();", "NAV.go('theory');\nPROG.update();\nif(state.completed){const box=document.getElementById('m08-complete');if(box)box.style.display='flex';syncDashboardDone();}", 'completion init')

# Normalize explicit source date and internal/public language.
rep('Liens vérifiés au 17.05.2026.','Sources juridiques à vérifier dans leur version en vigueur ; audit du module effectué le 08.09.2026.','source date')
rep('examen examen professionnel','niveau d’un examen professionnel','exam typo')

# Final sanitisation of unsupported certainty and old internal wording.
t=t.replace('clé AFC appliquee (defavorable)','clé à reconstituer sur une base économiquement appropriée')
t=t.replace("l'AFC applique sa propre clé (défavorable)","la méthode peut être contestée et doit pouvoir être reconstituée")
t=t.replace('généralement moins favorable','appropriée aux faits')

p.write_text(t,encoding='utf-8')
print('M08 patch changes',sum(n for _,n in changes),'bytes',len(t.encode()))
for x in changes: print(' -',x)
