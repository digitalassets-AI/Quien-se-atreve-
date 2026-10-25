#!/usr/bin/env python3
"""Monta el contenido del juego dentro de la interfaz HTML.

Estructura de nodos (categoría -> subcategoría -> {questions, actions}):

  Nodos HOT     -> contenido de la BD (database/quien_se_atreve.sqlite).
  Nodos NO-HOT  -> contenido de data/extra/<subcategoria>.csv
                   (200 verdades + 200 retos por nodo).

Uso:
    python3 tools/montar_interfaz.py [plantilla.html] [salida.html]
"""
import base64
import csv
import json
import sqlite3
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DB = ROOT / "database" / "quien_se_atreve.sqlite"
LOGO = ROOT / "assets" / "logo.webp"
NUEVOS = ROOT / "data" / "extra"
PLANTILLA = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "src" / "interfaz_base.html"
SALIDA = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "app" / "index.html"

# --- Nodos HOT: contenido explícito de la BD (todos los niveles del juego) ---
HOT = {
    "amigos": {"amigos_hot": "amigos"},
    "pareja": {"pareja_hot": "pareja"},
    "universidad": {"universidad_hot": "universidad"},
}

# --- Nodos NO-HOT: contenido nuevo (CSV en data/extra) ---
NUEVOS_NODOS = {
    "amigos": {"panas": "panas", "mejores_amigos": "mejores_amigos"},
    "pareja": {"conocerse": "conocerse", "conocerse_fondo": "conocerse_fondo"},
    "universidad": {"companeros": "companeros", "amigos_u": "amigos_u"},
}

# Orden de las claves dentro de cada categoría (coincide con la UI)
ORDEN = {
    "amigos": ["panas", "mejores_amigos", "amigos_hot"],
    "pareja": ["conocerse", "conocerse_fondo", "pareja_hot"],
    "universidad": ["universidad_hot", "companeros", "amigos_u"],
}


def item_de(texto, th, tm):
    """Devuelve un string o [base, hombre, mujer] si hay variante de género."""
    if th and tm:
        return [texto, th, tm]
    return texto


def cargar_hot(juego):
    """Todos los registros de un juego de la BD, separados por tipo."""
    con = sqlite3.connect(DB)
    filas = con.execute(
        "SELECT tipo, texto, texto_hombre, texto_mujer FROM preguntas "
        "WHERE juego=? ORDER BY nivel, id", (juego,)).fetchall()
    con.close()
    q, a = [], []
    for tipo, texto, th, tm in filas:
        (q if tipo == "verdad" else a).append(item_de(texto, th, tm))
    return {"questions": q, "actions": a}


def cargar_nuevo(nombre):
    """Lee data/extra/<nombre>.csv (columnas: tipo,texto)."""
    ruta = NUEVOS / f"{nombre}.csv"
    q, a = [], []
    with ruta.open(encoding="utf-8", newline="") as fh:
        for fila in csv.reader(fh):
            if len(fila) < 2 or not fila[0].strip():
                continue
            tipo, texto = fila[0].strip(), fila[1].strip()
            (q if tipo == "verdad" else a).append(texto)
    return {"questions": q, "actions": a}


def cargar_nodos():
    nodos = {}
    for juego, orden in ORDEN.items():
        nodos[juego] = {}
        for subcat in orden:
            if subcat in HOT.get(juego, {}):
                nodos[juego][subcat] = cargar_hot(HOT[juego][subcat])
            elif subcat in NUEVOS_NODOS.get(juego, {}):
                nodos[juego][subcat] = cargar_nuevo(NUEVOS_NODOS[juego][subcat])
    return nodos


def bloque_js(nodos):
    partes = []
    for juego, subcats in nodos.items():
        lineas = [f"  {juego}: {{"]
        for subcat, data in subcats.items():
            lineas.append(f"    {subcat}: {{")
            for clave in ("questions", "actions"):
                lineas.append(f"      {clave}: [")
                for item in data[clave]:
                    lineas.append("        " + json.dumps(item, ensure_ascii=False) + ",")
                lineas.append("      ],")
            lineas.append("    },")
        lineas.append("  },")
        partes.append("\n".join(lineas))
    return "\n".join(partes) + "\n"


def montar():
    html = PLANTILLA.read_text(encoding="utf-8")
    if not LOGO.exists():
        raise SystemExit(f"Falta el logo: {LOGO}")
    logo_b64 = base64.b64encode(LOGO.read_bytes()).decode("ascii")
    html = html.replace("__LOGO_DATA_URI__", f"data:image/webp;base64,{logo_b64}")
    nodos = cargar_nodos()

    ini = html.index("const challenges = {")
    fam_ini = html.index("familia: {", ini)
    amigos_ini = html.index("amigos: {", fam_ini)
    familia = html[fam_ini:amigos_ini]        # familia + su cierre "  },\n  "
    fin_obj = html.index("};", ini)          # primer "};" tras el inicio = cierre de challenges
    pie = html[fin_obj + 2:]

    nuevo_obj = "const challenges = {\n" + familia + bloque_js(nodos) + "};"
    html = html[:ini] + nuevo_obj + pie
    SALIDA.write_text(html, encoding="utf-8")

    print(f"Interfaz montada -> {SALIDA}")
    for juego, subcats in nodos.items():
        for subcat, d in subcats.items():
            print(f"  {juego:12s} {subcat:18s} questions:{len(d['questions']):4d}  actions:{len(d['actions']):4d}")
    tq = sum(len(d["questions"]) for j in nodos.values() for d in j.values())
    ta = sum(len(d["actions"]) for j in nodos.values() for d in j.values())
    print(f" TOTAL montado: {tq + ta} ({tq} preguntas + {ta} retos)")


if __name__ == "__main__":
    montar()
