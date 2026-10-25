# Contribuir a ¿Quién se atreve?

Gracias por querer mejorar el proyecto. Antes de abrir un Pull Request, revisa
estas reglas.

## Modelo de ramas

| Rama | Uso |
|---|---|
| `main` | Producción. Solo recibe merges de `release/*` o `hotfix/*`. |
| `develop` | Integración. Recibe features y fixes. |
| `feature/<nombre>` | Nueva función o contenido. Nace de `develop`. |
| `fix/<nombre>` | Corrección no urgente. Nace de `develop`. |
| `release/<version>` | Preparación de una versión. Nace de `develop`. |
| `hotfix/<nombre>` | Urgencia. Nace de `main`. |

## Pasos para un cambio

```bash
git switch develop
git pull origin develop
git switch -c feature/mi-cambio

# hacer cambios
python3 tools/build.py
python3 tools/verify.py
node tools/verify.js

git add .
git commit -m "feat(area): describir el cambio"
git push -u origin feature/mi-cambio
```

Abre un Pull Request hacia `develop`. No hagas merge directo a `main`.

## Convención de commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/es/):

```text
feat(contenido): agregar 40 retos de oficina
fix(android): corregir la orientación de la pantalla de inicio
docs(readme): documentar el flujo de ramas
chore(deps): actualizar acciones de GitHub
ci: verificar el contenido en cada PR
```

## Cambios de contenido

Los textos viven en CSV editables:

- `data/hot/{juego}_n{nivel}.csv` → columnas `juego,nivel,tipo,texto` y campos
  opcionales `genero,texto_hombre,texto_mujer,significado`.
- `data/extra/<nodo>.csv` → columnas `tipo,texto`.
- `data/glosario.csv` → `termino,definicion,categoria,ejemplo`.

Reglas editoriales:

- Español latinoamericano neutro; evita españolismos y regionalismos de un solo
  país.
- Tono adulto y picante, sin contenido pornográfico explícito.
- Preguntas con lógica y palabras poco comunes entre paréntesis.
- No repetir textos entre nodos.
- Respeto y consentimiento siempre presentes.

Después de editar:

```bash
python3 tools/build.py
python3 tools/verify.py
node tools/verify.js
```

## Estilo de código

- Python: biblioteca estándar, funciones pequeñas y mensajes en español.
- JavaScript: vanilla, sin frameworks de runtime. Capacitor solo se usa para
  empaquetar el APK.
- HTML/CSS: mantener la estética y las variables CSS existentes.
- No agregar analítica, cookies, backend ni servicios externos.
- No versionar `android/`, `android-assets/`, APK, keystores ni contraseñas.

## Checklist del Pull Request

- [ ] El cambio nace de `develop` (o de `main` si es `hotfix/*`).
- [ ] `python3 tools/build.py` se ejecutó.
- [ ] `python3 tools/verify.py` pasa.
- [ ] `node tools/verify.js` pasa.
- [ ] Probé el flujo en la vista web y, si toqué el empaquetado, compilé el
      APK con `./gradlew assembleDebug`.
- [ ] No incluí tokens, credenciales, keystores ni datos personales.
- [ ] Actualicé `CHANGELOG.md` y `package.json` si corresponde.

## Reportar problemas

Usa las plantillas de issues. Para vulnerabilidades, sigue
[`SECURITY.md`](SECURITY.md).
