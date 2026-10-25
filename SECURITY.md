# Seguridad

## Reportar una vulnerabilidad

No abras un issue público para vulnerabilidades. Usa la pestaña **Security →
Report a vulnerability** del repositorio en GitHub. Si esa opción no está
disponible, contacta de forma privada a **Digital Assets**.

Incluye:

- Descripción del problema.
- Pasos para reproducirlo.
- Versión de la app, dispositivo y versión de Android.
- Impacto potencial.
- Posible solución, si la tienes.

## Alcance

La distribución oficial es un **APK Android** que contiene los web assets y se
ejecuta en un WebView local. No hay backend, cuentas ni base de datos remota.

- Los jugadores y el historial se guardan en `localStorage`, dentro del WebView.
- No se envían datos a servidores.
- No se usan cookies de analítica.
- La vista previa web en GitHub Pages registra un service worker para cachear
  el app shell. El APK no lo necesita porque los archivos ya están incluidos.
- El APK incluye el permiso `INTERNET` que trae la plantilla de Capacitor, pero
  el juego no realiza peticiones de red para funcionar.

## Firma del APK

La firma de producción se guarda en los secretos de GitHub Actions:

- `ANDROID_KEYSTORE_BASE64`
- `ANDROID_KEYSTORE_PASSWORD`
- `ANDROID_KEY_ALIAS`
- `ANDROID_KEY_PASSWORD`

Nunca se versiona el keystore ni sus contraseñas. La pérdida o filtración de la
clave afecta la capacidad de publicar actualizaciones que Android acepte sobre
la app instalada. Si la clave se compromete, hay que evaluar un cambio de
`appId` o una reinstalación limpia.

## Buenas prácticas

- No publiques tokens, credenciales, keystores ni datos personales en issues o
  PRs.
- Revisa los cambios de dependencias de GitHub Actions y de Capacitor.
- Mantén `actions/checkout`, `actions/setup-*`, `android-actions/setup-android`
  y las acciones de Pages actualizadas.
- Verifica el APK con `apksigner verify --print-certs` antes de publicarlo.
- Si encuentras contenido inapropiado, repórtalo de forma privada.
