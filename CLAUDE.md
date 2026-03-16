# CLAUDE.md — ShoriWebsite2026

Site web de suivi de matchs de volley-ball universitaire pour l'équipe **Shori** (AMU).
Projet de L3 Informatique, semestre 6, cours BDW.

---

## Lancer le projet

```bash
python manage.py runserver
```

Base de données SQLite (`db.sqlite3`), pas de setup particulier.
Pour peupler la base : `python manage.py seed`

---

## Structure du projet

```
ShoriApp/          # Config Django (settings, urls racine, wsgi/asgi)
ShoriWebsite/      # App principale
  models.py        # Profile, Team, Match
  views.py         # home, login_view, logout_view, application_view, profil_view
  urls.py          # Routes de l'app
  admin.py
  management/commands/seed.py   # Commande pour peupler la BDD
templates/
  base.html        # Template de base (bg, patterns, cadres, navbar, instagram)
  home.html        # Page d'accueil (prochain match, timer, logos équipes)
  login.html       # Connexion par e-mail
  form.html        # Formulaire de candidature (rejoindre l'équipe)
  profil.html      # Profil utilisateur (authentifié uniquement)
static/
  css/
    style.css      # Styles globaux
    login.css      # Styles pages auth (login + form)
  images/
    Cadres/        # SVGs de décoration (BigCadre, LittleCadre, NavBar, LongCadre, LongBigCadre, Timer, Line)
    Patterns/      # SVGs/PNG de fond (Pattern1, Pattern2, BackGround)
    Teams/         # Logos des équipes (Teams=NomEquipe.png)
    Icons/         # Icônes (Profile, Instagram/Variant5)
  fonts/           # PinkBlue, YujiBoku, Rajdhani
```

---

## Modèles

- **Profile** : OneToOne avec `User` Django. Pas de champs supplémentaires pour l'instant.
- **Team** : `name`, `logo_name` (fichier sans extension, ex: `Shori` → `Teams=Shori.png`), `color` (hex).
- **Match** : `datetime`, `home_team` (FK Team), `away_team` (FK Team), `location`.

La connexion se fait par **e-mail** (pas username) — la vue cherche l'`User` par email puis authenticate par username.

---

## CSS — Conventions de dimensions

Référence Figma : **1920 × 992 px**.

| Unité | Usage |
|-------|-------|
| `vw`  | Largeurs horizontales (navbar, login-card...) |
| `vh`  | Hauteurs et **positionnement des cadres latéraux** |
| `max(Xvw, Ypx)` | Font-size (plancher px pour mobile) |
| `px`  | A éviter sauf éléments vraiment fixes |

### Cadres latéraux (LongCadre / LongBigCadre)

Les cadres qui glissent sur les côtés utilisent une largeur et des offsets **tous en `vh`** pour rester proportionnels quelle que soit la taille du viewport.

- `LongCadre.svg` : 545 × 87 px → ratio 6.264
  - Hauteur conteneur : `7.96vh` → largeur : `49.83vh` (= 7.96 × 6.264)
  - Caché : `right/left: -38.24vh` | Visible au hover : `right/left: -21.10vh`

- `LongBigCadre.svg` : 545 × 213 px → ratio 2.559
  - Hauteur conteneur : `18.75vh` → largeur : `47.98vh` (= 18.75 × 2.559)
  - Caché : `right: -36.39vh` | Visible au hover : `right: -19.25vh`

**Ne pas utiliser `vw` pour le positionnement de ces cadres** — ça les fait disparaître quand on redimensionne horizontalement.

### Couleurs

| Variable | Valeur |
|----------|--------|
| Rouge Shori (home) | `#971C22` |
| Violet (away) | `#741C97` |
| Fond | `#141313` |
| Texte secondaire | `#777` |

---

## Polices

| Famille | Fichier | Usage |
|---------|---------|-------|
| `PinkBlue` | `Pink Blue.ttf` | Police principale (titres, nav, boutons) |
| `YujiBoku` | `YujiBoku-Regular.ttf` | Décoratif |
| `Rajdhani` | 400/600/700 | Secondaire |

---

## Templates — Blocs disponibles dans base.html

```
{% block title %}
{% block description %}
{% block extra_css %}
{% block body_attrs %}    ← ajouter class="auth-bg" pour pages auth
{% block content %}
{% block extra_js %}
{% block nav_home %}      ← ajouter "active" sur le bon lien
{% block nav_equipe %}
{% block nav_calendrier %}
{% block nav_classement %}
```

---

## Points d'attention

- `db.sqlite3` est commité dans le repo (à ne pas vider sans prévenir les collègues).
- Les `__pycache__/` sont aussi commités (pas de `.gitignore` propre).
- `application_view` crée **uniquement** un `success = True` pour l'instant — la création réelle de compte n'est pas implémentée.
- `profil_view` est protégé (`redirect('login')` si non authentifié) mais il n'y a pas de `@login_required` decorator.
- Les couleurs des équipes home/away sont injectées via CSS custom properties `--home-color` et `--away-color` (voir `home.html`).
