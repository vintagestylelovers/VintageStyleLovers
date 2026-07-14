#!/usr/bin/env python3
"""
scrape_teepublic.py
--------------------
Legge la pagina pubblica del negozio TeePublic e rigenera products.json
con l'elenco aggiornato delle magliette (nuove incluse).

Questo script NON usa nessuna API privata: legge solo la pagina pubblica
del negozio, esattamente come farebbe un visitatore col browser.
Se TeePublic cambia il proprio HTML in futuro, questo script potrebbe
aver bisogno di un piccolo aggiustamento.

Uso:
    python3 scrape_teepublic.py

Viene eseguito automaticamente ogni giorno da GitHub Actions
(vedi .github/workflows/update-products.yml), ma puoi anche lanciarlo
a mano in qualsiasi momento.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

STORE_URL = "https://www.teepublic.com/user/https-www-tiktok-com-vintagestylelovers"
OUTPUT_FILE = Path(__file__).parent / "products.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}


def fetch_html(url: str) -> str:
    req = Request(url, headers=HEADERS)
    with urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_products(html: str):
    """Estrae i design dalla pagina del negozio TeePublic.

    TeePublic renderizza ogni design come un blocco che contiene:
    - un link al prodotto (/t-shirt/<id>-<slug>?store_id=...)
    - un'immagine del design
    - il "Main Tag" (modello auto / categoria)
    - una descrizione
    - un elenco di tag
    - un prezzo
    """
    products = []

    # Ogni prodotto ha un blocco <a ...t-shirt/ID-SLUG...><img ... alt="TITLE T-Shirt" src="IMG">
    card_pattern = re.compile(
        r'<img[^>]+alt="([^"]+?) T-Shirt"[^>]+src="([^"]+)"[^>]*>.*?'
        r'href="(https://www\.teepublic\.com/t-shirt/\d+-[a-z0-9\-]+\?store_id=\d+)"',
        re.DOTALL,
    )

    tag_pattern = re.compile(r'Main Tag:.*?>([^<]+) T-Shirt<', re.DOTALL)
    desc_pattern = re.compile(r'Description:\s*([^<\n]+)')
    tags_pattern = re.compile(r'Tags:\s*([^<\n]+)')
    price_pattern = re.compile(r'\$(\d+)(?:\s*\$\d+)?')

    # Approccio più robusto: dividiamo la pagina in blocchi per prodotto
    blocks = html.split("Back to Design")
    for block in blocks:
        img_match = re.search(r'alt="([^"]+?) T-Shirt"[^>]+src="([^"]+)"', block)
        if not img_match:
            img_match = re.search(r'src="([^"]+)"[^>]+alt="([^"]+?) T-Shirt"', block)
            if img_match:
                img, title = img_match.group(1), img_match.group(2)
            else:
                continue
        else:
            title, img = img_match.group(1), img_match.group(2)

        url_match = re.search(
            r'(https://www\.teepublic\.com/t-shirt/\d+-[a-z0-9\-]+\?store_id=\d+)', block
        )
        tag_match = tag_pattern.search(block)
        desc_match = desc_pattern.search(block)
        tags_match = tags_pattern.search(block)
        price_match = price_pattern.search(block)

        if not url_match:
            continue

        products.append({
            "title": title.strip(),
            "tag": (tag_match.group(1).strip().upper() if tag_match else ""),
            "description": (desc_match.group(1).strip() if desc_match else ""),
            "tags": (
                [t.strip() for t in tags_match.group(1).split(",")]
                if tags_match else []
            ),
            "image": img.strip(),
            "url": url_match.group(1).strip(),
            "price": (price_match.group(1) if price_match else ""),
        })

    return products


def main():
    print(f"Scarico la pagina dello store: {STORE_URL}")
    print(f"Lunghezza totale HTML scaricato: {len(html)} caratteri")
    try:
        html = fetch_html(STORE_URL)
    except Exception as exc:
        print(f"Errore nello scaricare la pagina: {exc}", file=sys.stderr)
        sys.exit(1)

    products = parse_products(html)

    if not products:
        print(
            "Nessun prodotto trovato: probabile cambiamento nella struttura "
            "della pagina TeePublic. Il file products.json NON viene sovrascritto "
            "per sicurezza.",
            file=sys.stderr,
        )
        sys.exit(1)

    data = {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "store_url": STORE_URL,
        "products": products,
    }

    OUTPUT_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Trovati {len(products)} design. products.json aggiornato.")


if __name__ == "__main__":
    main()
