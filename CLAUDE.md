# VintedTool — notes pour Claude

## Règle : titres et descriptions doivent sonner écrits par un humain

Le générateur SEO (`generate_seo()` dans `app.py`, templates dans
`DESCRIPTION_TEMPLATES`) produit un **squelette**, pas un livrable. Il sert
de point de départ pour choper les mots-clés (`data/seo_keywords.json`) et
la fourchette de prix — jamais à copier-coller tel quel dans une annonce ou
dans `notes` / `titre` de `data/stock.json`.

Avant d'enregistrer un titre/description pour un article (photo envoyée,
demande de listing, etc.), toujours réécrire à la main :

- **Phrases variées**, pas de structure figée répétée à l'identique d'une
  annonce à l'autre ("✅ État — description courte" copié tel quel = signal
  robot pour l'acheteur et pour l'algo).
- **Spécifique à l'article réel** : détails vus sur les photos (couleur
  exacte, matière, état des semelles/coutures/finitions), pas de
  remplissage générique ("coutures parfaites", "aucun défaut visible")
  sauf si vérifié sur les photos.
- **Mots-clés SEO intégrés naturellement** dans le titre et le corps du
  texte (marque, type, matière, certifications le cas échéant — ex. "S1P
  SRC" pour du matériel de sécurité), jamais en liste de tags collée à la
  fin façon spam.
- **Ton cohérent avec la manière dont Nikolai écrit** : direct, factuel,
  pas de superlatifs creux ("magnifique", "sublime").

Le format du skill `vinted-seller` (titre / prix / description / tips
photo / astuce pro) reste la structure de réponse à suivre — c'est la
rédaction à l'intérieur de chaque section qui doit être réécrite à la main,
pas générée mot pour mot par le template Flask.

## Où ça vit

- `data/stock.json` : suivi prix (affiché / cible / minimum) + statut par
  article — pas de champ description complète, `notes` reste un résumé
  court et réel de l'état.
- `data/seo_keywords.json` : banque de mots-clés par catégorie, à piocher
  dedans, pas à recopier en bloc.
- `/generate` (`generate.html`) : outil d'aide au brouillon, le résultat
  qu'il affiche doit être retravaillé avant usage réel.
