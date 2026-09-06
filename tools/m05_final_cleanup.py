from pathlib import Path
p=Path('m05-deduction-impot-prealable-dip.html')
t=p.read_text(encoding='utf-8')
repl={
    'ATF 132 II 353':'cadre actuel art. 28–30 et art. 81 al. 3 LTVA',
    'ATF 142 II 488':'art. 30 LTVA et art. 65–68 OTVA',
    'ATAF A-3251/2014':'art. 33 LTVA et art. 75 OTVA',
    'ATAF A-3098/2020':'art. 79 et 81 al. 3 LTVA',
}
for a,b in repl.items():
    if a in t:
        print('replace',a,t.count(a))
        t=t.replace(a,b)
# Fix a few awkward labels that can remain after the broad source replacement.
t=t.replace('Défense cadre actuel art. 28–30 et art. 81 al. 3 LTVA', 'Défense par la preuve')
t=t.replace('Lien intime entre IP et activité imposable (cadre actuel art. 28–30 et art. 81 al. 3 LTVA)', 'Affectation entrepreneuriale et preuve du DIP')
t=t.replace('art. cadre actuel art. 28–30 et art. 81 al. 3 LTVA', 'art. 28–30 et art. 81 al. 3 LTVA')
p.write_text(t,encoding='utf-8')
