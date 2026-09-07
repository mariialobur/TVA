from pathlib import Path
import re

p=Path('m06-territorialite-tva-internationale.html')
t=p.read_text(encoding='utf-8')
changes=[]

def rep(old,new,label):
    global t
    n=t.count(old)
    if n:
        t=t.replace(old,new)
        changes.append((label,n))

# Residual territory / legacy / unsafe authority cleanup.
rep("Campione d'Italia", "une enclave italienne hors territoire TVA suisse", 'Campione Italia')
rep('Campione d’Italia', 'une enclave italienne hors territoire TVA suisse', 'Campione Italia typographic')
rep('Campione', 'une enclave italienne hors territoire TVA suisse', 'Campione residual')
rep('Procédure centralisée de dédouanement', 'Procédure centralisée de décompte', 'PCD full name')
rep('procédure centralisée de dédouanement', 'procédure centralisée de décompte', 'PCD full name lower')
rep('ATF 138 II 465', 'référence à vérifier dans la pratique applicable', 'false Adobe citation')
rep('ATF 140 II 202', 'art. 10 LTVA et pratique AFC', 'false threshold citation')
rep('Solidairement responsable', 'Interlocuteur de procédure ; la dette fiscale reste à l’entreprise étrangère', 'representative liability')
rep('solidairement responsable', 'interlocuteur de procédure ; la dette fiscale reste à l’entreprise étrangère', 'representative liability lower')

# Add a 20-flow professional classification matrix once.
if 'Matrice de qualification — 20 flux' not in t:
    block='''
<div class="theory-block" id="m06-flow-matrix">
<h3><span class="num">20</span>Matrice de qualification — 20 flux transfrontaliers <span class="block-risk risk-red">🔴 Dossier professionnel</span></h3>
<p class="prose">Cette matrice force le bon ordre de raisonnement : <strong>nature du flux → lieu LTVA → statut suisse → ligne du décompte → preuve → contrôle étranger éventuel</strong>. Les lignes de taux dépendent du taux réellement applicable ; on ne transforme pas « Suisse » en « 8,1% » par automatisme.</p>
<table class="comp-table"><thead><tr><th>#</th><th>Flux</th><th>Qualification suisse</th><th>Décompte / preuve</th></tr></thead><tbody>
<tr><td>1</td><td>Bien CH → client CH</td><td>Art. 7 : lieu en Suisse ; tester art. 21/23 puis art. 25.</td><td>Ch. 200 + ligne de taux applicable ; facture / livraison.</td></tr>
<tr><td>2</td><td>Bien CH → étranger</td><td>Export : art. 23 si conditions remplies.</td><td>Ch. 220 ; DTe d’exportation / transport / facture.</td></tr>
<tr><td>3</td><td>Bien étranger → CH, importation classique</td><td>Art. 50 ss : impôt sur les importations OFDF.</td><td>DTe / e-bordereau ; DIP éventuel ch. 400/405.</td></tr>
<tr><td>4</td><td>Petit envoi étranger → CH, fournisseur sous le seuil de vente par correspondance</td><td>Tester art. 7 al. 3 et la non-perception de l’impôt à l’importation ; pas de règle « TVA suisse vendeur » automatique.</td><td>Suivi du seuil et valeur des envois ; preuve transport.</td></tr>
<tr><td>5</td><td>Vente par correspondance : seuil légal atteint</td><td>Art. 7 al. 3 let. b : livraisons concernées localisées en Suisse.</td><td>Assujettissement / ch. 200 + taux ; suivi annuel du seuil.</td></tr>
<tr><td>6</td><td>Vente de biens facilitée par une plateforme</td><td>Art. 20a : fournisseur réputé uniquement si les conditions sont remplies.</td><td>Documenter rôle de la plateforme, vendeur, importateur et flux de paiement.</td></tr>
<tr><td>7</td><td>Service art. 8 al. 1, prestataire CH → destinataire CH</td><td>Lieu du destinataire en Suisse ; tester exclusion / taux.</td><td>Ch. 200 + ligne de taux si imposable ; contrat / facture.</td></tr>
<tr><td>8</td><td>Service art. 8 al. 1, prestataire CH → destinataire étranger</td><td>Lieu à l’étranger, hors territoire suisse.</td><td>Ch. 221 si à reporter ; dossier du destinataire / établissement concerné.</td></tr>
<tr><td>9</td><td>Service art. 8 al. 1, prestataire étranger non inscrit → destinataire CH</td><td>Tester impôt sur les acquisitions art. 45.</td><td>Ch. 383 + DIP éventuel 400/405 ; facture, conversion CHF, affectation.</td></tr>
<tr><td>10</td><td>Restaurant exécuté à l’étranger</td><td>Art. 8 al. 2 : lieu d’exécution à l’étranger.</td><td>Hors territoire suisse ; droit étranger à vérifier.</td></tr>
<tr><td>11</td><td>Architecture / immobilier situé à l’étranger</td><td>Art. 8 al. 2 let. f : lieu de l’immeuble.</td><td>Ch. 221 si à reporter ; adresse de l’immeuble / mandat.</td></tr>
<tr><td>12</td><td>Prestation immobilière en Suisse par entreprise étrangère</td><td>Lieu en Suisse ; tester assujettissement de l’entreprise étrangère et règles de redevable.</td><td>Art. 10/67 selon cas ; mandat, chantier, CA mondial déterminant.</td></tr>
<tr><td>13</td><td>Événement / activité culturelle ou sportive exécutée en Suisse</td><td>Tester art. 8 al. 2 puis art. 21 selon la prestation exacte.</td><td>Ch. 200 ou 230 selon qualification ; programme / billets / contrat.</td></tr>
<tr><td>14</td><td>Événement exécuté à l’étranger</td><td>Art. 8 al. 2 : lieu de l’activité à l’étranger lorsque la règle spéciale s’applique.</td><td>Ch. 221 si à reporter ; preuve du lieu et de la nature du service.</td></tr>
<tr><td>15</td><td>Transport international de personnes</td><td>Localisation selon distances parcourues + tester exonérations légales ; ne pas appliquer une règle unique.</td><td>Itinéraire, billets, ventilation, base légale du cas.</td></tr>
<tr><td>16</td><td>Prestation typiquement fournie directement à une personne physiquement présente</td><td>Tester l’exception art. 8 al. 2 avant la règle du destinataire.</td><td>Preuve du lieu d’exécution / présence et nature exacte du service.</td></tr>
<tr><td>17</td><td>Prestation exclue art. 21 en Suisse</td><td>Pas de TVA collectée si non optée ; DIP en principe limité sur coûts affectés.</td><td>Ch. 230 ; documenter exclusion, option éventuelle et affectation.</td></tr>
<tr><td>18</td><td>Opération d’intermédiaire liée à un flux international</td><td>Tester précisément l’art. 23 et ses conditions ; « client étranger » ne suffit pas.</td><td>Ch. 220 seulement si exonération établie ; mandat et flux principal.</td></tr>
<tr><td>19</td><td>Droits / certificats visés par les règles d’acquisition 2025+</td><td>Tester la catégorie spécifique de l’art. 45, le lieu et le statut des parties.</td><td>Ch. 383 si dû ; contrat, nature du droit, date et contrepartie.</td></tr>
<tr><td>20</td><td>Travaux / livraison en Suisse par entreprise étrangère sans matériel importé par elle</td><td>Tester la catégorie d’impôt sur les acquisitions et, séparément, l’assujettissement du fournisseur.</td><td>Ch. 383 si conditions remplies ; contrat, lieu, matériel, statut TVA du fournisseur.</td></tr>
</tbody></table>
<div class="box warning"><div class="box-icon">⚠️</div><div class="box-body"><div class="box-title">Règle de sortie</div><p>Une conclusion M06 n’est complète que si elle contient : <strong>article suisse + lieu + statut TVA suisse + ligne de décompte + preuve + question de droit étranger à transmettre si le lieu sort de Suisse</strong>.</p></div></div>
</div>
'''
    marker='<!-- ══════════════════ LÉGISLATION'
    if marker in t:
        t=t.replace(marker,block+marker,1)
        changes.append(('20-flow matrix',1))
    else:
        # Stable fallback before case section.
        marker='<!-- ══════════════════ CAS'
        if marker in t:
            t=t.replace(marker,block+marker,1)
            changes.append(('20-flow matrix fallback',1))
        else:
            raise SystemExit('No safe insertion point for 20-flow matrix')

p.write_text(t,encoding='utf-8')
print('M06 final cleanup changes',changes)
