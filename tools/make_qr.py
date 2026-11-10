#!/usr/bin/env python3
"""Genera el QR único de descarga para Android e iOS.

El QR apunta a app/descargar.html, que detecta el sistema del visitante y
muestra la descarga del APK o la instalación de la PWA.

Uso:
    python3 tools/make_qr.py
"""
from pathlib import Path

import segno

ROOT = Path(__file__).resolve().parent.parent
SALIDA = ROOT / "app"
URL = "https://digitalassets-ai.github.io/Quien-se-atreve-/go/"


def main() -> None:
    qr = segno.make_qr(URL, error="q")
    for nombre in ("qr-descarga.png", "qr-descarga.svg"):
        qr.save(SALIDA / nombre, scale=16, border=4, dark="#0b0710", light="#ffffff")
        print(f"Creado app/{nombre}")
    print(f"Contenido del QR: {URL}")


if __name__ == "__main__":
    main()
