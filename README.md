<p align="center">
  <img src="assets/logo.webp" alt="¿Quién se atreve?" width="280">
</p>

<h1 align="center">¿Quién se atreve?</h1>

<p align="center">
  Juego de verdades y retos para amigos, pareja y universidad.
  <br>
  <b>Hecho por Digital Assets</b>
</p>

<p align="center">
  <a href="https://github.com/digitalassets-AI/Quien-se-atreve-/actions/workflows/ci.yml">
    <img alt="CI" src="https://github.com/digitalassets-AI/Quien-se-atreve-/actions/workflows/ci.yml/badge.svg?branch=main">
  </a>
  <a href="https://github.com/digitalassets-AI/Quien-se-atreve-/actions/workflows/pages.yml">
    <img alt="Deploy" src="https://github.com/digitalassets-AI/Quien-se-atreve-/actions/workflows/pages.yml/badge.svg?branch=main">
  </a>
  <img alt="18+" src="https://img.shields.io/badge/18%2B-solo%20adultos-ff0066">
  <img alt="PWA" src="https://img.shields.io/badge/PWA-instalable-5a0fc8">
  <img alt="Offline" src="https://img.shields.io/badge/offline-s%C3%AD-00a86b">
  <img alt="Licencia MIT" src="https://img.shields.io/badge/c%C3%B3digo-MIT-ffcc00">
</p>

> **Aviso:** contenido pensado para personas mayores de 18 años. Los retos son
> opcionales y siempre deben jugarse con respeto y consentimiento. **Digital
> Assets no se responsabiliza de nada** de lo que ocurra antes, durante o
> después del juego.

## Demo

La app se publica automáticamente en **GitHub Pages** al hacer merge a `main`:

```text
https://digitalassets-AI.github.io/Quien-se-atreve-/
```

Si el enlace aún no responde, activa Pages en **Settings → Pages → GitHub
Actions** y ejecuta el workflow **Deploy PWA to GitHub Pages**.

## Tabla de contenido

- [¿Qué es?](#qué-es)
- [Características](#características)
- [Instalar en el celular](#instalar-en-el-celular)
- [Contenido](#contenido)
- [Modelo de ramas](#modelo-de-ramas)
- [Flujo de trabajo](#flujo-de-trabajo)
- [Convención de commits](#convención-de-commits)
- [CI/CD](#cicd)
- [Estructura del proyecto](#estructura-del-proyecto)
- [¿Por qué solo hay una base de datos?](#por-qué-solo-hay-una-base-de-datos)
- [Desarrollo](#desarrollo)
- [Base de datos](#base-de-datos)
- [Publicar en GitHub Pages](#publicar-en-github-pages)
- [Contribuir](#contribuir)
- [Privacidad y seguridad](#privacidad-y-seguridad)
- [Licencia y créditos](#licencia-y-créditos)

## ¿Qué es?

Una app web instalable (PWA) con **4.432 verdades y retos** repartidos en tres
categorías y nueve subcategorías. Funciona sin conexión, guarda los jugadores en
el dispositivo y no repite contenido dentro de una partida.

- **Amigos:** panas, mejores amigos y amigos 🔥
- **Pareja:** conocerse, conocerse a fondo y pareja 🔥
- **Universidad:** compañeros, amigos de la U y universidad 🔥
- **Familia:** primos y familia (contenido base incluido en la app)
- Tres modos: **💬 Preguntas**, **🔥 Retos** y **🎲 Aleatorio**
- Cambio de modo desde la pantalla del giro, sin salir de la partida
- Jugadores guardados, saltos por jugador y botella animada
- Historial anti-repetición persistente y botón para reiniciarlo
- Glosario integrado para las palabras menos comunes

## Características

| Característica | Detalle |
|---|---|
| Instalable | PWA con manifest, iconos y pantalla completa |
| Offline | Service worker con caché del app shell |
| Sin backend | Todo se ejecuta en el navegador |
| Persistencia | `localStorage`: jugadores, partida e historial |
| Anti-repetición | Historial global por texto base, persistente |
| Responsive | Diseñada para teléfonos, tablets y escritorio |
| Accesibilidad | Lighthouse 100 en accesibilidad, buenas prácticas y SEO |
| Privacidad | Sin analítica, sin cuentas y sin envío de datos |

## Instalar en el celular

La app se instala desde el navegador. No hace falta tienda de aplicaciones ni
archivo APK.

### Android

1. Abre la URL publicada en **Chrome**.
2. Toca el botón **📲 INSTALAR APP** o el menú **⋮ → Instalar app**.
3. Confirma. El icono aparecerá en tu pantalla de inicio.

### iPhone / iPad

1. Abre la URL publicada en **Safari**.
2. Toca **Compartir**.
3. Elige **Agregar a pantalla de inicio** y confirma.

Después de la primera carga, la app abre sin conexión. En Android, Chrome
mostrará el aviso de instalación; en iPhone, el botón de la app explica los
pasos.

> **¿APK?** Si necesitas un archivo `.apk`, se puede generar con
> [PWABuilder](https://www.pwabuilder.com/) a partir de la URL publicada o con un
> wrapper de Capacitor. La PWA es la vía recomendada para Android e iOS.

## Contenido

| Categoría   | Subcategoría       | Ítems | Origen                    |
|-------------|--------------------|:-----:|---------------------------|
| Familia     | primos / familia   |   32  | Incluido en la plantilla  |
| Amigos      | panas              |  400  | `data/extra/panas.csv`    |
| Amigos      | mejores_amigos     |  400  | `data/extra/mejores_amigos.csv` |
| Amigos      | amigos_hot         |  600  | Base de datos             |
| Pareja      | conocerse          |  400  | `data/extra/conocerse.csv` |
| Pareja      | conocerse_fondo    |  400  | `data/extra/conocerse_fondo.csv` |
| Pareja      | pareja_hot         |  800  | Base de datos             |
| Universidad | universidad_hot    |  600  | Base de datos             |
| Universidad | companeros         |  400  | `data/extra/companeros.csv` |
| Universidad | amigos_u           |  400  | `data/extra/amigos_u.csv` |
| **Total**   |                    | **4.432** | 4.400 + 32 de familia |

- **2.218 preguntas + 2.214 retos** en el HTML final.
- Cero duplicados exactos entre los 4.432 textos visibles.
- Cada nodo no-hot tiene 200 preguntas y 200 retos.
- Los textos con variante de género usan `["base", "hombre", "mujer"]` y se
  resuelven según el jugador.

## Modelo de ramas

El repositorio usa un flujo **Git Flow simplificado**:

| Rama | Propósito | ¿Despliega? |
|---|---|:---:|
| `main` | Producción estable | ✅ Sí |
| `develop` | Integración de la próxima versión | ❌ No |
| `feature/*` | Nuevas funciones o contenido | ❌ No |
| `fix/*` | Correcciones no urgentes | ❌ No |
| `release/*` | Preparación de una versión | ❌ No |
| `hotfix/*` | Corrección urgente desde `main` | Al mergear a `main` |

```text
main ───●──────────────●──────────────●───▶
         \            /              /
develop   ●──●──●──●──●──●──●──●──●──●───▶
             \     /     \     /
feature/*     ●───●       ●───●
```

Reglas:

1. Nadie trabaja directamente sobre `main`.
2. Toda función nace de `develop` en `feature/<nombre>`.
3. Todo cambio entra por **Pull Request** y debe pasar el CI.
4. `develop` se integra a `main` solo para publicar una versión.
5. Los tags de versión se crean sobre `main` (`v1.0.0`, `v1.1.0`, ...).

## Flujo de trabajo

### Nueva función o contenido

```bash
git switch develop
git pull origin develop
git switch -c feature/nueva-subcategoria

# editar datos, interfaz o documentación
python3 tools/build.py
python3 tools/verify.py
node tools/verify.js

git add .
git commit -m "feat(contenido): agregar subcategoría de oficina"
git push -u origin feature/nueva-subcategoria
```

Abre un Pull Request hacia `develop`.

### Corrección normal

```bash
git switch develop
git switch -c fix/boton-instalar-ios
# corregir
git commit -am "fix(pwa): mostrar instrucciones correctas en iOS"
git push -u origin fix/boton-instalar-ios
```

### Publicar una versión

```bash
git switch develop
git pull origin develop
git switch -c release/1.1.0

# actualizar CHANGELOG.md y probar
git commit -am "chore(release): preparar 1.1.0"

git switch main
git merge --no-ff release/1.1.0
git tag -a v1.1.0 -m "Versión 1.1.0"
git push origin main --tags

git switch develop
git merge --no-ff main
git push origin develop
```

### Hotfix urgente

```bash
git switch main
git switch -c hotfix/error-critico
# corregir
git commit -am "fix: corregir error crítico"
git switch main
git merge --no-ff hotfix/error-critico
git tag -a v1.0.2 -m "Versión 1.0.2"
git push origin main --tags
git switch develop
git merge --no-ff main
git push origin develop
```

## Convención de commits

Se usa [Conventional Commits](https://www.conventionalcommits.org/es/):

| Prefijo | Uso |
|---|---|
| `feat:` | Nueva función o contenido |
| `fix:` | Corrección de un error |
| `docs:` | Solo documentación |
| `style:` | Formato sin cambios de lógica |
| `refactor:` | Reestructuración sin cambiar comportamiento |
| `test:` | Pruebas |
| `chore:` | Mantenimiento, build o dependencias |
| `ci:` | Cambios en GitHub Actions |

Ejemplos:

```text
feat(pwa): agregar botón de instalación
fix(contenido): corregir pregunta duplicada
docs(readme): documentar modelo de ramas
ci: verificar el contenido en cada pull request
```

## CI/CD

| Workflow | Cuándo se ejecuta | Qué hace |
|---|---|---|
| `ci.yml` | Push a `main`/`develop` y Pull Requests | Reconstruye, verifica contenido y comprueba que `app/index.html` esté actualizado |
| `pages.yml` | Push a `main` o ejecución manual | Publica `app/` en GitHub Pages |

Comandos que ejecuta el CI:

```bash
python3 tools/build.py
python3 tools/verify.py
node tools/verify.js
git diff --exit-code -- app
```

Si el build genera un `app/index.html` distinto al commiteado, el CI falla. Eso
evita publicar una app desactualizada respecto de los CSV o la base de datos.

### Proteger `main`

En **Settings → Branches → Add branch protection rule**:

1. Patrón: `main`.
2. Activar **Require a pull request before merging**.
3. Activar **Require status checks to pass** y seleccionar **CI / verify**.
4. Activar **Do not allow bypassing the above settings**.
5. Repetir una regla más flexible para `develop`.

## Estructura del proyecto

```text
Quien-se-atreve-/
├── app/                         # Sitio que se publica (PWA)
│   ├── index.html               # App final, autónoma y con el logo incrustado
│   ├── manifest.webmanifest
│   ├── sw.js                    # Service worker (funciona offline)
│   └── icons/                   # Iconos 192/512, maskable, Apple y favicon
├── assets/
│   └── logo.webp                # Logo original con transparencia
├── data/
│   ├── hot/                     # 18 CSV (6 niveles × 3 juegos)
│   ├── extra/                   # 6 CSV de los nodos no-hot
│   └── glosario.csv             # 72 términos
├── database/
│   └── quien_se_atreve.sqlite   # Única base de datos del proyecto
├── src/
│   └── interfaz_base.html       # Plantilla editable de la interfaz
├── tools/
│   ├── build.py                 # Reconstruye BD + app
│   ├── crear_bd.py              # CSV → SQLite
│   ├── montar_interfaz.py       # SQLite + CSV + logo → app/index.html
│   ├── make_icons.py            # Genera los iconos desde el logo
│   ├── verify.py                # Verifica BD, PWA y archivos
│   ├── verify.js                # Verifica los 4.432 ítems finales
│   └── requirements.txt         # Solo para regenerar iconos
├── .github/
│   ├── workflows/
│   │   ├── ci.yml
│   │   └── pages.yml
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── SECURITY.md
```

## ¿Por qué solo hay una base de datos?

Solo existe **`database/quien_se_atreve.sqlite`**. Los demás archivos cumplen
funciones distintas y no son bases de datos duplicadas:

- **`data/hot/*.csv`**: fuente editable de las 2.000 preguntas y retos hot.
- **`data/extra/*.csv`**: fuente editable de los 2.400 ítems no-hot.
- **`data/glosario.csv`**: fuente del glosario.
- **`app/index.html`**: lleva todo el contenido incrustado para funcionar sin
  servidor ni base de datos en el celular.
- **`database/quien_se_atreve.sqlite`**: se genera desde los CSV y se usa para
  montar la app. Es la única BD del repositorio.

El antiguo volcado `.sql` y las copias de revisión se eliminaron porque eran
artefactos regenerables.

## Desarrollo

Requisitos: **Python 3.10+** y **Node.js 18+** para las verificaciones. Para
regenerar los iconos, **Pillow** y **NumPy**.

```bash
# Reconstruir la base de datos y la app final
python3 tools/build.py

# Verificar integridad y contenido
python3 tools/verify.py
node tools/verify.js

# Solo si cambia el logo (requiere Pillow y NumPy)
python3 -m pip install -r tools/requirements.txt
python3 tools/make_icons.py
```

El build deja la app lista en `app/index.html`. Para probarla en local:

```bash
cd app
python3 -m http.server 8765
# Abre http://localhost:8765
```

No abras `app/index.html` con `file://` si quieres probar la instalación PWA:
el service worker necesita `http://` o `https://`.

Si publicas una actualización y la app ya estaba instalada, sube `VERSION` en
`app/sw.js` para que el service worker descarte la caché anterior.

## Base de datos

`database/quien_se_atreve.sqlite` contiene:

- `juegos(id, nombre, descripcion)`
- `niveles(juego, nivel, nombre)`
- `preguntas(id, juego, nivel, tipo, texto, genero, texto_hombre, texto_mujer, significado)`
- `glosario(termino, definicion, categoria, ejemplo)`
- `nodos_extra(categoria, subcategoria, tipo, texto)`
- Vista `preguntas_azar` e índices por `(juego, nivel, tipo)`

Conteos: **2.000** filas hot en `preguntas`, **2.400** en `nodos_extra` y **72**
términos en `glosario`. `tipo` es `verdad` o `reto`.

Consulta rápida:

```bash
sqlite3 database/quien_se_atreve.sqlite \
  "SELECT juego, nivel, tipo, COUNT(*) FROM preguntas GROUP BY 1,2,3;"
```

## Publicar en GitHub Pages

La primera vez:

1. Sube `main` y `develop`:

   ```bash
   git push -u origin main
   git push -u origin develop
   ```

2. En GitHub, entra a **Settings → Pages**.
3. En **Build and deployment → Source**, elige **GitHub Actions**.
4. Ejecuta el workflow **Deploy PWA to GitHub Pages** desde la pestaña
   **Actions** si no se lanzó automáticamente.
5. Abre la URL publicada en el celular e instala la app.

A partir de ahí, cada merge a `main` publica una nueva versión.

## Contribuir

Lee [`CONTRIBUTING.md`](CONTRIBUTING.md) para el flujo de ramas, la convención de
commits y la checklist de Pull Request. Todas las contribuciones deben respetar
el [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## Privacidad y seguridad

La app no recopila datos personales, no usa analítica y no envía información a
ningún servidor. Los jugadores y el historial de preguntas se guardan únicamente
en `localStorage`, en el dispositivo.

Para reportar una vulnerabilidad, usa **Security → Report a vulnerability** en
GitHub. No publiques tokens, credenciales ni datos personales en issues o Pull
Requests. Más detalles en [`SECURITY.md`](SECURITY.md).

## Licencia y créditos

El código se distribuye bajo licencia **MIT** (ver [`LICENSE`](LICENSE)). El
nombre **¿Quién se atreve?**, el logo y los textos del juego son propiedad de
**Digital Assets** y no se incluyen en esa licencia.

Hecho por **Digital Assets**.
