"""Extrait le contenu du portfolio Adobe téléchargé : galeries, photos, légendes.

Usage : python3 -I extract.py <dossier ancien-site>
"""
import html
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(sys.argv[1])
HTML = ROOT / "html"
PHOTOS = ROOT / "photos"
UA = {"User-Agent": "Mozilla/5.0"}

def get(url, dest):
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        dest.write_bytes(r.read())

def text(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

# Page d'accueil (/work) : ordre des galeries, titres, années, vignettes
work = (HTML / "work.html").read_text()
galleries = []
for m in re.finditer(r'<a class="project-cover[^"]*" href="/([\w-]+)"(.*?)</a>', work, re.S):
    slug, inner = m.group(1), m.group(2)
    title = re.search(r'class="title[^"]*"[^>]*>(.*?)</div>', inner, re.S)
    year = re.search(r'class="date[^"]*"[^>]*>(.*?)</div>', inner, re.S)
    cover = re.search(r'data-src="(https://cdn\.myportfolio\.com/[^"]+_rwc_[^"]+)"', inner)
    galleries.append({
        "slug": slug,
        "title": text(title.group(1)) if title else slug,
        "year": text(year.group(1)) if year else "",
        "cover_url": html.unescape(cover.group(1)) if cover else None,
    })

out = {"source": "https://jc324d.myportfolio.com", "site_title": "J-C. Baptiste", "galleries": []}
for g in galleries:
    page = (HTML / f"{g['slug']}.html").read_text()
    start = page.find('id="project-modules"')
    end = page.find("You may also like", start)
    body = page[start:end if end > 0 else None]

    photos, texts = [], []
    # Modules dans l'ordre : grilles d'images et blocs de texte
    for item in re.finditer(r'class="grid__item-container[^"]*"[^>]*data-width="(\d+)" data-height="(\d+)"(.*?)grid__item-filler'
                            r'|class="project-module module text[^"]*"(.*?)</div>\s*</div>', body, re.S):
        if item.group(4) is not None:
            t = text(item.group(4))
            if t:
                texts.append(t)
            continue
        w, h, chunk = item.group(1), item.group(2), item.group(3)
        src = re.search(r'data-src="([^"]+)"', chunk)
        cap = re.search(r'grid__caption-text">(.*?)</h6>', chunk, re.S)
        if not src:
            continue
        url = html.unescape(src.group(1))
        pid = re.search(r"/([0-9a-f-]{36})_", url).group(1)
        n = len(photos) + 1
        fname = f"{n:02d}-{pid[:8]}.jpg"
        get(url, PHOTOS / g["slug"] / fname)
        photos.append({"file": f"photos/{g['slug']}/{fname}", "width": int(w), "height": int(h),
                       "caption": text(cap.group(1)) if cap else "", "id": pid})

    if g["cover_url"]:
        get(g["cover_url"], PHOTOS / g["slug"] / "_couverture.jpg")
    out["galleries"].append({**{k: g[k] for k in ("slug", "title", "year")},
                             "cover": f"photos/{g['slug']}/_couverture.jpg" if g["cover_url"] else None,
                             "texts": texts, "photos": photos})
    print(f"{g['slug']:20} {len(photos):3} photos, {sum(1 for p in photos if p['caption']):2} légendes, {len(texts)} textes")

(ROOT / "contenu.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
