#!/usr/bin/env python3
"""Copia el APK del último release a app/descargas/quien-se-atreve.apk.

Ese archivo se versiona y se sirve desde GitHub Pages, para que la descarga
del APK no dependa de la API de GitHub en tiempo de ejecución.

Uso:
    GH_TOKEN=... python3 tools/copy_apk.py

Después de ejecutarlo, haz commit del APK actualizado.
"""
import json
import os
import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DESTINO = ROOT / "app" / "descargas" / "quien-se-atreve.apk"
REPO = "digitalassets-AI/Quien-se-atreve-"


def main() -> None:
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "quien-se-atreve",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    peticion = urllib.request.Request(
        f"https://api.github.com/repos/{REPO}/releases/latest", headers=headers
    )
    with urllib.request.urlopen(peticion, timeout=30) as respuesta:
        release = json.load(respuesta)

    assets = [a for a in release.get("assets", []) if a["name"].endswith(".apk")]
    if not assets:
        sys.exit("El último release no tiene ningún APK.")

    asset = assets[0]
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(asset["browser_download_url"], timeout=120) as origen:
        with DESTINO.open("wb") as destino:
            shutil.copyfileobj(origen, destino)

    print(f"APK actualizado: {DESTINO.relative_to(ROOT)} ({DESTINO.stat().st_size} bytes)")
    print(f"Release: {release.get('tag_name')} · {asset['name']}")


if __name__ == "__main__":
    main()
