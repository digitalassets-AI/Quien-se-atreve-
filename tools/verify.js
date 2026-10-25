#!/usr/bin/env node
/**
 * Verifica el contenido final de app/index.html: nodos, conteos y duplicados.
 *
 * Uso:
 *   node tools/verify.js
 */
const fs = require("fs");
const path = require("path");

const ROOT = path.resolve(__dirname, "..");
const APP = path.join(ROOT, "app");
const EXPECTED = {
  "familia/primos": 16,
  "familia/familia": 16,
  "amigos/panas": 400,
  "amigos/mejores_amigos": 400,
  "amigos/amigos_hot": 600,
  "pareja/conocerse": 400,
  "pareja/conocerse_fondo": 400,
  "pareja/pareja_hot": 800,
  "universidad/companeros": 400,
  "universidad/amigos_u": 400,
  "universidad/universidad_hot": 600,
};

const errors = [];
function check(condition, message) {
  if (!condition) {
    errors.push(message);
    console.log(`  ✗ ${message}`);
  }
}

const html = fs.readFileSync(path.join(APP, "index.html"), "utf8");
const start = html.indexOf("const challenges = {");
const end = html.indexOf("\n};", start);

check(start !== -1, "No se encontró el objeto challenges");
check(end !== -1, "No se encontró el cierre del objeto challenges");

if (start === -1 || end === -1) {
  process.exit(1);
}

const source = html.slice(start + "const challenges = ".length, end + 2);
let challenges;
try {
  challenges = new Function(`return (${source});`)();
} catch (error) {
  console.error("No se pudo evaluar challenges:", error.message);
  process.exit(1);
}

const seen = new Map();
const perNode = {};
let total = 0;
let preguntas = 0;
let retos = 0;

for (const [categoria, subcategorias] of Object.entries(challenges)) {
  for (const [subcategoria, nodo] of Object.entries(subcategorias)) {
    const key = `${categoria}/${subcategoria}`;
    const questions = Array.isArray(nodo.questions) ? nodo.questions : [];
    const actions = Array.isArray(nodo.actions) ? nodo.actions : [];
    perNode[key] = questions.length + actions.length;
    preguntas += questions.length;
    retos += actions.length;
    total += questions.length + actions.length;

    check(
      perNode[key] === EXPECTED[key],
      `${key}: ${perNode[key]} ítems (esperados ${EXPECTED[key]})`
    );

    for (const item of [...questions, ...actions]) {
      const text = Array.isArray(item) ? item[0] : item;
      check(typeof text === "string" && text.trim().length > 0, `${key}: ítem vacío o inválido`);
      if (typeof text !== "string") continue;

      if (Array.isArray(item)) {
        check(
          item.length === 3 && item.every((part) => typeof part === "string" && part.trim()),
          `${key}: variante de género incompleta`
        );
      }

      if (seen.has(text)) {
        errors.push(`Texto repetido: "${text.slice(0, 70)}" (${seen.get(text)} y ${key})`);
      } else {
        seen.set(text, key);
      }
    }
  }
}

const expectedNodes = Object.keys(EXPECTED).sort();
const actualNodes = Object.keys(perNode).sort();
check(
  JSON.stringify(actualNodes) === JSON.stringify(expectedNodes),
  `Nodos inesperados o faltantes: ${actualNodes.filter((n) => !expectedNodes.includes(n)).join(", ") || "ninguno"}`
);

check(total === 4432, `Total final: ${total} (esperados 4432)`);
check(seen.size === total, `Textos únicos: ${seen.size} de ${total}`);
check(preguntas === 2218, `Preguntas: ${preguntas} (esperadas 2218)`);
check(retos === 2214, `Retos: ${retos} (esperados 2214)`);

console.log("Contenido de app/index.html");
for (const [key, count] of Object.entries(perNode)) {
  console.log(`  · ${key}: ${count}`);
}
console.log(`  · Total: ${total} (${preguntas} preguntas + ${retos} retos)`);
console.log(`  · Únicos: ${seen.size}`);

if (errors.length) {
  console.error(`\n❌ ${errors.length} error(es)`);
  process.exit(1);
}
console.log("\n✅ Contenido final correcto: 4.432 ítems, 0 duplicados");
