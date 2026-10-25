#!/usr/bin/env python3
"""Genera los iconos PWA a partir de assets/logo.webp.

Requiere Pillow y NumPy. Los iconos se versionan en app/icons/, así que este
script solo hace falta si cambia el logo.

Uso:
    python3 tools/make_icons.py
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
LOGO = ROOT / "assets" / "logo.webp"
ICONS = ROOT / "app" / "icons"

TOP = (26, 0, 51)       # #1a0033
BOTTOM = (102, 0, 102)  # #660066


def gradiente(size: int) -> Image.Image:
    """Fondo diagonal oscuro con un resplandor cálido detrás del logo."""
    y, x = np.mgrid[0:size, 0:size].astype(np.float32)
    t = np.clip((x + y) / (2 * (size - 1)), 0, 1)
    rgb = np.zeros((size, size, 3), dtype=np.float32)
    for canal in range(3):
        rgb[..., canal] = TOP[canal] + (BOTTOM[canal] - TOP[canal]) * t

    cx = cy = (size - 1) / 2
    dist = np.sqrt((x - cx) ** 2 + (y - cy) ** 2) / (size * 0.55)
    glow = np.clip(1 - dist, 0, 1)[..., None] ** 2
    rgb = rgb + glow * np.array([120, 45, 0], dtype=np.float32)

    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8), "RGB")


def icono(size: int, cobertura: float, fondo: bool = True) -> Image.Image:
    lienzo = gradiente(size) if fondo else Image.new("RGBA", (size, size), (0, 0, 0, 0))
    logo = Image.open(LOGO).convert("RGBA")

    ancho = int(size * cobertura)
    alto = round(logo.height * ancho / logo.width)
    logo = logo.resize((ancho, alto), Image.Resampling.LANCZOS)

    # Sombra suave para separar el logo del fondo.
    sombra = Image.new("RGBA", lienzo.size, (0, 0, 0, 0))
    mascara = logo.split()[-1].point(lambda a: int(a * 0.55))
    sombra.paste((0, 0, 0, 255), ((size - ancho) // 2, (size - alto) // 2 + 6), mascara)
    sombra = sombra.filter(ImageFilter.GaussianBlur(max(2, size // 40)))
    lienzo = Image.alpha_composite(lienzo.convert("RGBA"), sombra)

    lienzo.alpha_composite(logo, ((size - ancho) // 2, (size - alto) // 2))
    return lienzo


def main() -> None:
    ICONS.mkdir(parents=True, exist_ok=True)
    salidas = {
        "icon-192.png": (192, 0.88),
        "icon-512.png": (512, 0.88),
        "icon-maskable-512.png": (512, 0.70),
        "apple-touch-icon.png": (180, 0.86),
        "favicon-32.png": (32, 0.96),
    }
    for nombre, (size, cobertura) in salidas.items():
        icono(size, cobertura).save(ICONS / nombre, optimize=True)
        print(f"  {nombre}: {size}x{size}")

    # favicon.ico multi-resolución para navegadores antiguos.
    ico = icono(64, 0.92)
    ico.save(ICONS / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("  favicon.ico: 16/32/48/64")


if __name__ == "__main__":
    main()
