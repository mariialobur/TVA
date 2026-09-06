from pathlib import Path

p=Path('m03-decomptes-methodes-tva.html')
t=p.read_text(encoding='utf-8')
changes=0

def rep(old,new):
    global t,changes
    if old not in t:
        print('WARN missing:', old[:100])
        return
    t=t.replace(old,new,1)
    changes+=1

rep("q:'Quel est le délai pour déposer la concordance annuelle (correction / concordance ePortal) ?',\n    opts:['60 jours après clôture','180 jours après clôture','240 jours après fin de l\\'exercice','360 jours'],\n    correct:2,\n    expl:'L\\'art. 72 LTVA fixe le délai à 240 jours après la fin de l\\'exercice commercial. Pour exercice 2025 (clos 31.12.2025) → délai 28.08.2026. Au-delà : les décomptes périodiques peuvent être considérés comme définitifs.'",
"q:'Quel couple de repères faut-il retenir pour la concordance annuelle ?',\n    opts:['60 jours puis 90 jours','Art. 72 : période contenant le 180e jour après la clôture; pratique AFC : repère de 240 jours pour la finalisation','240 jours = délai légal unique dans tous les cas','5 ans sans autre repère'],\n    correct:1,\n    expl:'L’art. 72 rattache la correction à la période de décompte dans laquelle tombe le 180e jour après la fin de l’exercice. En pratique, l’AFC utilise aussi le repère de 240 jours : en l’absence de rectification à ce moment, elle part du principe que les décomptes sont complets et corrects. Il faut donc retenir les deux repères et l’échéance concrète du décompte concerné.'")

rep("expl:'Le correction / concordance ePortal « Concordance annuelle » est utilisé pour les corrections des décomptes d\\'une période passée et la concordance annuelle. Dépôt via ePortal AFC dans les 240 jours après fin d\\'exercice.'",
"expl:'Le service de correction / concordance dans ePortal sert à corriger les décomptes et à finaliser la concordance annuelle. Pour le timing, appliquer l’art. 72 à la période contenant le 180e jour après la clôture et tenir compte du repère pratique AFC de 240 jours.'")

rep('<tr><td>Engagement minimum</td><td>—</td><td>1 an</td></tr>',
    '<tr><td>Durée minimale</td><td>—</td><td>Au moins une période fiscale complète, sous réserve des règles de changement applicables</td></tr>')

rep('• Les périodes et délais (60 jours paiement, 240 jours concordance)\\n• Les chiffres clés du décompte ePortal/Décompte TVA pro\\n• La concordance annuelle (correction / concordance ePortal)\\n• Les intérêts moratoires 2026 (4,0%/an)',
    '• Les périodes et délais (60 jours paiement; concordance : période contenant le 180e jour + repère pratique AFC de 240 jours)\\n• Les chiffres clés du décompte ePortal/Décompte TVA pro\\n• La concordance annuelle (correction / concordance ePortal)\\n• Le calcul des intérêts au taux DFF applicable (4,0% en 2026)')

if changes < 4:
    raise SystemExit(f'Expected 4 residual replacements, got {changes}')
p.write_text(t,encoding='utf-8')
print('Residual replacements:',changes)
