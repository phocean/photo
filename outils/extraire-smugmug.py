"""Copie de référence de l'ancien site SmugMug (photo.phocean.net) via les flux RSS publics des galeries.

Usage : python3 -I extraire-smugmug.py <dossier de sortie>
Produit : flux/<id>.xml, photos/<chemin galerie>/NNN-<fichier>.jpg (plus grande taille du flux), contenu.json
"""
import html
import json
import pathlib
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

OUT = pathlib.Path(sys.argv[1])
SITE = "https://photo.phocean.net"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"}
NS = {"media": "http://search.yahoo.com/mrss/", "exif": "http://www.exif.org/specifications.html",
      "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#"}

# Arborescence relevée à la main sur le site (dossier -> galeries), dans l'ordre d'affichage
GALERIES = [
    ("Japon", "/Japon/Rue", "La rue", "368871604_THrvpF"),
    ("Japon", "/Japon/Japon-la-campagne", "La campagne", "368872848_HvDLdk"),
    ("Japon", "/Japon/Japon-le-sacr%C3%A9", "Le sacré", "369644063_9q8L7p"),
    ("France", "/France/Provence", "Provence", "370422896_4BcpHv"),
    ("France", "/France/Paris-et-sa-r%C3%A9gion", "Paris et sa région", "370420128_P8Gw3V"),
    ("France", "/France/Escapade-en-Baie-de-Somme", "Escapade en Baie de Somme - 2023", "341373461_JqH9nj"),
    ("France", "/France/Escapade-dans-lEure", "Escapade dans l'Eure - 2023", "341795534_ZD3d9f"),
    ("France", "/France/Bourgogne", "Bourgogne", "332622059_BmrqS3"),
    ("France", "/France/Marseille-la-Corniche-Hiver-2022", "Ballade sur la Corniche", "325803985_V9HGWM"),
    ("France", "/France/Le-harras", "Le harras", "370594618_wDj9W2"),
    ("France", "/France/Paris-hiver", "Paris - l'hiver", "391166118_kVNQQ6"),
    ("France", "/France/Neige", "La neige", "391166546_CXR2Lb"),
    ("France", "/France/Paris-Printemps", "Paris-Printemps", "408211126_6877Vg"),
    ("France", "/France/Noir-et-blanc", "Noir et blanc", "410445253_N59BLc"),
    ("France", "/France/Loire", "Loire", "449556799_VH5kg2"),
    ("Nature", "/Nature/Arbres", "Arbres", "370420417_Bj8qX6"),
    ("Nature", "/Nature/Oiseaux", "Oiseaux", "370594916_HXx3bL"),
    ("Nature", "/Nature/%C3%80-la-ferme", "À la ferme", "436727942_GGmBgV"),
    ("Nature", "/Nature/Monochrome", "Monochrome", "468607497_BVftmS"),
    ("Paysages", "/Paysages/Paysages", "Paysages", "373983665_tTvbdG"),
    ("Paysages", "/Paysages/Japon", "Japon", "457824620_5pvpZf"),
]


def get(url):
    url = urllib.parse.quote(url, safe=":/?&=%~-_.!*'()")  # chemins avec accents (« Le sacré »)
    for essai in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return r.read()
        except Exception as e:  # noqa: BLE001 — on réessaie puis on remonte l'erreur
            if essai == 2:
                raise
            print("  nouvel essai :", url, e, flush=True)
            time.sleep(3)


def slug(path):
    return urllib.parse.unquote(path).strip("/")


out = {"source": SITE, "galleries": []}
for dossier, path, titre, gid in GALERIES:
    feed = OUT / "flux" / f"{gid}.xml"
    if not feed.exists():
        feed.parent.mkdir(parents=True, exist_ok=True)
        feed.write_bytes(get(f"{SITE}/hack/feed.mg?Type=gallery&Data={gid}&format=rss200"))
    chan = ET.parse(feed).getroot().find("channel")
    photos = []
    for n, item in enumerate(chan.findall("item"), 1):
        contents = item.findall("media:group/media:content", NS)
        best = max(contents, key=lambda c: int(c.get("width", 0)) * int(c.get("height", 0)))
        url = best.get("url")
        nom = url.rsplit("/", 1)[-1]
        nom = re.sub(r"-(X3|X2|XL|L|M)\.jpg$", ".jpg", nom)
        fichier = f"photos/{slug(path)}/{n:03d}-{nom}"
        dest = OUT / fichier
        if not dest.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(get(url))
        t = item.findtext("media:title", "", NS) or item.findtext("title", "")
        kw = item.findtext("media:keywords", "", NS)
        photos.append({
            "file": fichier,
            "original_name": re.sub(r"-(X3|X2|XL|L|M)\.jpg$", ".jpg", nom),
            "width": int(best.get("width")), "height": int(best.get("height")),
            "taken": item.findtext("exif:DateTimeOriginal", "", NS),
            "title": "" if t == "Jean Christophe Baptiste's photo" else html.unescape(t),
            "keywords": kw,
            "lat": item.findtext("geo:lat", "", NS), "long": item.findtext("geo:long", "", NS),
            "page": item.findtext("link"),
        })
    out["galleries"].append({"folder": dossier, "path": urllib.parse.unquote(path), "title": titre,
                             "description": html.unescape(chan.findtext("description") or ""),
                             "published": chan.findtext("pubDate"), "photos": photos})
    print(f"{slug(path):40} {len(photos):3} photos", flush=True)

(OUT / "contenu.json").write_text(json.dumps(out, ensure_ascii=False, indent=2))
print("total", sum(len(g["photos"]) for g in out["galleries"]))
