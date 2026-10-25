#!/usr/bin/env python3
"""Genera los recursos Android (iconos y splash) a partir del logo.

Los archivos se escriben en ``android-assets/`` y el workflow los copia dentro
del proyecto Android generado por Capacitor. Requiere Pillow y NumPy.

Uso:
    python3 tools/make_android_assets.py
"""
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFilter

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
OUT = ROOT / "android-assets"

sys.path.insert(0, str(BASE))
from make_icons import LOGO, gradiente, icono  # noqa: E402

MIPMAPS = {
    "mdpi": 48,
    "hdpi": 72,
    "xhdpi": 96,
    "xxhdpi": 144,
    "xxxhdpi": 192,
}
FOREGROUNDS = {
    "mdpi": 108,
    "hdpi": 162,
    "xhdpi": 216,
    "xxhdpi": 324,
    "xxxhdpi": 432,
}
SPLASHES = {
    "drawable/splash.png": (480, 320),
    "drawable-land-mdpi/splash.png": (480, 320),
    "drawable-land-hdpi/splash.png": (800, 480),
    "drawable-land-xhdpi/splash.png": (1280, 720),
    "drawable-land-xxhdpi/splash.png": (1600, 960),
    "drawable-land-xxxhdpi/splash.png": (1920, 1280),
    "drawable-port-mdpi/splash.png": (320, 480),
    "drawable-port-hdpi/splash.png": (480, 800),
    "drawable-port-xhdpi/splash.png": (720, 1280),
    "drawable-port-xxhdpi/splash.png": (960, 1600),
    "drawable-port-xxxhdpi/splash.png": (1280, 1920),
}


def fondo(w: int, h: int) -> Image.Image:
    """Recorta el degradado cuadrado al tamaño exacto de la pantalla."""
    size = max(w, h)
    base = gradiente(size)
    left = (size - w) // 2
    top = (size - h) // 2
    return base.crop((left, top, left + w, top + h)).convert("RGBA")


def splash(w: int, h: int) -> Image.Image:
    """Fondo degradado con el logo centrado para la pantalla de inicio."""
    lienzo = fondo(w, h)
    logo = Image.open(LOGO).convert("RGBA")
    ancho = int(min(w, h) * 0.34)
    alto = round(logo.height * ancho / logo.width)
    logo = logo.resize((ancho, alto), Image.Resampling.LANCZOS)

    x = (w - ancho) // 2
    y = (h - alto) // 2

    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    mascara = logo.split()[-1].point(lambda a: int(a * 0.6))
    sombra.paste((0, 0, 0, 255), (x, y + max(4, h // 220)), mascara)
    sombra = sombra.filter(ImageFilter.GaussianBlur(max(3, w // 100)))
    lienzo = Image.alpha_composite(lienzo, sombra)
    lienzo.alpha_composite(logo, (x, y))
    return lienzo


def redondo(size: int) -> Image.Image:
    """Icono legacy con recorte circular y transparencia en las esquinas."""
    icon = icono(size, 0.88).convert("RGBA")
    mascara = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mascara).ellipse((0, 0, size - 1, size - 1), fill=255)
    icon.putalpha(mascara)
    return icon


def escribir_xml() -> None:
    adaptive = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background"/>
    <foreground android:drawable="@mipmap/ic_launcher_foreground"/>
</adaptive-icon>
"""
    for nombre in ("ic_launcher.xml", "ic_launcher_round.xml"):
        ruta = OUT / "mipmap-anydpi-v26" / nombre
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(adaptive, encoding="utf-8")

    fondo_xml = """<?xml version="1.0" encoding="utf-8"?>
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <gradient
        android:angle="45"
        android:endColor="#660066"
        android:startColor="#1A0033"
        android:type="linear" />
</shape>
"""
    ruta = OUT / "drawable" / "ic_launcher_background.xml"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(fondo_xml, encoding="utf-8")

    color_xml = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="ic_launcher_background">#1A0033</color>
</resources>
"""
    ruta = OUT / "values" / "ic_launcher_background.xml"
    ruta.parent.mkdir(parents=True, exist_ok=True)
    ruta.write_text(color_xml, encoding="utf-8")


def main() -> None:
    if not LOGO.exists():
        raise SystemExit(f"Falta el logo: {LOGO}")

    OUT.mkdir(parents=True, exist_ok=True)

    for densidad, size in MIPMAPS.items():
        carpeta = OUT / f"mipmap-{densidad}"
        carpeta.mkdir(parents=True, exist_ok=True)
        icono(size, 0.88).save(carpeta / "ic_launcher.png", optimize=True)
        redondo(size).save(carpeta / "ic_launcher_round.png", optimize=True)

    for densidad, size in FOREGROUNDS.items():
        carpeta = OUT / f"mipmap-{densidad}"
        carpeta.mkdir(parents=True, exist_ok=True)
        icono(size, 0.62, fondo=False).save(
            carpeta / "ic_launcher_foreground.png", optimize=True
        )

    for ruta, (w, h) in SPLASHES.items():
        destino = OUT / ruta
        destino.parent.mkdir(parents=True, exist_ok=True)
        splash(w, h).convert("RGB").save(destino, optimize=True)

    escribir_xml()
    print(f"Recursos Android generados en {OUT.relative_to(ROOT)}")
    print(f"  · {len(MIPMAPS)} densidades de icono")
    print(f"  · {len(FOREGROUNDS)} densidades de icono adaptativo")
    print(f"  · {len(SPLASHES)} pantallas de inicio")
    print("  · icono adaptativo con degradado y fondo de respaldo")


if __name__ == "__main__":
    main()
