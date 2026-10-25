#!/usr/bin/env python3
"""Ajusta el proyecto Android generado por Capacitor antes de compilar.

El proyecto ``android/`` no se versiona: el workflow lo crea con
``npx cap add android`` y este script aplica nombre, versión, orientación,
colores del sistema y la firma de producción cuando existen los secretos.

Uso:
    python3 tools/prepare_android.py
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID = ROOT / "android"
APP = ANDROID / "app"

APP_NAME = "¿Quién se atreve?"
STATUS_ITEMS = (
    '<item name="android:statusBarColor">#1A0033</item>',
    '<item name="android:navigationBarColor">#1A0033</item>',
    '<item name="android:windowLightStatusBar">false</item>',
    '<item name="android:windowLightNavigationBar">false</item>',
)


def leer_paquete() -> dict:
    return json.loads((ROOT / "package.json").read_text(encoding="utf-8"))


def versiones(paquete: dict) -> tuple[int, str]:
    nombre = os.environ.get("ANDROID_VERSION_NAME", str(paquete["version"])).strip()
    codigo_txt = os.environ.get("ANDROID_VERSION_CODE", "").strip()
    if codigo_txt:
        codigo = int(codigo_txt)
    else:
        # 1.1.0 -> 10100. Deja espacio para parches y mantenimientos.
        partes = [int(p) for p in re.findall(r"\d+", nombre)[:3]]
        partes += [0] * (3 - len(partes))
        codigo = partes[0] * 10_000 + partes[1] * 100 + partes[2]
    if codigo < 1:
        raise SystemExit("ANDROID_VERSION_CODE debe ser mayor que 0")
    return codigo, nombre


def parchear_gradle(codigo: int, nombre: str) -> None:
    ruta = APP / "build.gradle"
    texto = ruta.read_text(encoding="utf-8")
    texto, n_codigo = re.subn(r"versionCode\s+\d+", f"versionCode {codigo}", texto)
    texto, n_nombre = re.subn(
        r'versionName\s+"[^"]*"', f'versionName "{nombre}"', texto
    )
    if not n_codigo or not n_nombre:
        raise SystemExit("No se encontraron versionCode/versionName en build.gradle")
    ruta.write_text(texto, encoding="utf-8")


def parchear_strings() -> None:
    ruta = APP / "src" / "main" / "res" / "values" / "strings.xml"
    texto = ruta.read_text(encoding="utf-8")
    for clave in ("app_name", "title_activity_main"):
        texto = re.sub(
            rf'(<string name="{clave}">).*?(</string>)',
            rf"\g<1>{APP_NAME}\g<2>",
            texto,
        )
    ruta.write_text(texto, encoding="utf-8")


def parchear_manifest() -> None:
    ruta = APP / "src" / "main" / "AndroidManifest.xml"
    texto = ruta.read_text(encoding="utf-8")
    if "android:screenOrientation=\"portrait\"" not in texto:
        texto = texto.replace(
            'android:name=".MainActivity"',
            'android:name=".MainActivity"\n            android:screenOrientation="portrait"',
            1,
        )
    ruta.write_text(texto, encoding="utf-8")


def parchear_estilos() -> None:
    ruta = APP / "src" / "main" / "res" / "values" / "styles.xml"
    texto = ruta.read_text(encoding="utf-8")

    def agregar(estilo: str, contenido: str) -> str:
        patron = rf'(<style name="{estilo}"[^>]*>)(.*?)(\s*</style>)'
        match = re.search(patron, contenido, flags=re.S)
        if not match:
            raise SystemExit(f"No se encontró el estilo {estilo} en styles.xml")
        cuerpo = match.group(2)
        for item in STATUS_ITEMS:
            if item not in cuerpo:
                cuerpo += f"\n        {item}"
        return contenido[: match.start()] + match.group(1) + cuerpo + match.group(3) + contenido[match.end() :]

    texto = agregar("AppTheme.NoActionBar", texto)
    texto = agregar("AppTheme.NoActionBarLaunch", texto)
    ruta.write_text(texto, encoding="utf-8")


def configurar_firma() -> bool:
    clave = os.environ.get("ANDROID_KEYSTORE_PASSWORD", "").strip()
    alias = os.environ.get("ANDROID_KEY_ALIAS", "").strip()
    clave_clave = os.environ.get("ANDROID_KEY_PASSWORD", "").strip()
    if not (clave and alias and clave_clave):
        print("  · Firma de producción no configurada (build de depuración).")
        return False

    signing = APP / "signing.gradle"
    signing.write_text(
        """android {
    signingConfigs {
        release {
            storeFile file("release-key.p12")
            storePassword System.getenv("ANDROID_KEYSTORE_PASSWORD")
            keyAlias System.getenv("ANDROID_KEY_ALIAS")
            keyPassword System.getenv("ANDROID_KEY_PASSWORD")
            storeType "PKCS12"
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
""",
        encoding="utf-8",
    )

    gradle = APP / "build.gradle"
    texto = gradle.read_text(encoding="utf-8")
    if "apply from: 'signing.gradle'" not in texto:
        texto += "\napply from: 'signing.gradle'\n"
        gradle.write_text(texto, encoding="utf-8")
    print("  · Firma de producción configurada (PKCS12).")
    return True


def main() -> None:
    if not APP.exists():
        raise SystemExit("Falta android/. Ejecuta primero: npx cap add android")

    paquete = leer_paquete()
    codigo, nombre = versiones(paquete)

    parchear_gradle(codigo, nombre)
    parchear_strings()
    parchear_manifest()
    parchear_estilos()
    configurar_firma()

    print(f"Proyecto Android preparado: {APP_NAME} {nombre} ({codigo})")
    print("  · Nombre, versión y orientación vertical")
    print("  · Barras de estado y navegación oscuras")


if __name__ == "__main__":
    main()
