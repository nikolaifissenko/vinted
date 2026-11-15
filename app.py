import json
import os
import uuid
from datetime import datetime, date
from flask import Flask, render_template, request, jsonify, redirect, url_for

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def load_json(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── Vinted fee ──────────────────────────────────────────────────────────────
# Payé par l'acheteur en plus du prix affiché (vendeur particulier : 0 €).
# Taux dans data/fees.json — modifier ce fichier si Vinted change le barème.

def load_fees():
    path = os.path.join(DATA_DIR, "fees.json")
    if not os.path.exists(path):
        return {"fixe": 0.70, "pourcentage": 0.05}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def vinted_fee(prix, fees=None):
    fees = fees or load_fees()
    prix = float(prix or 0)
    if prix <= 0:
        return 0.0
    return round(fees["fixe"] + prix * fees["pourcentage"], 2)


def prix_acheteur(prix, fees=None):
    return round(float(prix or 0) + vinted_fee(prix, fees), 2)


@app.context_processor
def inject_fees():
    return {"vinted_fee": vinted_fee, "prix_acheteur": prix_acheteur, "fees": load_fees()}


# ─── SEO Generator ───────────────────────────────────────────────────────────

CATEGORY_LABELS = {
    "vetements_homme": "Vêtements Homme",
    "vetements_femme": "Vêtements Femme",
    "chaussures": "Chaussures",
    "electronique": "Électronique",
    "livres": "Livres",
    "jeux_video": "Jeux Vidéo",
    "instruments": "Instruments",
}

DESCRIPTION_TEMPLATES = {
    "vetements_homme": (
        "✅ {etat} — {description_courte}\n\n"
        "{misure}"
        "Idéal pour un look {style}. Matière agréable, coupe {coupe}.\n"
        "Pas de trou, pas de tache, coutures impeccables.\n\n"
        "📦 Envoi rapide et soigné.\n"
        "🔁 -10 % dès 2 articles achetés dans mon dressing.\n"
        "💬 N'hésitez pas pour vos questions ou une offre raisonnable !"
    ),
    "vetements_femme": (
        "✅ {etat} — {description_courte}\n\n"
        "{misure}"
        "Pièce {style}, parfaite pour {occasion}.\n"
        "Tissu de qualité, aucun défaut visible.\n\n"
        "📦 Envoi rapide et soigné.\n"
        "🔁 -10 % dès 2 articles achetés dans mon dressing.\n"
        "💬 Questions bienvenues, offres raisonnables acceptées !"
    ),
    "chaussures": (
        "✅ {etat} — {description_courte}\n\n"
        "{misure}"
        "Très peu portées, semelles en bon état.\n"
        "Aucune déformation, lacets d'origine inclus.\n\n"
        "📦 Envoi soigné en carton protégé.\n"
        "💬 Une question ? Je réponds vite !"
    ),
    "electronique": (
        "✅ {etat} — {description_courte}\n\n"
        "Testé et parfaitement fonctionnel. {accessoires}\n"
        "Aucune rayure importante, écran impeccable.\n\n"
        "📦 Emballage protégé, envoi suivi.\n"
        "💬 N'hésitez pas à me poser vos questions !"
    ),
    "livres": (
        "✅ {etat} — {description_courte}\n\n"
        "Pages propres, sans annotations ni soulignements.\n"
        "Couverture en bon état.\n\n"
        "📦 Envoi en enveloppe à bulles.\n"
        "💬 Prix dégressif si vous prenez plusieurs livres !"
    ),
    "jeux_video": (
        "✅ {etat} — {description_courte}\n\n"
        "Jeu testé et fonctionnel, {details}.\n"
        "Disque sans rayure, boîtier inclus.\n\n"
        "📦 Envoi rapide et soigné.\n"
        "💬 Je vends d'autres jeux, jetez un œil à mon dressing !"
    ),
    "instruments": (
        "✅ {etat} — {description_courte}\n\n"
        "Instrument en parfait état de marche. {accessoires}\n"
        "Idéal pour {niveau}.\n\n"
        "📦 Envoi soigné, emballage renforcé.\n"
        "💬 Questions ou négociation raisonnable bienvenues !"
    ),
}

STYLE_DEFAULTS = {
    "vetements_homme": {"style": "casual / streetwear", "coupe": "confortable"},
    "vetements_femme": {"style": "tendance", "occasion": "toutes les occasions"},
    "chaussures": {},
    "electronique": {"accessoires": "Chargeur inclus."},
    "livres": {},
    "jeux_video": {"details": "notice incluse"},
    "instruments": {"accessoires": "Housse incluse.", "niveau": "débutants et intermédiaires"},
}


# Mensurations standard par taille (corps, cm) — indicatives, pas mesurées sur le vêtement
SIZE_CHARTS = {
    "vetements_femme": {
        "XS": ("FR 34", "poitrine 80-84 · taille 62-66 · hanches 88-92"),
        "S": ("FR 36", "poitrine 84-88 · taille 66-70 · hanches 92-96"),
        "M": ("FR 38", "poitrine 88-92 · taille 70-74 · hanches 96-100"),
        "L": ("FR 40", "poitrine 94-98 · taille 76-80 · hanches 102-106"),
        "XL": ("FR 42", "poitrine 100-104 · taille 82-86 · hanches 108-112"),
        "XXL": ("FR 44", "poitrine 106-110 · taille 88-92 · hanches 114-118"),
    },
    "vetements_homme": {
        "XS": ("FR 42", "poitrine 80-86 · taille 68-74"),
        "S": ("FR 44", "poitrine 88-94 · taille 76-82"),
        "M": ("FR 46-48", "poitrine 96-102 · taille 84-90"),
        "L": ("FR 50", "poitrine 104-110 · taille 92-98"),
        "XL": ("FR 52", "poitrine 112-118 · taille 100-106"),
        "XXL": ("FR 54", "poitrine 120-126 · taille 108-114"),
    },
}


def misure_standard(categorie, taille):
    taille = (taille or "").strip().upper()
    if categorie == "chaussures":
        try:
            n = float(taille.replace(",", "."))
        except ValueError:
            return ""
        return f"📐 Pointure {taille} EU = pied d'environ {n / 1.5 - 1.5:.1f} cm (indicatif)\n"
    chart = SIZE_CHARTS.get(categorie, {})
    if taille not in chart:
        return ""
    fr, misure = chart[taille]
    return f"📏 Taille {taille} ({fr}) — mensurations standard : {misure} cm\n"


def generate_seo(description, categorie, marque="", taille="", etat="très bon état", couleur=""):
    keywords_data = load_json("seo_keywords.json")
    cat_data = keywords_data.get(categorie, {})
    mots_cles = cat_data.get("mots_cles", [])
    prix_min, prix_max = cat_data.get("prix_fourchette", [10, 50])

    # Build title
    parts = [p for p in [marque, description[:40], couleur, taille] if p.strip()]
    titre_base = " ".join(parts)
    etat_label = etat if etat else "très bon état"
    titre = f"{titre_base} {etat_label}"
    if len(titre) > 80:
        titre = titre[:77] + "..."

    # Build description
    defaults = STYLE_DEFAULTS.get(categorie, {})
    template = DESCRIPTION_TEMPLATES.get(
        categorie, "✅ {etat} — {description_courte}\n\n📦 Envoi rapide.\n💬 Questions bienvenues !"
    )
    desc = template.format(
        etat=etat_label.capitalize(),
        misure=misure_standard(categorie, taille),
        description_courte=description[:80],
        **defaults,
    )

    # Tags — seulement les mots-clés qui décrivent vraiment l'article (+ le genre)
    texte = f"{description} {couleur}".lower()
    selected_tags = [m for m in mots_cles if m.lower() in texte or m in ("homme", "femme")]
    if couleur:
        selected_tags.append(couleur.lower())
    if marque:
        selected_tags.insert(0, marque.lower())
    if taille:
        selected_tags.append(f"taille {taille}")
    tags = list(dict.fromkeys(selected_tags))[:10]

    return {
        "titre": titre,
        "description": desc,
        "tags": tags,
        "prix_fourchette": f"{prix_min} – {prix_max} €",
        "prix_fourchette_acheteur": f"{prix_acheteur(prix_min):.2f} – {prix_acheteur(prix_max):.2f} €",
    }


@app.route("/generate", methods=["GET", "POST"])
def generate():
    result = None
    form = {}
    if request.method == "POST":
        form = request.form.to_dict()
        result = generate_seo(
            description=form.get("description", ""),
            categorie=form.get("categorie", "vetements_homme"),
            marque=form.get("marque", ""),
            taille=form.get("taille", ""),
            etat=form.get("etat", "très bon état"),
            couleur=form.get("couleur", ""),
        )
    return render_template("generate.html", result=result, form=form, categories=CATEGORY_LABELS)


# ─── Stock Tracker ───────────────────────────────────────────────────────────

@app.route("/stock")
def stock():
    items = load_json("stock.json")
    total = len(items)
    en_ligne = sum(1 for i in items if i["statut"] == "En ligne")
    vendus = [i for i in items if i["statut"] == "Vendu"]
    revenus = sum(float(i.get("prix_affiche", 0)) for i in vendus)
    potentiel = sum(float(i.get("prix_affiche", 0)) for i in items if i["statut"] == "En ligne")
    fees = load_fees()
    frais_vendus = sum(vinted_fee(i.get("prix_affiche", 0), fees) for i in vendus)
    return render_template(
        "stock.html",
        frais_vendus=frais_vendus,
        items=items,
        total=total,
        en_ligne=en_ligne,
        nb_vendus=len(vendus),
        revenus=revenus,
        potentiel=potentiel,
        categories=CATEGORY_LABELS,
    )


@app.route("/stock/add", methods=["POST"])
def stock_add():
    items = load_json("stock.json")
    item = {
        "id": str(uuid.uuid4())[:8],
        "titre": request.form.get("titre", ""),
        "categorie": request.form.get("categorie", ""),
        "prix_affiche": float(request.form.get("prix_affiche") or 0),
        "prix_cible": float(request.form.get("prix_cible") or 0),
        "prix_minimum": float(request.form.get("prix_minimum") or 0),
        "statut": request.form.get("statut", "Brouillon"),
        "date_mise_en_ligne": request.form.get("date_mise_en_ligne") or str(date.today()),
        "notes": request.form.get("notes", ""),
    }
    items.append(item)
    save_json("stock.json", items)
    return redirect(url_for("stock"))


@app.route("/stock/update/<item_id>", methods=["POST"])
def stock_update(item_id):
    items = load_json("stock.json")
    for item in items:
        if item["id"] == item_id:
            item["titre"] = request.form.get("titre", item["titre"])
            item["categorie"] = request.form.get("categorie", item["categorie"])
            item["prix_affiche"] = float(request.form.get("prix_affiche") or item["prix_affiche"])
            item["prix_cible"] = float(request.form.get("prix_cible") or item["prix_cible"])
            item["prix_minimum"] = float(request.form.get("prix_minimum") or item["prix_minimum"])
            item["statut"] = request.form.get("statut", item["statut"])
            item["notes"] = request.form.get("notes", item["notes"])
            break
    save_json("stock.json", items)
    return redirect(url_for("stock"))


@app.route("/stock/delete/<item_id>", methods=["POST"])
def stock_delete(item_id):
    items = load_json("stock.json")
    items = [i for i in items if i["id"] != item_id]
    save_json("stock.json", items)
    return redirect(url_for("stock"))


# ─── Message Templates ────────────────────────────────────────────────────────

@app.route("/messages")
def messages():
    templates = load_json("templates.json")
    return render_template("messages.html", templates=templates)


@app.route("/messages/save", methods=["POST"])
def messages_save():
    data = request.get_json()
    templates = load_json("templates.json")
    for t in templates:
        if t["id"] == data.get("id"):
            t["texte"] = data.get("texte", t["texte"])
            break
    save_json("templates.json", templates)
    return jsonify({"ok": True})


# ─── Dashboard ───────────────────────────────────────────────────────────────

@app.route("/dashboard")
def dashboard():
    items = load_json("stock.json")
    vendus = [i for i in items if i["statut"] == "Vendu"]
    en_ligne = [i for i in items if i["statut"] == "En ligne"]

    total_revenus = sum(float(i.get("prix_affiche", 0)) for i in vendus)
    potentiel = sum(float(i.get("prix_affiche", 0)) for i in en_ligne)
    fees = load_fees()
    frais_vendus = sum(vinted_fee(i.get("prix_affiche", 0), fees) for i in vendus)

    today = date.today()
    week_start = today.toordinal() - today.weekday()
    month_start = today.replace(day=1)

    def in_week(item):
        d = item.get("date_mise_en_ligne", "")
        try:
            return date.fromisoformat(d).toordinal() >= week_start
        except Exception:
            return False

    def in_month(item):
        d = item.get("date_mise_en_ligne", "")
        try:
            return date.fromisoformat(d) >= month_start
        except Exception:
            return False

    revenus_semaine = sum(float(i.get("prix_affiche", 0)) for i in vendus if in_week(i))
    revenus_mois = sum(float(i.get("prix_affiche", 0)) for i in vendus if in_month(i))

    # Sales by date for chart
    sales_by_date = {}
    for i in vendus:
        d = i.get("date_mise_en_ligne", "?")
        sales_by_date[d] = sales_by_date.get(d, 0) + float(i.get("prix_affiche", 0))
    chart_labels = sorted(sales_by_date.keys())
    chart_data = [sales_by_date[k] for k in chart_labels]

    objectif = float(request.args.get("objectif", 200))
    progress = min(100, round(total_revenus / objectif * 100)) if objectif else 0

    return render_template(
        "dashboard.html",
        total_revenus=total_revenus,
        frais_vendus=frais_vendus,
        revenus_semaine=revenus_semaine,
        revenus_mois=revenus_mois,
        potentiel=potentiel,
        nb_vendus=len(vendus),
        nb_en_ligne=len(en_ligne),
        recent_sales=sorted(vendus, key=lambda x: x.get("date_mise_en_ligne", ""), reverse=True)[:10],
        chart_labels=json.dumps(chart_labels),
        chart_data=json.dumps(chart_data),
        objectif=objectif,
        progress=progress,
    )


# ─── Index redirect ───────────────────────────────────────────────────────────

@app.route("/")
def index():
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
