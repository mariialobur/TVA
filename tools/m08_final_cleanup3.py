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
        print('WARN',label)

def sub(pattern,repl,label):
    global t
    t2,n=re.subn(pattern,repl,t,flags=re.S)
    if n:
        t=t2; changes.append((label,n))
    else:
        print('WARN regex',label)

# Remove remaining unsupported/misleading jurisprudence shortcuts.
rep('ATF 145 II 130','art. 42 LTVA · prescription','remove 145 misuse')
rep('140 II 88','art. 30 LTVA','remove bare 140 reference')
rep('⚖️ ATF + ATAF','⚖️ Jurisprudence vérifiée','legis chip')

# Replace the obsolete legislation jurisprudence block with a source-hierarchy block.
sub(r'''<div class="block">\s*<div class="block-h"><span class="bnum">3</span><h3>Jurisprudence — TF &amp; TAF Immobilier</h3></div>.*?<div class="sec-nav">\s*<button class="btn btn-g" onclick="NAV.go\('theory'\)">← Théorie</button>''', '''<div class="block">
<div class="block-h"><span class="bnum">3</span><h3>Jurisprudence — méthode de vérification</h3></div>
<div class="box info"><div class="box-icon">⚖️</div><div class="box-body"><div class="box-title">Ne pas mémoriser un numéro d’arrêt sans son considérant</div>Dans M08, une jurisprudence n’est citée que si le texte de l’arrêt a été vérifié et soutient précisément la règle enseignée. Pour un dossier réel : partir de la LTVA et de l’OTVA, vérifier la pratique AFC en vigueur, puis rechercher au besoin la jurisprudence TF/TAF pertinente.</div></div>
<div class="leg-card"><div class="leg-icon li-gold">⚖️</div><div><div class="leg-ref">Tribunal fédéral / Tribunal administratif fédéral</div><div class="leg-title">Recherche ciblée par question juridique</div><div class="leg-desc">Rechercher par article et par problème concret : option art. 22, double affectation art. 30, correction art. 31–32, procédure de déclaration art. 38, impôt sur les acquisitions art. 45. Lire les considérants avant de reprendre une règle.</div><div class="leg-links"><a class="leg-link" href="https://www.bger.ch/fr/home.html" rel="noopener noreferrer" target="_blank">🔍 Tribunal fédéral</a><a class="leg-link" href="https://www.bvger.ch/fr/jurisprudence" rel="noopener noreferrer" target="_blank">🔍 Tribunal administratif fédéral</a></div></div></div>
<div class="box info"><div class="box-icon">📌</div><div class="box-body"><div class="box-title">Registre foncier comme pièce du dossier</div>Le registre foncier cantonal peut servir à vérifier propriétaire, droits réels, servitudes, droit de superficie et caractéristiques du bien. Il s’agit d’une source factuelle du dossier, pas d’une présomption de contrôle automatique de l’AFC.</div></div>
</div>
<div class="sec-nav">
<button class="btn btn-g" onclick="NAV.go('theory')">← Théorie</button>''','replace legislation jurisprudence')

# Correct lingering French typo in case-section intro.
rep("correspondent au niveau de l'niveau d’un examen professionnel","correspondent au niveau d’un examen professionnel",'exam intro typo')

# Error section: direct allocation first; foreign contractor decision tree; no invented monitoring/sanctions.
rep('''✅ Art. 30 LTVA + art. 30 LTVA · pratique AFC : clé objective à vérifier. DIP déductible = DIP × (surface commerciale / surface totale). Documenter dans un tableau annexe au décompte.''','''✅ Art. 30 LTVA : affecter d’abord directement les charges identifiables. Pour les coûts réellement communs, appliquer une clé objective et économiquement appropriée (surface, recettes ou autre critère pertinent) et documenter la méthode.''','error1 allocation')
rep("<strong>Impact AFC :</strong> Sur CHF 300'000 HT de travaux, DIP indu si clé réelle = 35% → CHF 24'300 × 65% = CHF 15'795 de rappel + intérêts moratoires selon taux DFF applicable. Sur 5 ans = CHF 18'000+ de rappel.","<strong>Impact :</strong> Une déduction trop élevée doit être recalculée selon l’affectation correcte, avec intérêts selon le taux DFF applicable. Le montant et la période doivent être reconstitués à partir des factures et des règles de prescription applicables.",'error1 fixed amount')
rep('''✅ Art. 45 LTVA : lieu = Suisse → acquisition à vérifier. CHF 180'000 × 8,1% = CHF 14'580 à déclarer et déduire (si chantier commercial). Impact net = 0 mais obligation procédurale.''','''✅ Avant de conclure à l’art. 45, vérifier la nature du contrat, l’assujettissement suisse du fournisseur étranger et l’importation éventuelle de matériel. Selon la configuration, le dossier peut relever de l’impôt à l’importation, de l’impôt sur les acquisitions ou de l’inscription TVA du fournisseur. Le DIP suit ensuite l’affectation.''','error4 foreign rule')
rep("<strong>Impact AFC :</strong> L'AFC croise les virements à l'étranger. CHF 14'580 de rappel + intérêts moratoires selon taux DFF applicable. Récupérable comme DIP mais pénalité procédurale reste.","<strong>Impact :</strong> Une mauvaise qualification peut produire un impôt non déclaré, une déduction erronée ou une obligation d’immatriculation omise. Reconstituer le traitement avant de chiffrer rappel, intérêts ou éventuelle sanction.",'error4 monitoring')
rep('''✅ art. 30 LTVA · pratique AFC : clé stable, objective (surface ou recettes), documentée (plan + tableau) et appliquée systématiquement. Changer de méthode = justifier à l'AFC.''','''✅ Art. 30 LTVA : la méthode doit représenter l’utilisation des inputs. Une modification de clé est possible si les faits ou la pertinence économique changent, mais elle doit être documentée et reproductible.''','error7 key')
rep("<strong>Impact AFC :</strong> L'AFC peut imposer rétroactivement sa propre clé (appropriée aux faits) sur 5 ans si la méthode est jugée arbitraire.","<strong>Impact :</strong> Une méthode non défendable peut être corrigée pour les périodes concernées selon les règles de procédure et de prescription applicables. D’où l’importance d’un dossier permettant de reproduire chaque calcul.",'error7 fixed years')
rep('''✅ Art. 38 LTVA + art. 38 LTVA · Info TVA 11 : procédure de déclaration à appliquer si les conditions sont remplies. Notification formelle AFC. Le cessionnaire reprend tous droits et obligations TVA (DIP déduit, corrections potentielles).''','''✅ Art. 38 LTVA : tester si la procédure de déclaration est obligatoire ou facultative, documenter les valeurs transférées et utiliser le formulaire 764 selon la pratique AFC en vigueur. L’acquéreur reprend notamment la base de calcul et le coefficient de déduction pour les valeurs transférées selon l’art. 38 al. 4.''','error8 art38')
rep("<strong>Impact AFC :</strong> TVA sur la valeur totale du transfert. Sur immeuble commercial CHF 2'500'000 : TVA CHF 202'500 + intérêts. L'erreur la plus coûteuse en restructuration immobilière.","<strong>Impact :</strong> Une mauvaise application de l’art. 38 peut fausser la taxation du transfert et les valeurs historiques reprises. Les conséquences doivent être déterminées selon le traitement réellement appliqué, pas par une pénalité chiffrée automatique.",'error8 impact')

# Evaluation UI must match the actual arrays.
rep('SECTION E — QUIZ 30 QUESTIONS','SECTION E — QUIZ 35 QUESTIONS','quiz comment')
rep('30 questions · Format examen professionnel · Timer 25 min','35 questions · Format examen professionnel · Timer 25 min','quiz hero count')
rep('Seuil de validation : 75% (23/30). Auto-submit à 0:00.','Seuil de validation : 75% (27/35). Auto-submit à 0:00.','quiz threshold')
rep('Question 1 / 30','Question 1 / 35','quiz initial count')
rep('25 flashcards Immo/Construction — 4 catégories · SM-2','30 flashcards Immo/Construction — 5 catégories · SM-2','flash hero count')
rep('<span class="chip">🃏 25 cartes</span><span class="chip">📚 4 catégories</span>','<span class="chip">🃏 30 cartes</span><span class="chip">📚 5 catégories</span>','flash chips')

# Generic language cleanup around keys and option.
rep('clé objective (surface ou recettes)','clé objective adaptée aux faits','generic key wording')
rep('La méthode doit être stable d\'une année à l\'autre et documentée.','La méthode doit être cohérente, reproductible et documentée ; tout changement doit être justifié par les faits.','stability wording')

p.write_text(t,encoding='utf-8')
print('M08 cleanup3 changes',sum(n for _,n in changes),'bytes',len(t.encode()))
for c in changes: print(' -',c)
