#!/usr/bin/env python3
"""
Baixa imagens reais do Wikimedia Commons (sem IA).
Classes: objeto_a = maca (apple), objeto_b = laranja (orange).

Politica: User-Agent identificavel (https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use).
"""

from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

USER_AGENT = (
    "FIAP-FarmTechDataset/1.0 (projeto educacional FIAP; dataset local YOLO; "
    "+https://commons.wikimedia.org/) Python-urllib"
)

ALLOWED_MIME = frozenset({"image/jpeg", "image/png", "image/webp"})
MIN_EDGE = 160


def api_get(params: dict) -> dict:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=90, context=ctx) as r:
        return json.load(r)


def search_one_query_all_pages(
    query: str, seen_urls: set[str], max_new: int
) -> list[dict]:
    """Varre todas as paginas de resultado de uma busca ate esgotar ou atingir max_new novos."""
    out: list[dict] = []
    base = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": "50",
        "prop": "imageinfo",
        "iiprop": "url|mime|size|dimensions",
    }
    params = dict(base)

    while len(out) < max_new:
        data = api_get(params)
        pages = (data.get("query") or {}).get("pages") or {}
        if not pages:
            break
        for _pid, page in pages.items():
            if len(out) >= max_new:
                break
            infos = page.get("imageinfo") or []
            if not infos:
                continue
            info = infos[0]
            url = info.get("url")
            mime = info.get("mime")
            w = info.get("width") or 0
            h = info.get("height") or 0
            if not url or mime not in ALLOWED_MIME:
                continue
            if min(w, h) < MIN_EDGE:
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            out.append(
                {
                    "title": page.get("title", ""),
                    "url": url,
                    "mime": mime,
                    "width": w,
                    "height": h,
                    "size": info.get("size", 0),
                }
            )
        cont = data.get("continue")
        if not cont:
            break
        params = dict(base)
        params.update(cont)
        time.sleep(0.35)

    return out


def collect_candidates(queries: list[str], need_candidates: int) -> list[dict]:
    seen: set[str] = set()
    bucket: list[dict] = []
    for q in queries:
        if len(bucket) >= need_candidates:
            break
        extra = search_one_query_all_pages(q, seen, need_candidates - len(bucket) + 5)
        bucket.extend(extra)
    return bucket


def download_file(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=120, context=ctx) as r:
            data = r.read()
    except (urllib.error.HTTPError, urllib.error.URLError, OSError):
        return False
    if len(data) < 1500:
        return False
    dest.write_bytes(data)
    return True


def ext_for_mime(mime: str) -> str:
    return {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(
        mime, ".img"
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1] / "assets" / "dataset_yolo_farmtech"
    train_img = root / "train" / "images"
    val_img = root / "valid" / "images"
    test_img = root / "test" / "images"
    for p in (train_img, val_img, test_img):
        p.mkdir(parents=True, exist_ok=True)
    (root / "train" / "labels").mkdir(parents=True, exist_ok=True)
    (root / "valid" / "labels").mkdir(parents=True, exist_ok=True)

    # Varias buscas por classe para garantir volume no Commons
    queries_a = [
        "Malus domestica apple fruit",
        "apple fruit photo",
        "red apple fruit -logo",
    ]
    queries_b = [
        "orange fruit citrus",
        "sweet orange fruit",
        "blood orange fruit",
        "Citrus sinensis fruit",
    ]

    plan = [
        ("objeto_a", queries_a),
        ("objeto_b", queries_b),
    ]
    per_class = 40
    all_meta: list[dict] = []

    for prefix, qlist in plan:
        candidates = collect_candidates(qlist, need_candidates=250)
        saved = 0
        for m in candidates:
            if saved >= per_class:
                break
            # proximo indice (1..40); em caso de falha no download, repetimos o mesmo n
            n = saved + 1
            ext = ext_for_mime(m["mime"])
            if n <= 32:
                sub = train_img
            elif n <= 36:
                sub = val_img
            else:
                sub = test_img
            fname = f"{prefix}_{n:03d}{ext}"
            dest = sub / fname
            if download_file(m["url"], dest):
                saved += 1
                all_meta.append(
                    {
                        "file": str(dest.relative_to(root)),
                        "commons_title": m["title"],
                        "source_url": m["url"],
                    }
                )
            time.sleep(0.2)

        if saved < per_class:
            raise SystemExit(
                f"Faltam imagens para {prefix}: {saved}/{per_class}. "
                "Verifique a rede ou amplie queries_b/queries_a no script."
            )
        print(f"OK {prefix}: {saved} imagens")

    log = root / "download_log.json"
    log.write_text(json.dumps(all_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Dataset em:", root)
    print("Log de fontes:", log)
    print("Proximo passo: rotular train e valid no Make Sense; gerar .txt em labels/.")


if __name__ == "__main__":
    main()
