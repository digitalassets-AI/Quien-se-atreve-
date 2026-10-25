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
  <img alt="18+" src="https://img.shields.io/badge/18%2B-solo%20adultos-ff0066">
  <img alt="PWA" src="https://img.shields.io/badge/PWA-instalable-5a0fc8">
  <img alt="Offline" src="https://img.shields.io/badge/offline-s%C3%AD-00a86b">
  <img alt="Licencia MIT" src="https://img.shields.io/badge/c%C3%B3digo-MIT-ffcc00">
</p>

> **Aviso:** contenido pensado para personas mayores de 18 años. Los retos son
> opcionales y siempre deben jugarse con respeto y consentimiento. **Digital
> Assets no se responsabiliza de nada** de lo que ocurra antes, durante o
> después del juego.

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

## Instalar en el celular

La app se publica con **GitHub Pages** y se instala desde el navegador. No hace
falta tienda de aplicaciones ni archivo APK.

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

- **2.202 preguntas + 2.198 retos + 32 de familia**.
- Cero duplicados exactos entre los 4.432 textos visibles.
- Cada nodo no-hot tiene 200 preguntas y 200 retos.
- Los textos con variante de género usan `["base", "hombre", "mujer"]` y se
  resuelven según el jugador.

## Estructura del proyecto

```text
quien-se-atreve/
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
│   └── make_icons.py            # Genera los iconos desde el logo
├── .github/workflows/pages.yml  # Despliegue automático a GitHub Pages
└── README.md
```

### ¿Por qué solo hay una base de datos?

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

Requisitos: **Python 3.10+**. Para regenerar los iconos, **Pillow** y **NumPy**.

```bash
# Reconstruir la base de datos y la app final
python3 tools/build.py

# Solo si cambia el logo (requiere Pillow y NumPy)
python3 -m pip install -r tools/requirements.txt
python3 tools/make_icons.py
```

Si publicas una actualización y la app ya estaba instalada, sube `VERSION` en
`app/sw.js` para que el service worker descarte la caché anterior.

El build deja la app lista en `app/index.html`. Para probarla en local:

```bash
cd app
python3 -m http.server 8765
# Abre http://localhost:8765
```

No abras `app/index.html` con `file://` si quieres probar la instalación PWA:
el service worker necesita `http://` o `https://`.

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

1. Crea un repositorio llamado `quien-se-atreve` en GitHub.
2. Sube este proyecto a la rama `main`.
3. En **Settings → Pages → Build and deployment**, elige **GitHub Actions**.
4. El workflow `.github/workflows/pages.yml` publicará la carpeta `app/`.
5. Abre la URL que muestra GitHub Pages en el celular e instala la app.

```bash
git init -b main
git add .
git commit -m "feat: lanzar ¿Quién se atreve? como PWA"
git remote add origin https://github.com/TU-USUARIO/quien-se-atreve.git
git push -u origin main
```

## Privacidad

La app no recopila datos personales, no usa analítica y no envía información a
ningún servidor. Los jugadores y el historial de preguntas se guardan únicamente
en `localStorage`, en el dispositivo.

## Licencia y créditos

El código se distribuye bajo licencia **MIT** (ver `LICENSE`). El nombre
**¿Quién se atreve?**, el logo y los textos del juego son propiedad de
**Digital Assets** y no se incluyen en esa licencia.

Hecho por **Digital Assets**.
