# VintedTool — sessione ottobre 2026

## 1. Nuove condizioni Vinted (ottobre 2026)

| | Italia / UE | UK · US · AU |
|---|---|---|
| Entrata in vigore | **5 ottobre 2026** | 8 ottobre 2026 |

- **Vinted Pay** sostituisce Mangopay: accettare i nuovi termini nell'app e completare la verifica d'identità (KYC). IBAN intestato a te, nome identico al profilo Vinted. I venditori Pro sono esclusi.
- **"Buyer Protection fee" → "Vinted fee"**: stessa tariffa (IT: **0,70 € + 5 %**), la paga l'acquirente. Il venditore privato incassa il prezzo pieno.
- **Contraffazione**: 48 h (prima 24 h) per dimostrare l'autenticità. Un articolo che non supera la verifica non si può rimettere in vendita; dopo 6 settimane Vinted può distruggerlo.
- **Sanzioni**: anche una sola violazione può portare al blocco (temporaneo o definitivo), a giudizio di Vinted ("proporzionale"). Un solo ricorso, entro 6 mesi.
- **Eliminare e ripubblicare** un annuncio per farlo risalire è ora una violazione → usare **Modifica**, ribasso ≥10 % (notifica chi ha messo "preferito") o Boost.
- Mai citare marche diverse da quella vera nei tag (es. "Ralph Lauren" su U.S. Polo Assn.) → rischio segnalazione per contraffazione.

Fonti: [Value Added Resource (UE)](https://www.valueaddedresource.net/vinted-europe-terms-october-2026/) · [Value Added Resource (UK/US/AU)](https://www.valueaddedresource.net/vinted-us-uk-australia-terms-october-2026/) · [Sad Vinted Faces](https://sadvintedfaces.com/vinted-new-terms) · [Vendy Studio](https://www.vendystudio.com/blog/vinted-new-terms-and-conditions-2026) · [Vinted – autenticità](https://www.vinted.com/help/307-item-authenticity-policy)

## 2. Modifiche al tool

| Modifica | Dove |
|---|---|
| Calcolo **Vinted fee** e **totale acquirente** (prezzo + fee) | `/stock`, `/dashboard`, `/generate` |
| Tariffa configurabile in un solo file | `data/fees.json` (`fixe`, `pourcentage`) |
| Generatore in **italiano** (testi, condizioni, parole chiave) | `app.py`, `data/seo_keywords.json`, `templates/generate.html` |
| Tag solo se descrivono davvero l'articolo | `generate_seo()` |
| **Misure standard** automatiche dalla taglia (donna/uomo XS–XXL, scarpe EU → cm piede) | `SIZE_CHARTS`, `misure_standard()` |
| Titoli dello stock tradotti in italiano | `data/stock.json` |

Branch: `claude/tender-franklin-rnhPz`

## 3. Annunci pronti

### U.S. Polo Assn. — maglione scollo V grigio XL (bozza)
**Prezzo:** 15 € (acquirente 16,45 €) · obiettivo 12 € · minimo 10 €

**Titolo**
```
U.S. Polo Assn. maglione scollo V grigio XL uomo ottime condizioni
```
**Descrizione**
```
U.S. POLO ASSN. | Maglione scollo a V | Taglia XL

✅ Condizioni: ottime — nessun pelucco, nessuna macchia
📏 Taglia XL (IT 54) — misure standard del corpo: petto 112-118 · vita 100-106 cm
🎨 Colore: grigio melange, profilo nero sul collo
🧵 Composizione: 100% acrilico — morbido, non pizzica, lavabile in lavatrice

✨ Classico maglione con logo ricamato sul petto. Perfetto sopra una camicia
per l'ufficio o con jeans e sneakers nel tempo libero. Capo base per l'autunno/inverno.

⚠️ Difetti: nessuno visibile

📦 Spedizione rapida, imballaggio curato
🔁 -10% acquistando 2 o più articoli dal mio profilo
💬 Scrivimi per qualsiasi domanda o proposta ragionevole!
```
**Hashtag:** `#uspoloassn #maglione #scolloV #maglioneuomo #grigio #XL #casual #preppy #autunno`

### Cappotto donna rosso bordeaux svasato — taglia L (bozza)
**Prezzo:** 25 € (acquirente 26,95 €) · obiettivo 20 € · minimo 16 € · se invenduto a metà novembre → 22 €

**Titolo**
```
Cappotto donna rosso bordeaux svasato colletto tg. L ottime condizioni
```
**Descrizione**
```
Cappotto donna | Rosso bordeaux | Taglia L

✅ Condizioni: ottime — nessuna macchia, nessun buco
📏 Taglia L (IT 46) — misure standard del corpo: busto 94-98 · vita 76-80 · fianchi 102-106 cm
🎨 Colore: rosso bordeaux, interno grigio melange
🧵 Tessuto: spesso e morbido, interno felpato caldo

✨ Cappotto svasato con colletto classico, chiusura a bottoni automatici
metallici, due tasche a filetto e maniche con risvolto e bottone decorativo.
Caldo ma leggero, perfetto per l'autunno e l'inverno. Elegante sopra un vestito,
casual con jeans e sneakers.

⚠️ Difetti: nessuno visibile

📦 Spedizione rapida, imballaggio curato
🔁 -10% acquistando 2 o più articoli dal mio profilo
💬 Scrivimi per misure o foto aggiuntive!
```
**Hashtag:** `#cappotto #cappottodonna #rosso #bordeaux #svasato #colletto #autunno #inverno #elegante #casual`

## 4. Da fare

- [ ] Accettare i termini Vinted Pay + verifica identità, prima del prossimo prelievo
- [ ] Annunci online (Nike AF1, iPhone 12, abito Zara): **Modifica** → incollare titolo e descrizione in italiano (non eliminare/ripubblicare)
- [ ] Levi's 501 "T38": verificare se è taglia EU o vita W
- [ ] Maglione: rifare foto su fondo bianco + retro + etichetta composizione → poi "En ligne"
- [ ] Cappotto: foto etichetta composizione (scrivere "lana" solo se c'è sull'etichetta) + foto retro; foto principale = cappotto chiuso sul muro bianco; taglia Vinted "L / IT 46"
- [ ] Conservare scontrini / prove di autenticità per ogni articolo di marca (48 h in caso di segnalazione)
