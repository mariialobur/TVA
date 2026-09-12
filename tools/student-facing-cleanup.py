from pathlib import Path

FILES = {
    'm09-secteurs-sensibles-tva.html': [
        ('Legal QA · version 09.09.2026', 'Droit vérifié au 09.09.2026'),
        ('Théorie & truth map', 'Théorie & méthode'),
        ('Audit juridique : 09.09.2026', 'Droit vérifié : 09.09.2026'),
        ('M09 · Legal QA 09.09.2026', 'M09 · Repères juridiques au 09.09.2026'),
        ('La « truth map » M09 — ordre obligatoire', 'Méthode M09 — ordre de qualification'),
        ('Cheatsheet & validation', 'Synthèse & validation'),
        ('Cheatsheet', 'Synthèse'),
        ('← Tableau de bord', '← Accueil du parcours'),
    ],
    'm12-jurisprudence-lab-tva.html': [
        ('Red-team source QA · 09.09.2026', 'Sources vérifiées au 09.09.2026'),
        ('M12 · Legal QA 09.09.2026', 'M12 · Sources vérifiées au 09.09.2026'),
        ('Bank · 12', 'Jurisprudence · 12'),
        ('>Bank<', '>Jurisprudence<'),
        ('<h3>Truth map</h3>', '<h3>Méthode de recherche</h3>'),
        ('<b>Temporal gate</b>', '<b>Vérifier le droit applicable à la période</b>'),
        ('<b>Negative research</b>', '<b>Rechercher aussi les sources contraires</b>'),
        ('<h3>Temporal gate</h3>', '<h3>Droit applicable à la période</h3>'),
        ('<h3>Negative research</h3>', '<h3>Recherche contradictoire</h3>'),
        ('current-law check/comparabilité', 'droit actuel / comparabilité'),
        ('12 anchor cases vérifiés', '12 décisions de référence vérifiées'),
        ('7 current/procedural + 5 historical bridges. L’ancien bank de 18 références approximatives est supprimé.', '7 références actuelles ou procédurales + 5 passerelles historiques, sélectionnées pour leur utilité pratique.'),
        ('le vrai anchor internet du bank est notamment', 'une référence pertinente pour les prestations sur internet est notamment'),
        ('Cheatsheet', 'Synthèse'),
        ('← Tableau de bord', '← Accueil du parcours'),
    ],
    'm13-communication-fiscale-cabinet.html': [
        ('Red-team practice QA · 09.09.2026', 'Pratique vérifiée au 09.09.2026'),
        ('QA 09.09.2026', 'Droit vérifié · 09.09.2026'),
        ('M13 · Practice & legal QA', 'M13 · Pratique professionnelle'),
        ('Truth map — 7 questions avant «Envoyer»', '7 questions avant d’envoyer'),
        ('Templates cabinet', 'Modèles cabinet'),
        ('>Templates<', '>Modèles<'),
        ('Facts first', 'Faits d’abord'),
        ('Pas de tolling', 'Pas d’interruption de prescription'),
        ('next owner', 'responsable de la prochaine action'),
        ('Cheatsheet', 'Synthèse'),
        ('← Tableau de bord', '← Accueil du parcours'),
    ],
    'm14-examen-blanc-synthese-finale.html': [
        ('Final Legal QA · 11.09.2026', 'Droit vérifié au 11.09.2026'),
        ('Best Final Pro', 'Meilleur score final'),
        ('<span>Capstones</span>', '<span>Dossiers</span>'),
        ('Cadre & current-law', 'Cadre & droit en vigueur'),
        ('Capstones · 4', 'Dossiers de synthèse · 4'),
        ('<option value="capstones">Capstones</option>', '<option value="capstones">Dossiers</option>'),
        ('Snapshot droit: 11.09.2026', 'Droit vérifié : 11.09.2026'),
        ('M14 · Final assessment', 'M14 · Évaluation finale'),
        ('4 capstones', '4 dossiers de synthèse'),
        ('Current-law snapshot · 11.09.2026', 'Repères juridiques au 11.09.2026'),
        ('Blueprint réel', 'Structure des examens'),
        ('Exam engine', 'Modes d’examen'),
        ('Open dossiers', 'Dossiers de synthèse'),
        ('4 capstones à rédiger', '4 dossiers de synthèse à rédiger'),
        ('Debrief', 'Analyse du résultat'),
        ('module floor', 'seuil minimal par module'),
        ('Course gate', 'Conditions de validation'),
        ('Deux portes: Final Pro + 4 dossiers ouverts.', 'Deux conditions : examen final + 4 dossiers de synthèse.'),
        ('Gate 1 · Final Pro', 'Condition 1 · Examen final'),
        ('Gate 2 · Capstones', 'Condition 2 · Dossiers de synthèse'),
        ('Complétez les deux gates ci-dessus.', 'Remplissez les deux conditions ci-dessus.'),
        ('✓ Valider M14 sur le dashboard', '✓ Valider le parcours'),
        ('← Tableau de bord', '← Accueil du parcours'),
    ],
}

for name, pairs in FILES.items():
    path = Path(name)
    text = path.read_text(encoding='utf-8')
    if 'favicon.svg' not in text:
        text = text.replace('</title>', '</title>\n<link rel="icon" href="favicon.svg" type="image/svg+xml">', 1)
    changed = 0
    for old, new in pairs:
        n = text.count(old)
        if n:
            text = text.replace(old, new)
            changed += n
    path.write_text(text, encoding='utf-8')
    print(f'{name}: {changed} visible copy replacement(s)')
