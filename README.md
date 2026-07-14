# Vintage Style Lovers — Garage Collection

Sito vetrina per il tuo store TeePublic, con catalogo che si aggiorna **da solo ogni giorno**.

## Come funziona l'aggiornamento automatico

TeePublic non offre un'API pubblica per collegare store esterni, quindi non esiste un modo
"ufficiale" per sincronizzare i due siti in tempo reale. La soluzione qui dentro fa questo:

1. Ogni giorno (alle 6:00 UTC) un robot gratuito di GitHub legge la pagina pubblica del tuo
   store (`scrape_teepublic.py`), esattamente come farebbe un visitatore col browser.
2. Se trova design nuovi, riscrive `products.json`.
3. Il sito (`index.html`) legge `products.json` e mostra sempre la lista aggiornata.
4. GitHub pubblica automaticamente la nuova versione del sito.

Tu non devi fare nulla: pubblichi la maglietta su TeePublic e, entro 24 ore, compare da sola
sul tuo sito. Se vuoi forzare l'aggiornamento subito dopo aver pubblicato un nuovo design,
puoi lanciarlo a mano (spiegato sotto, punto 4).

> Nota: essendo uno script "fai da te" e non un'API ufficiale, se TeePublic cambia il layout
> della pagina in futuro lo script potrebbe smettere di trovare i prodotti. In quel caso il
> file `products.json` NON viene sovrascritto (resta quello valido precedente) e basta
> aggiornare qualche riga in `scrape_teepublic.py`. Se ti capita, torna pure da me e ti aiuto
> a sistemarlo.

---

## Passo 1 — Crea un account GitHub (gratis)

Vai su [github.com](https://github.com) e crea un account, se non ce l'hai già.

## Passo 2 — Crea un nuovo repository

1. Clicca su **New repository**.
2. Nome consigliato: `vintage-style-lovers-shop`.
3. Lascialo **Public**.
4. Non aggiungere README/gitignore (li hai già qui).
5. Clicca **Create repository**.

## Passo 3 — Carica questi file

Il modo più semplice, senza usare la riga di comando:

1. Nella pagina del repository appena creato, clicca **uploading an existing file** (o
   trascina i file nella pagina).
2. Trascina **tutti** i file e le cartelle che trovi qui (`index.html`, `products.json`,
   `scrape_teepublic.py`, `README.md` e la cartella `.github`).
3. Attenzione: la cartella `.github` deve rimanere con questo nome esatto e la sua struttura
   interna (`.github/workflows/update-products.yml`) — è quella che dice a GitHub di eseguire
   l'aggiornamento automatico.
4. Clicca **Commit changes**.

## Passo 4 — Attiva GitHub Pages (pubblica il sito)

1. Nel repository, vai su **Settings → Pages**.
2. Alla voce **Source**, scegli **GitHub Actions**.
3. Vai sulla tab **Actions** del repository e apri il workflow **"Aggiorna catalogo da
   TeePublic"**. Clicca **Run workflow** per lanciarlo la prima volta a mano.
4. Dopo un paio di minuti, il sito sarà online su un indirizzo tipo:
   `https://TUO-USERNAME.github.io/vintage-style-lovers-shop/`

Da questo momento in poi il robot gira da solo ogni giorno. Puoi comunque rilanciarlo a mano
in qualsiasi momento dalla tab **Actions → Run workflow**, ad esempio subito dopo aver
caricato un nuovo design su TeePublic.

---

## Come collegare un dominio tuo (es. vintagestylelovers.com)

### 1. Compra il dominio

Puoi comprarlo su un registrar qualsiasi. I più comuni ed economici:

- **Namecheap** (namecheap.com) — buon rapporto qualità/prezzo, whois privacy incluso.
- **Cloudflare Registrar** (cloudflare.com) — prezzo alla pari col costo reale, nessun ricarico.
- **Google Domains → ora Squarespace Domains**.
- **IONOS / Aruba** — se preferisci un registrar italiano con supporto in italiano.

Costo indicativo: **8–15€/anno** per un `.com`, spesso meno per `.shop`, `.store`, `.style`
(adatti a un negozio di magliette).

Cerca il nome che vuoi (es. `vintagestylelovers.com`) e completa l'acquisto.

### 2. Collega il dominio a GitHub Pages

Nel pannello DNS del tuo registrar (si trova di solito nella sezione "DNS" o
"Gestione DNS" del dominio appena comprato):

**Se usi il dominio nudo (`vintagestylelovers.com`):**
Aggiungi questi 4 record di tipo **A**, tutti con host `@`:
```
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

**Se preferisci usare un sottodominio (`shop.vintagestylelovers.com`):**
Aggiungi un record **CNAME**:
```
Host: shop
Valore: TUO-USERNAME.github.io
```

Poi torna su GitHub: **Settings → Pages → Custom domain**, scrivi il tuo dominio
(es. `vintagestylelovers.com` o `shop.vintagestylelovers.com`) e salva. Spunta anche
**Enforce HTTPS** (potrebbe richiedere qualche ora per attivarsi da sola).

I DNS possono impiegare da pochi minuti a 24-48 ore per propagarsi ovunque nel mondo:
è normale, basta aspettare.

---

## Personalizzare il sito

- **Colori/testi**: apri `index.html`, tutto il testo visibile è in chiaro nell'HTML.
- **Immagine di copertina/loghi**: al momento il sito non usa immagini proprie, solo le
  foto dei design prese da TeePublic — se vuoi aggiungere un tuo logo, dimmelo e te lo integro.
- **Frequenza di aggiornamento**: nel file `.github/workflows/update-products.yml`, la riga
  `cron: "0 6 * * *"` decide l'orario. Se vuoi che giri più spesso (es. ogni 6 ore), cambiala in
  `cron: "0 */6 * * *"`.
