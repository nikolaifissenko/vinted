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
        "Idéal pour un look {style}. Matière agréable, coupe {coupe}.\n"
        "Pas de trou, pas de tache, coutures parfaites.\n\n"
        "📦 Envoi rapide en Mondial Relay ou Colissimo.\n"
        "💬 N'hésitez pas à poser vos questions ou faire une offre raisonnable !"
    ),
    "vetements_femme": (
        "✅ {etat} — {description_courte}\n\n"
        "Pièce {style}, parfaite pour {occasion}.\n"
        "Tissu de qualité, aucun défaut visible.\n\n"
        "📦 Envoi rapide en Mondial Relay ou Colissimo.\n"
        "💬 Questions bienvenues, offres raisonnables acceptées !"
    ),
    "chaussures": (
        "✅ {etat} — {description_courte}\n\n"
        "Très peu portées, semelles en bon état.\n"
        "Aucune déformation, lacets d'origine inclus.\n\n"
        "📦 Envoi soigné avec protection.\n"
        "💬 Des questions ? Je réponds vite !"
    ),
    "electronique": (
        "✅ {etat} — {description_courte}\n\n"
        "Testé et pleinement fonctionnel. {accessoires}\n"
        "Aucune rayure majeure, écran impeccable.\n\n"
        "📦 Emballage soigné, envoi suivi obligatoire.\n"
        "💬 N'hésitez pas à me poser vos questions !"
    ),
    "livres": (
        "✅ {etat} — {description_courte}\n\n"
        "Pages propres, sans annotations ni soulignements.\n"
        "Couverture en bon état.\n\n"
        "📦 Envoi en enveloppe bulles protégée.\n"
        "💬 Lot possible si vous achetez plusieurs livres !"
    ),
    "jeux_video": (
        "✅ {etat} — {description_courte}\n\n"
        "Jeu testé et fonctionnel, {details}.\n"
        "Disque sans rayure, boîte incluse.\n\n"
        "📦 Envoi rapide et soigné.\n"
        "💬 Je vends d'autres jeux, n'hésitez pas à regarder mon profil !"
    ),
    "instruments": (
        "✅ {etat} — {description_courte}\n\n"
        "Instrument en parfait état de fonctionnement. {accessoires}\n"
        "Idéal pour {niveau}.\n\n"
        "📦 Envoi soigné, emballage renforcé pour la protection.\n"
        "💬 Questions ou négociation raisonnable bienvenues !"
    ),
}

STYLE_DEFAULTS = {
    "vetements_homme": {"style": "casual / streetwear", "coupe": "confortable"},
    "vetements_femme": {"style": "tendance", "occasion": "toutes occasions"},
    "chaussures": {},
    "electronique": {"accessoires": "Chargeur inclus."},
    "livres": {},
    "jeux_video": {"details": "notice incluse"},
    "instruments": {"accessoires": "Housse incluse.", "niveau": "débutants et intermédiaires"},
}


def generate_seo(description, categorie, marque="", taille="", etat="très bon état", couleur=""):
    keywords_data = load_json("seo_keywords.json")
    cat_data = keywords_data.get(categorie, {})
    mots_cles = cat_data.get("mots_cles", [])
    prix_min, prix_max = cat_data.get("prix_fourchette", [10, 50])

    # Build title
    parts = [p for p in [marque, description[:40], couleur, taille] if p.strip()]
    titre_base = " ".join(parts)
    etat_label = etat if etat else "très bon état"
    titre = f"{titre_base} — {etat_label}"
    if len(titre) > 80:
        titre = titre[:77] + "..."

    # Build description
    defaults = STYLE_DEFAULTS.get(categorie, {})
    template = DESCRIPTION_TEMPLATES.get(
        categorie, "✅ {etat} — {description_courte}\n\n📦 Envoi rapide.\n💬 Questions bienvenues !"
    )
    desc = template.format(
        etat=etat_label,
        description_courte=description[:80],
        **defaults,
    )

    # Tags
    selected_tags = mots_cles[:6]
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
    return render_template(
        "stock.html",
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
