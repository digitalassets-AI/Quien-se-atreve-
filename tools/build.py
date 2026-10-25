#!/usr/bin/env python3
"""Reconstruye la base de datos y la app final desde las fuentes.

Uso:
    python3 tools/build.py
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent


def main() -> None:
    for script in ("crear_bd.py", "montar_interfaz.py"):
        print(f"\n▶ {script}")
        subprocess.run([sys.executable, str(BASE / script)], check=True)
    print("\n✅ Build completo: app/index.html")


if __name__ == "__main__":
    main()
