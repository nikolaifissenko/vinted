# VintedTool ⚓

Tableau de bord complet pour vendeurs Vinted — SEO, stock, messages, revenus.

## Lancement (2 commandes)

```bash
pip install flask
python app.py
```

Puis ouvrez http://localhost:5000

## Fonctionnalités

| Page | URL | Description |
|------|-----|-------------|
| Dashboard | `/` | Revenus, stats, graphique, objectif semaine |
| Générateur SEO | `/generate` | Titre + description + tags optimisés |
| Stock | `/stock` | CRUD articles avec prix affiché/cible/minimum |
| Messages | `/messages` | Templates réponses acheteurs, copiables en 1 clic |

## Données

Tout est stocké localement dans `data/`:
- `stock.json` — vos articles
- `templates.json` — modèles de messages
- `seo_keywords.json` — banque de mots-clés par catégorie
