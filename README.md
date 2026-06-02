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

## Workflow complet par article

1. **Photo** → envoyer la photo à Claude pour analyse visuelle
2. **Texte** → Claude génère titre SEO + description + tags + fourchette de prix
3. **Images IA** → utiliser les prompts Gemini fournis pour générer des photos propres
4. **Stock** → ajouter l'article dans `/stock` avec les 3 prix (affiché / cible / minimum)
5. **Mise en ligne** → copier-coller titre + description sur Vinted (< 60 secondes)

## Génération de photos avec Gemini

Pour chaque article, Claude fournit 4 prompts Gemini prêts à l'emploi :

| Type | Usage |
|------|-------|
| Fond blanc | Photo principale — meilleur taux de clic |
| Détail tissu/étiquette | Rassure sur la qualité et l'authenticité |
| Lifestyle (lit/canapé) | Donne envie, contexte d'usage |
| Détail col/finitions | Répond aux questions fréquentes des acheteurs |

Les prompts sont calibrés pour un rendu **"photo maison authentique"** — pas trop studio, lumière naturelle, légèrement imparfait. C'est ce qui convertit le mieux sur Vinted.

## Données

Tout est stocké localement dans `data/` :
- `stock.json` — vos articles
- `templates.json` — modèles de messages
- `seo_keywords.json` — banque de mots-clés par catégorie (7 catégories)

## Pricing conseillé

| Stratégie | Règle |
|-----------|-------|
| Prix affiché | Prix psychologique (ex: 45 € pas 50 €) |
| Prix cible | Ce que vous voulez vraiment toucher |
| Prix minimum | Plancher en dessous duquel vous refusez |
| Pièces vintage/soie | Ne pas brader — argument premium justifie +30% |
