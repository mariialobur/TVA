from pathlib import Path
p=Path('m08-immobilier-construction-tva.html')
t=p.read_text(encoding='utf-8')
repl={
  'Toutes documentées avec l\'impact AFC chiffré. Les connaître est aussi important que la théorie.':'Chaque erreur est reliée à son risque fiscal, à la méthode de correction et aux pièces à reconstituer. Les connaître est aussi important que la théorie.',
  '<span class="chip">🏛 Impact AFC chiffré</span>':'<span class="chip">🏛 Risque & correction</span>',
  '4 — Sous-traitant étranger non déclaré en acquisition':'4 — Prestataire étranger mal qualifié',
  'Très fréquent en construction · Art. 45 ignoré':'Très fréquent en construction · Art. 45 / importation / assujettissement',
  '8 — Transfert d\'immeuble en marche sans procédure art. 38':'8 — Transfert d\'immeuble sans analyse de l\'art. 38',
  'Très grave · TVA sur tout le transfert':'Très grave · Procédure et valeurs historiques à sécuriser',
  '<div class="fc-ctr" id="fc-ctr">Carte 1 / 25</div>':'<div class="fc-ctr" id="fc-ctr">Carte 1 / 30</div>',
}
for a,b in repl.items():
    if a in t:
        t=t.replace(a,b)
    else:
        print('WARN missing',a[:60])
p.write_text(t,encoding='utf-8')
print('M08 micro cleanup done',len(t.encode()))
