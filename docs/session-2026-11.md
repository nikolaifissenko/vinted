# VintedTool — session novembre 2026 (15/11)

## 1. Décision : retour au français

- Le compte est sur **vinted.fr**, et la plupart des acheteurs sont **français**, même si Nikolai habite en Italie.
- Le passage à l'italien d'octobre (commits `f85b07a`, `5e4d2fb`) a été annulé (commit `8cd121f`) :
  - le générateur SEO est en français : modèles de texte, états Vinted, mots-clés, tableau des tailles en FR ;
  - les 8 titres du stock sont en français.
- On a gardé les améliorations d'octobre : la ligne de mesures, la remise de -10 % dès 2 articles et les tags limités aux mots qui décrivent l'article.
- **Règle** : on ne met jamais dans le titre ou les tags une marque qui n'est pas sur l'étiquette. Pas de « Ralph Lauren » pour un Chaps, ni pour un U.S. Polo.
- **À vérifier** : les options d'envoi du compte, pour être sûr que des transporteurs italiens sont proposés. Un compte .fr avec une adresse italienne, c'est inhabituel.

## 2. Prompt Gemini (amélioration des photos)

On l'utilise une photo à la fois. Il faut adapter la phrase sur la couleur à chaque pull.

```
Edit this exact photo. Keep the original image as it is: same sweater, same hanger, same door/table, same position, framing and angle. Do not regenerate, redraw, replace or remove anything.

Only improve:
- image quality: sharper, more detail in the knit, less blur, noise and compression artefacts
- lighting: brighter and more even, softer shadows, remove the yellow/orange cast so the [COULEUR] looks like its true colour

Keep colours natural, no filters, no added effects. Do not change the sweater, logo, label, collar stripes or any marks on the fabric. Same proportions, higher resolution.
```

Compare toujours le résultat avec l'original, en particulier le logo, le texte de l'étiquette et les défauts. Si l'un d'eux a changé, garde la photo d'origine.

## 3. Annonces prêtes (pas encore dans stock.json)

Toutes les descriptions se terminent par le même paragraphe :

> Si vous voulez les mesures, demandez-moi, je vous les envoie tout de suite. J'accepte les offres, et si vous prenez plusieurs articles de mon dressing on s'arrange sur le prix.

Les prix sont indiqués sous la forme affiché / cible / minimum.

### American Eagle — col montant boutonné gris, L — 18 / 15 / 13 €
**Titre :** Pull American Eagle homme L gris col montant boutonné

Pull American Eagle pour homme, taille L, coupe classique. Gris anthracite chiné, col montant avec 4 boutons qu'on peut porter fermé quand il fait froid ou ouvert pour un look plus décontracté.

Je l'ai peu porté, il est en très bon état. Il y a juste un peu de bouloche sur le bord du col, on la voit sur la 3e photo. Il est chaud sans être lourd, je le mettais sur une chemise ou un t-shirt.

- [ ] Photo de l'étiquette de composition

### Nautica — col rond bleu marine, L, 100 % coton — 20 / 17 / 14 €
**Titre :** Pull Nautica homme bleu marine taille L col rond logo brodé 100% coton

Pull Nautica pour homme, taille L, bleu marine. 100% coton, donc doux et pas du tout qui gratte.

Col rond avec un liseré à petites rayures bleu ciel et blanches, et l'intérieur du col en gris, ce qui lui donne un petit plus. Petit logo Nautica brodé sur la poitrine. C'est le genre de pull qui va avec tout, en jean ou en chino, sur une chemise ou tout seul.

Il est en bon état. On voit quelques petites peluches claires sur les photos, c'est juste de la poussière de tissu, je lui passe un coup de brosse avant l'envoi.

- [ ] Étiquette blanche au col : s'il est neuf, le mettre en « Neuf avec étiquette » ; sinon, l'enlever avant les photos
- [ ] Rouleau anti-peluches avant de refaire les photos

### Calvin Klein — col rond maille fine, L — 20 / 17 / 14 €
**Titre :** Pull Calvin Klein homme L bleu marine col rond maille fine logo CK brodé

Pull Calvin Klein pour homme, taille L. Maille fine, col rond, avec le petit logo CK brodé ton sur ton sur la poitrine. Discret et classe, il se porte aussi bien avec un jean qu'avec un pantalon plus habillé, ou sur une chemise pour le bureau.

Il est en bon état, sans trou ni tache. Il y a quelques petites peluches claires qu'on voit sur les photos, je lui passe un coup de brosse avant l'envoi.

- [ ] Couleur : vérifier s'il est noir ou bleu marine à la lumière du jour
- [ ] Repasser ou passer à la vapeur, puis refaire les photos
- [ ] Composition : s'il y a de la laine ou du cachemire, l'ajouter au titre et afficher 25 € ou plus

### Chaps — col rond rouge bordeaux, XL — 16 / 14 / 11 €
**Titre :** Pull Chaps homme XL rouge bordeaux col rond maille coton

Pull Chaps pour homme, taille XL. Rouge bordeaux, col rond avec l'intérieur du col à petites rayures rouges et blanches, et le petit logo brodé ton sur ton sur la poitrine.

Grosse maille bien épaisse, il tient chaud sans gratter. Une couleur sympa pour l'hiver et les fêtes, avec un jean brut ou un chino beige.

Il est en bon état, pas de trou ni de tache. La couleur est un peu plus passée dans le dos, comme souvent sur le coton lavé, on le voit sur la photo.

- [ ] Garder « coton » seulement si l'étiquette le confirme
- [ ] Étiquette blanche sur la manche : neuf ou à enlever ?
- [ ] Supprimer la photo en double

### Levi's — col rond beige chiné, L — 18 / 15 / 12 €
**Titre :** Pull Levi's homme L beige chiné col rond maille fine

Pull Levi's pour homme, taille L. Beige chiné, col rond, maille fine et légère.

Une couleur neutre qui va avec absolument tout : jean brut, chino, sur une chemise blanche ou un t-shirt. Parfait pour la mi-saison comme pour l'hiver sous une veste.

Il est en bon état, pas de trou.

- [ ] Zones plus foncées sur le devant : taches ou ombre ? Laver le pull ; si elles restent, les signaler avec une photo en gros plan
- [ ] Ajouter une photo de face sur cintre et la mettre en première
- [ ] Vérifier que c'est bien un modèle homme

### Nautica NavTech — col V rouge bordeaux, S — 18 / 15 / 12 €
**Titre :** Pull Nautica NavTech homme S rouge bordeaux col V logo brodé

Pull Nautica de la ligne NavTech, pour homme, taille S. Rouge bordeaux chiné, col V, avec le logo voilier brodé en bleu marine sur la poitrine. Maille fine et souple, agréable à porter.

Le col V se porte très bien sur une chemise ou un t-shirt blanc, avec un jean ou un chino. Il est en très bon état, sans trou ni tache.

- [ ] Composition (étiquette intérieure)
- [ ] Repasser ou passer à la vapeur, puis refaire les photos

## 4. À faire

- [ ] Publier les 6 pulls **le même jour** pour favoriser les achats groupés. On est en plein dans la saison des pulls : il faut qu'ils soient en ligne avant début décembre.
- [ ] Les ajouter en brouillon dans `stock.json` (pas encore fait)
- [ ] Annonces en ligne (Nike AF1, iPhone 12, robe Zara) : **Modifier** pour coller le titre français du stock, et baisser le prix de 10 à 15 %. Elles sont en ligne depuis mai-juin, et l'iPhone est la priorité.
- [ ] Brouillons d'octobre (U.S. Polo, manteau, Redmond) : refaire les photos et les publier
- [ ] Accepter les conditions Vinted Pay et faire la vérification d'identité (reste du mois d'octobre)
- [ ] Repartir de la checklist d'octobre (`sessione-2026-10.md` §4). Le point sur le Levi's 501 est sans objet : il est vendu.
