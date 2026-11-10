# Changelog

Todos los cambios importantes de este proyecto se documentan aquí.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y
el versionado sigue [Semantic Versioning](https://semver.org/lang/es/).

## [Unreleased]

### Próximo

- Mejoras de accesibilidad y pruebas en más dispositivos.

### Agregado

- Página de descarga con detección de Android/iOS y QR dinámico para ambas
  plataformas.
- El APK del último release se publica en `app/descargas/quien-se-atreve.apk` y
  se sirve desde GitHub Pages, sin depender de la API de GitHub en tiempo de
  ejecución.

## [1.1.1] - 2026-11-09

### Cambiado

- Nueva base de datos de 1.210 verdades y retos: 610 ítems hot en cuatro
  niveles y 600 ítems normales repartidos en los seis nodos no-hot.
- Eliminada la categoría Familia de la interfaz.
- Verificadores y documentación ajustados a los nuevos conteos.

## [1.1.0] - 2026-10-25

### Agregado

- APK Android empaquetado con Capacitor 7, con los web assets dentro del
  archivo y funcionamiento sin conexión.
- Workflow `android.yml` que compila, firma y publica el APK en GitHub
  Releases al crear un tag `v*`.
- Generación automática de iconos, icono adaptativo y pantallas de inicio
  desde `assets/logo.webp`.
- Firma de producción estable mediante secretos de GitHub Actions.
- Instrucciones de instalación directa del APK, actualización y compilación
  local.

### Cambiado

- La distribución oficial pasa de PWA instalable desde el navegador a APK
  Android.
- `README.md` reescrito para explicar la descarga, instalación, firma,
  versionado y publicación del APK.
- El botón de instalación PWA se oculta dentro de la app nativa.
- El service worker solo se registra en la vista previa web, no en el APK.
- La vista web de GitHub Pages queda como herramienta de desarrollo, no como
  método de instalación.

### Seguridad

- La clave de firma se guarda en los secretos del repositorio y nunca se
  versiona.
- Se documenta que la pérdida de la clave impide actualizar la app instalada.

## [1.0.1] - 2026-10-25

### Agregado

- README profesional con demo, instalación, modelo de ramas, CI/CD y licencia.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md` y `CHANGELOG.md`.
- Plantillas de issues y Pull Request.
- Workflow de CI que reconstruye y verifica el contenido.
- Verificadores `tools/verify.py` y `tools/verify.js`.
- Dependabot para mantener actualizadas las GitHub Actions.

### Cambiado

- `README.md` reescrito y reorganizado.
- Documentación del flujo `main` / `develop` / `feature/*` / `release/*`.
- El workflow de Pages ahora publica solo la carpeta `app/`.

## [1.0.0] - 2026-10-25

### Agregado

- App **¿Quién se atreve?** como PWA instalable.
- 4.432 verdades y retos sin duplicados.
- Modos de preguntas, retos y aleatorio.
- Instalación en Android e iPhone, con funcionamiento offline.
- Logo transparente, iconos PWA y botón de instalación.
- Persistencia de jugadores, partida e historial anti-repetición.
- Términos, crédito **Digital Assets** y aviso de responsabilidad.
- Base de datos SQLite y fuentes CSV editables.
