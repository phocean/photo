# Design du site photo — décisions

Maquettes : canevas https://claude.ai/artifact/UBEFzqetzTcSiisdTrTmLa (privé).

## Décidé

| Sujet | Décision | Date |
|---|---|---|
| Orientation | Artistique : ni EXIF, ni infos techniques, ni haute résolution | 17/11/2026 |
| Direction | **A — galerie claire**, dans l'esprit du portfolio Adobe | 17/11/2026 |
| Accueil | Grille de **3 colonnes**, vignettes **4:3** (format du boîtier), titre de série dessous | 17/11/2026 |
| Typographie | Classique et élégante : **Cormorant Garamond** (logo, titres, textes) + **Inter** (navigation, mentions) | 17/11/2026 |
| Langues | **Français, anglais, japonais**, interface comprise. Adresses : `/`, `/en/…`, `/ja/…`. À l'arrivée, la langue du navigateur choisit la version (anglais si aucune des trois) ; un choix fait dans le sélecteur « FR · EN · 日本語 » est mémorisé et l'emporte ensuite | 17/11/2026 |
| Typographie japonaise | Latin en Cormorant / Inter, kanji et kana en polices du système (Hiragino, Yu Mincho, Noto) ; tailles réduites, pas d'italique | 17/11/2026 |
| Thème | **Clair et sombre** : suit le réglage du système du visiteur, bouton discret dans la navigation pour basculer (choix mémorisé) ; la visionneuse reste toujours sur fond noir | 17/11/2026 |
| Page de série | **Grille justifiée** : photos à hauteur égale par ligne, proportions respectées, clic vers la visionneuse | 17/11/2026 |

## Écarté

- Direction B (photo plein cadre + index typographique sur fond sombre).
- Accueil en 2 colonnes 3:2.
- Typographies EB Garamond seule et Inter seule.
- Page de série en colonne unique (une photo par écran).

## Repères de la direction A

- Thème clair : fond `#FAFAF8`, texte `#1A1A1A`, gris `#6B6B6B`, filets `#E4E4E0`.
- Thème sombre : fond `#121212`, texte `#EDEDEA`, gris `#9E9E9A`, filets `#2A2A2A`.
- Visionneuse : fond `#0B0B0B`.
- Largeur utile 1312 px, marges 32 px.
- Navigation : Séries · À propos · Contact, en capitales espacées.
- Visionneuse plein écran sur fond noir : flèches, fermeture, « n / total », titre éventuel.
- Pied de page : © J-C. Baptiste · Mentions légales.

## Encore ouvert

- Textes : phrases d'intention des séries, courriel de contact, hébergeur pour les mentions légales.
