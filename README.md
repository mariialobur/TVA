# TVA Academy — Parcours Spécialiste TVA Suisse

Site statique de formation consacré à la TVA suisse, structuré en **14 modules (M01–M14)** avec cas pratiques, autotests et examen blanc.

## GitHub Pages

Après activation de Pages sur la branche `main` et le dossier `/ (root)`, le site du dépôt est publié comme **project site** sous :

`https://mariialobur.github.io/TVA/`

Aucun domaine personnalisé n'est nécessaire pour cette publication.

## Structure

- `index.html` — dashboard du parcours
- `m01-...html` à `m14-...html` — modules
- `legal-qa-checklist.html` — checklist de contrôle des zones TVA volatiles
- `manifest.json` — inventaire technique des modules
- `.nojekyll` — publication directe des fichiers statiques

## Contrôle avant usage professionnel

Ce dépôt est un support pédagogique. Les taux, seuils, délais, règles de déduction, pratiques AFC, jurisprudence et autres éléments susceptibles d'évoluer doivent être vérifiés contre les sources officielles en vigueur avant utilisation dans un dossier client.

## Publication

GitHub → **Settings → Pages** → **Deploy from a branch** → `main` → `/ (root)`. Laisser **Custom domain vide** sauf si un véritable nom de domaine est configuré avec DNS.
