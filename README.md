# Site photo — photo.jcbaptiste.com

Site de photographies de J-C. Baptiste, construit avec [Hugo](https://gohugo.io) et publié par GitHub Pages.
Choix de design : [docs/design.md](docs/design.md).

## Organisation

| Dossier | Contenu |
|---|---|
| `albums/<série>/` | Les photos d'une série, **et rien d'autre** : c'est le dossier de destination d'un album d'exportation Aster |
| `content/series/<série>.md` | Titre, ordre sur l'accueil, phrase d'intention, couverture et titres de photos de la série |
| `content/a-propos.md`, `content/mentions-legales.md` | Pages de texte |
| `hugo.toml` | Réglages du site (adresse de contact, lien Instagram…) |
| `layouts/`, `assets/`, `static/` | Gabarits, style, scripts, polices |
| `outils/` | Scripts de récupération des anciens sites |
| `ancien-site/`, `ancien-site-phocean/` | Copies de référence des anciens sites, hors dépôt |

Le nom du dossier dans `albums/` et celui du fichier dans `content/series/` doivent être identiques : ils donnent aussi l'adresse de la série (`albums/arbres/` → `photo.jcbaptiste.com/arbres/`).

## Publier depuis Aster

Un album d'exportation Aster par série, avec pour dossier `albums/<série>/`. Réglages conseillés :

- JPEG, sRGB, qualité 0,92 ;
- côté long 2048 px ;
- netteté de sortie « Écran » ;
- métadonnées « Copyright seul » (le dépôt est public : les fichiers d'origine y sont visibles) ;
- renommage numéroté (`{seq}`) si l'ordre doit différer de l'ordre des noms d'origine.

Les photos s'affichent **dans l'ordre alphabétique des noms de fichier**. Le site n'affiche jamais les fichiers d'origine : il publie seulement des versions recalculées (grille et visionneuse, en WebP), sans aucune métadonnée.

## Ajouter une série

1. Créer l'album d'exportation dans Aster vers `albums/ma-serie/` et y envoyer les photos.
2. Copier un fichier existant de `content/series/` en `ma-serie.md` (et ses traductions `.en.md`, `.ja.md`) et adapter :

```yaml
---
title: "Ma série"
slug: "ma-serie"      # adresse de la série dans cette langue
weight: 70            # ordre sur l'accueil
intention: ""         # phrase facultative sous le titre
couverture: ""        # fichier de albums/ma-serie/ ; vide : la première photo
titres:               # facultatif
  "_JCB4103.jpg": "Symétries"
---
```

## Langues

Le site existe en français (à la racine), en anglais (`/en/`) et en japonais (`/ja/`).

- Chaque page se traduit par un fichier voisin : `arbres.md`, `arbres.en.md`, `arbres.ja.md`. Le champ `slug` donne l'adresse dans chaque langue (`/en/trees/`).
- Dans les fichiers de série traduits, garder le même `weight` et la même `couverture`, et traduire `title`, `intention` et `titres`.
- Les textes de l'interface (menus, boutons, visionneuse) sont dans `i18n/fr.toml`, `en.toml`, `ja.toml`.
- À l'arrivée sur le site, la langue du navigateur choisit la version (anglais si ce n'est ni le français ni le japonais). Un choix fait dans le sélecteur est mémorisé dans le navigateur et l'emporte ensuite.

## Voir le site en local

```bash
hugo server
```

Puis ouvrir http://localhost:1313. Le site se recharge à chaque modification.

## Mise en ligne

Chaque envoi sur la branche `main` de GitHub construit et publie le site (`.github/workflows/pages.yml`).
À faire une fois : dans les réglages du dépôt, *Pages* → source « GitHub Actions » et domaine `photo.jcbaptiste.com` ;
chez le registraire, un enregistrement DNS `CNAME photo` → `<compte>.github.io`.

L'ancien domaine `photo.phocean.net` (SmugMug) redirige vers ce site. La redirection est publiée par un dépôt à part,
[phocean/photo-phocean-net](https://github.com/phocean/photo-phocean-net) : GitHub Pages n'accepte qu'un domaine par dépôt.
Les anciennes galeries qui ont une série équivalente y mènent directement, toutes les autres adresses mènent à l'accueil.
