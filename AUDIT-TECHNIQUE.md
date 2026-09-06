# Audit technique pré-publication — TVA Academy

Date de préparation : 2026-09-06

## Périmètre publié

- dashboard `index.html`
- 14 modules M01–M14
- `legal-qa-checklist.html`
- `manifest.json`
- `README.md`
- `.nojekyll`

Les doublons / sources de récupération et le document MASTER interne ne sont pas inclus dans le paquet public.

## Corrections appliquées

- renommage des modules avec des noms de fichiers stables et lisibles ;
- normalisation des retours `../index.html` vers `index.html` pour un déploiement GitHub Pages à la racine du dépôt ;
- suppression du lien public vers l'ancien dashboard de récupération ;
- reformulation du dashboard pour une présentation publique ;
- ajout de `rel="noopener noreferrer"` aux liens externes ouverts dans un nouvel onglet ;
- ajout de `.nojekyll` ;
- création d'un inventaire `manifest.json`.

## Tests statiques réussis

- aucun lien local cassé dans le paquet ;
- syntaxe JavaScript valide sur tous les scripts inline (`node --check`) ;
- aucun ID HTML dupliqué détecté ;
- aucune ressource locale manquante ;
- aucun lien HTTP non sécurisé détecté ;
- balise viewport présente sur toutes les pages.

## Points à contrôler après mise en ligne

1. ouverture de M01 à M14 depuis le dashboard ;
2. autotests : réponse → feedback → bouton suivant ;
3. mémo-fiches : précédent / suivant ;
4. affichage desktop et mobile, notamment les textes longs ;
5. M14 : correspondance module / compétence ;
6. console navigateur : absence d'erreurs JavaScript à l'exécution.

## Audit fiscal / juridique séparé

La validation technique ne vaut pas validation de fond TVA. Les taux, TDFN/TaF, décompte annuel, DIP, plateformes numériques, associations, immobilier, contrôle AFC, jurisprudence et toute pratique évolutive doivent être confrontés aux sources officielles AFC/LTVA/OTVA en vigueur avant diffusion professionnelle.
