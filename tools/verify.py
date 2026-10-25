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
    print("Aplicación web y APK")
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
    check("isNativeApp" in html, "Falta la detección de la app nativa")
    check("!isNativeApp" in html, "El service worker no está desactivado en la app nativa")
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


def verificar_android() -> None:
    print("Empaquetado Android")
    paquete_path = ROOT / "package.json"
    check(paquete_path.exists(), "Falta package.json")
    if paquete_path.exists():
        paquete = json.loads(paquete_path.read_text(encoding="utf-8"))
        check(paquete.get("name") == "quien-se-atreve", "Nombre de package.json incorrecto")
        check(
            bool(re.fullmatch(r"\d+\.\d+\.\d+", str(paquete.get("version", "")))),
            "Versión de package.json inválida",
        )
        dependencias = {**paquete.get("dependencies", {}), **paquete.get("devDependencies", {})}
        for dependencia in ("@capacitor/core", "@capacitor/android", "@capacitor/cli"):
            check(dependencia in dependencias, f"Falta {dependencia} en package.json")
        check(
            paquete.get("scripts", {}).get("android:release") == "cd android && ./gradlew assembleRelease",
            "Falta el script android:release",
        )

    config_path = ROOT / "capacitor.config.json"
    check(config_path.exists(), "Falta capacitor.config.json")
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        check(config.get("appId") == "com.digitalassets.quienseatreve", "appId de Capacitor incorrecto")
        check(config.get("appName") == "¿Quién se atreve?", "appName de Capacitor incorrecto")
        check(config.get("webDir") == "app", "webDir de Capacitor incorrecto")

    for ruta in (
        "tools/make_android_assets.py",
        "tools/prepare_android.py",
        ".github/workflows/android.yml",
    ):
        check((ROOT / ruta).exists(), f"Falta {ruta}")

    workflow = ROOT / ".github" / "workflows" / "android.yml"
    if workflow.exists():
        texto = workflow.read_text(encoding="utf-8")
        for fragmento in ("assembleRelease", "apksigner", "softprops/action-gh-release"):
            check(fragmento in texto, f"android.yml no incluye {fragmento}")

    indice = ROOT / "app" / "index.html"
    if indice.exists():
        html = indice.read_text(encoding="utf-8")
        check("Capacitor" in html, "La app no detecta Capacitor")
        check("isNativeApp" in html, "La app no detecta el modo nativo")

    readme = ROOT / "README.md"
    if readme.exists():
        texto = readme.read_text(encoding="utf-8")
        check("APK" in texto, "El README no menciona el APK")
        check("releases/latest" in texto, "El README no enlaza a las Releases")

    check("android/" in (ROOT / ".gitignore").read_text(encoding="utf-8"), "android/ no está ignorado")
    check("*.p12" in (ROOT / ".gitignore").read_text(encoding="utf-8"), "Las claves PKCS12 no están ignoradas")


def main() -> None:
    print("Verificando ¿Quién se atreve?\n")
    verificar_bd()
    verificar_app()
    verificar_android()
    print()
    if errores:
        print(f"❌ {len(errores)} error(es)")
        sys.exit(1)
    print("✅ Base de datos, web y empaquetado Android correctos")


if __name__ == "__main__":
    main()
