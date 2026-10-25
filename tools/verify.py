#!/usr/bin/env python3
"""Verifica la integridad de la base de datos y de los archivos PWA.

Uso:
    python3 tools/verify.py
"""
import json
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "database" / "quien_se_atreve.sqlite"
APP = ROOT / "app"

EXPECTED = {
    "preguntas": 2000,
    "nodos_extra": 2400,
    "glosario": 72,
}
HOT_POR_JUEGO = {"amigos": 600, "pareja": 800, "universidad": 600}
EXTRA_POR_NODO = {
    ("amigos", "panas"): 400,
    ("amigos", "mejores_amigos"): 400,
    ("pareja", "conocerse"): 400,
    ("pareja", "conocerse_fondo"): 400,
    ("universidad", "companeros"): 400,
    ("universidad", "amigos_u"): 400,
}

errores = []


def check(condicion: bool, mensaje: str) -> None:
    if not condicion:
        errores.append(mensaje)
        print(f"  ✗ {mensaje}")


def verificar_bd() -> None:
    print("Base de datos")
    check(DB.exists(), f"Falta {DB.relative_to(ROOT)}")
    if not DB.exists():
        return

    con = sqlite3.connect(DB)
    cur = con.cursor()

    for tabla, esperado in EXPECTED.items():
        total = cur.execute(f"SELECT COUNT(*) FROM {tabla}").fetchone()[0]
        check(total == esperado, f"{tabla}: {total} filas (esperadas {esperado})")
        print(f"  · {tabla}: {total}")

    for juego, esperado in HOT_POR_JUEGO.items():
        total = cur.execute(
            "SELECT COUNT(*) FROM preguntas WHERE juego=?", (juego,)
        ).fetchone()[0]
        check(total == esperado, f"preguntas/{juego}: {total} (esperadas {esperado})")

    for (categoria, subcategoria), esperado in EXTRA_POR_NODO.items():
        total = cur.execute(
            "SELECT COUNT(*) FROM nodos_extra WHERE categoria=? AND subcategoria=?",
            (categoria, subcategoria),
        ).fetchone()[0]
        check(
            total == esperado,
            f"nodos_extra/{categoria}/{subcategoria}: {total} (esperados {esperado})",
        )

    for tabla in ("preguntas", "nodos_extra"):
        filas, distintas = cur.execute(
            f"SELECT COUNT(*), COUNT(DISTINCT texto) FROM {tabla}"
        ).fetchone()
        check(filas == distintas, f"{tabla}: hay textos duplicados ({filas - distintas})")

    solapadas = cur.execute(
        "SELECT COUNT(*) FROM preguntas p JOIN nodos_extra n ON p.texto = n.texto"
    ).fetchone()[0]
    check(solapadas == 0, f"Hay {solapadas} textos repetidos entre hot y no-hot")

    vacios = cur.execute(
        "SELECT COUNT(*) FROM preguntas WHERE TRIM(texto) = ''"
    ).fetchone()[0]
    check(vacios == 0, f"Hay {vacios} preguntas vacías")

    tipos = {
        fila[0]
        for tabla in ("preguntas", "nodos_extra")
        for fila in cur.execute(f"SELECT DISTINCT tipo FROM {tabla}")
    }
    check(tipos <= {"verdad", "reto"}, f"Tipos inesperados: {sorted(tipos)}")

    con.close()


def verificar_app() -> None:
    print("Aplicación PWA")
    index = APP / "index.html"
    check(index.exists(), "Falta app/index.html")
    if not index.exists():
        return

    html = index.read_text(encoding="utf-8")
    check(len(html) > 500_000, f"index.html parece incompleto ({len(html)} bytes)")
    check("__LOGO_DATA_URI__" not in html, "El logo no se montó en index.html")
    check("data:image/webp;base64," in html, "Falta el logo incrustado")
    check('rel="manifest"' in html, "Falta el enlace al manifest")
    check("serviceWorker" in html, "Falta el registro del service worker")
    check("Digital Assets" in html, "Falta el crédito de Digital Assets")
    check("INSTALAR APP" in html, "Falta el botón de instalación")
    check("Digital Accent" not in html, "Quedó el nombre antiguo Digital Accent")

    manifest_path = APP / "manifest.webmanifest"
    check(manifest_path.exists(), "Falta app/manifest.webmanifest")
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        check(manifest.get("name") == "¿Quién se atreve?", "Nombre del manifest incorrecto")
        for icono in manifest.get("icons", []):
            check((APP / icono["src"]).exists(), f"Falta el icono {icono['src']}")

    sw_path = APP / "sw.js"
    check(sw_path.exists(), "Falta app/sw.js")
    if sw_path.exists():
        sw = sw_path.read_text(encoding="utf-8")
        for ruta in re.findall(r'"(\./[^"]+)"', sw):
            check((APP / ruta[2:]).exists(), f"El service worker referencia {ruta} y no existe")


def main() -> None:
    print("Verificando ¿Quién se atreve?\n")
    verificar_bd()
    verificar_app()
    print()
    if errores:
        print(f"❌ {len(errores)} error(es)")
        sys.exit(1)
    print("✅ Base de datos y PWA correctas")


if __name__ == "__main__":
    main()
