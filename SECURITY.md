# Seguridad

## Reportar una vulnerabilidad

No abras un issue público para vulnerabilidades. Usa la pestaña **Security →
Report a vulnerability** del repositorio en GitHub. Si esa opción no está
disponible, contacta de forma privada a **Digital Assets**.

Incluye:

- Descripción del problema.
- Pasos para reproducirlo.
- Navegador, sistema operativo y versión de la app.
- Impacto potencial.
- Posible solución, si la tienes.

## Alcance

Este proyecto es una app estática que se ejecuta en el navegador. No tiene
backend, cuentas ni base de datos remota.

- Los jugadores y el historial se guardan en `localStorage`.
- No se envían datos a servidores.
- No se usan cookies de analítica.
- El service worker cachea únicamente archivos del app shell.

## Buenas prácticas

- No publiques tokens, credenciales ni datos personales en issues o PRs.
- Revisa los cambios de dependencias de GitHub Actions.
- Mantén `actions/checkout`, `actions/setup-*` y las acciones de Pages
  actualizadas.
- Si encuentras contenido inapropiado, repórtalo de forma privada.
