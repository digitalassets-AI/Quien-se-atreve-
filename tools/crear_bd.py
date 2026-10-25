#!/usr/bin/env python3
"""Construye la base de datos de ¿Quién se atreve? desde los CSV de data/."""
import csv
import re
import sqlite3
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
DATOS = ROOT / "data"
DB = ROOT / "database" / "quien_se_atreve.sqlite"

JUEGOS = {
    "amigos": ("Amigos Hot", "Fiestas entre amigos, verdad o reto de intensidad creciente."),
    "pareja": ("Pareja Hot", "Velada en pareja, de la conexión al cuarto oscuro."),
    "universidad": ("Universidad Hot", "Fiestas universitarias con pasos de intensidad creciente."),
}

NIVELES = {
    "amigos": {1:"Rompehielos", 2:"Coquetas", 3:"Atrevidas", 4:"Calientes",
                5:"Extremas", 6:"Leyenda Fuego"},
    "pareja": {1:"Conexión", 2:"Deseo", 3:"Pasión", 4:"Fuego",
                5:"Éxtasis", 6:"Noche Infinita"},
    "universidad": {1:"Paso 1 · Cero", 2:"Paso 2 · Fuego", 3:"Paso 3 · Pulso",
                     4:"Paso 4 · Límite", 5:"Paso 5 · Tormenta", 6:"Invictus"},
}


def rebuild() -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    if DB.exists():
        DB.unlink()

    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.executescript("""
        CREATE TABLE juegos (
            id TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            descripcion TEXT NOT NULL
        );
        CREATE TABLE niveles (
            juego TEXT NOT NULL REFERENCES juegos(id),
            nivel INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            PRIMARY KEY (juego, nivel)
        );
        CREATE TABLE preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            juego TEXT NOT NULL REFERENCES juegos(id),
            nivel INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('verdad','reto')),
            genero TEXT NOT NULL DEFAULT 'ambos'
                CHECK (genero IN ('ambos','hombre','mujer')),
            texto TEXT NOT NULL UNIQUE,
            texto_hombre TEXT,
            texto_mujer TEXT,
            significado TEXT,
            UNIQUE (juego, nivel, tipo, texto)
        );
        CREATE INDEX idx_preguntas_filtro ON preguntas (juego, nivel, tipo, genero);
        CREATE VIEW preguntas_azar AS
            SELECT id, juego, nivel, tipo, genero, texto,
                   COALESCE(texto_hombre, texto) AS texto_hombre,
                   COALESCE(texto_mujer, texto) AS texto_mujer
            FROM preguntas ORDER BY RANDOM();

        CREATE TABLE glosario (
            termino TEXT PRIMARY KEY,
            definicion TEXT NOT NULL,
            categoria TEXT,
            ejemplo TEXT
        );

        CREATE TABLE nodos_extra (
            categoria TEXT NOT NULL,
            subcategoria TEXT NOT NULL,
            tipo TEXT NOT NULL CHECK (tipo IN ('verdad','reto')),
            texto TEXT NOT NULL UNIQUE
        );
    """)

    for juego, (nombre, desc) in JUEGOS.items():
        cur.execute("INSERT INTO juegos (id, nombre, descripcion) VALUES (?,?,?)",
                    (juego, nombre, desc))
        for n, nombre_nivel in NIVELES[juego].items():
            cur.execute("INSERT INTO niveles (juego, nivel, nombre) VALUES (?,?,?)",
                        (juego, n, nombre_nivel))

    patron = re.compile(r"^([a-z]+)_n(\d+)\.csv$")
    archivos = sorted((DATOS / "hot").glob("*.csv"))
    insertados = duplicados = 0
    for archivo in archivos:
        if archivo.name == "glosario.csv":
            continue
        m = patron.match(archivo.name)
        if not m:
            continue
        juego = m.group(1)
        if juego not in JUEGOS:
            continue
        with archivo.open(encoding="utf-8", newline="") as fh:
            reader = csv.reader(fh)
            for fila in reader:
                if not fila or all(c.strip() == "" for c in fila):
                    continue
                if len(fila) < 4:
                    print(f"[aviso] fila incompleta en {archivo.name}: {fila!r}")
                    continue
                j, nivel, tipo, texto = (fila[i].strip() for i in range(4))
                # Campos opcionales: genero, texto_hombre, texto_mujer, significado
                genero = (fila[4].strip() if len(fila) >= 5 and fila[4].strip() else "ambos")
                t_h = (fila[5].strip() if len(fila) >= 6 and fila[5].strip() else None)
                t_m = (fila[6].strip() if len(fila) >= 7 and fila[6].strip() else None)
                sig = (fila[7].strip() if len(fila) >= 8 and fila[7].strip() else None)
                if j != juego:
                    print(f"[aviso] juego inconsistente en {archivo.name}: {j!r}")
                    continue
                try:
                    cur.execute(
                        "INSERT INTO preguntas (juego, nivel, tipo, genero, texto, "
                        "texto_hombre, texto_mujer, significado) VALUES (?,?,?,?,?,?,?,?)",
                        (juego, int(nivel), tipo, genero, texto, t_h, t_m, sig),
                    )
                    insertados += 1
                except sqlite3.IntegrityError:
                    duplicados += 1

    # Carga del glosario (opcional, data/glosario.csv)
    gl = DATOS / "glosario.csv"
    ngl = 0
    if gl.exists():
        with gl.open(encoding="utf-8", newline="") as fh:
            for fila in csv.reader(fh):
                if not fila or all(c.strip() == "" for c in fila):
                    continue
                if len(fila) < 2:
                    continue
                term = fila[0].strip()
                defin = fila[1].strip()
                cat = fila[2].strip() if len(fila) >= 3 and fila[2].strip() else None
                ej = fila[3].strip() if len(fila) >= 4 and fila[3].strip() else None
                try:
                    cur.execute("INSERT INTO glosario (termino, definicion, categoria, ejemplo) "
                                "VALUES (?,?,?,?)", (term, defin, cat, ej))
                    ngl += 1
                except sqlite3.IntegrityError:
                    pass

    # Nodos no-hot: data/extra/*.csv (columnas: tipo,texto)
    NUEVOS_MAP = {
        "panas": ("amigos", "panas"),
        "mejores_amigos": ("amigos", "mejores_amigos"),
        "conocerse": ("pareja", "conocerse"),
        "conocerse_fondo": ("pareja", "conocerse_fondo"),
        "companeros": ("universidad", "companeros"),
        "amigos_u": ("universidad", "amigos_u"),
    }
    nuevos = 0
    nuevos_dir = DATOS / "extra"
    for nombre, (categoria, subcategoria) in NUEVOS_MAP.items():
        ruta = nuevos_dir / f"{nombre}.csv"
        if not ruta.exists():
            continue
        with ruta.open(encoding="utf-8", newline="") as fh:
            for fila in csv.reader(fh):
                if len(fila) < 2 or not fila[0].strip():
                    continue
                try:
                    cur.execute(
                        "INSERT INTO nodos_extra (categoria, subcategoria, tipo, texto) "
                        "VALUES (?,?,?,?)",
                        (categoria, subcategoria, fila[0].strip(), fila[1].strip()),
                    )
                    nuevos += 1
                except sqlite3.IntegrityError:
                    pass

    con.commit()

    print("=================================================")
    print(f" Insertados preguntas : {insertados}")
    print(f" Duplicados preguntas : {duplicados}")
    print(f" Insertados glosario  : {ngl}")
    print(f" Nodos extra (no-hot) : {nuevos}")
    print("=================================================")
    print(" Conteo por juego y nivel:")
    for juego, nivel, cnt in cur.execute(
            "SELECT juego, nivel, COUNT(*) FROM preguntas "
            "GROUP BY juego, nivel ORDER BY juego, nivel").fetchall():
        print(f"   {juego:12s} N{nivel} ({NIVELES[juego][nivel]:18s}) : {cnt:4d}")
    total = cur.execute("SELECT COUNT(*) FROM preguntas").fetchone()[0]
    print("-------------------------------------------------")
    print(f" TOTAL PREGUNTAS: {total}  | GLOSARIO: {ngl}")
    print(f" NODOS NO-HOT   : {nuevos}  | TOTAL JUEGO: {total + nuevos}")
    v = cur.execute("SELECT COUNT(*) FROM preguntas WHERE tipo='verdad'").fetchone()[0]
    r = cur.execute("SELECT COUNT(*) FROM preguntas WHERE tipo='reto'").fetchone()[0]
    print(f" Verdad: {v}   Reto: {r}")
    con.close()


if __name__ == "__main__":
    rebuild()
