// Look for the key, and for the variable name, in everything the browser can download.
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const key = process.env.ANTHROPIC_API_KEY;
if (!key) {
  console.error("ANTHROPIC_API_KEY is not set, so there is nothing to look for.");
  process.exit(1);
}

function files(dir) {
  return readdirSync(dir).flatMap((name) => {
    const p = join(dir, name);
    return statSync(p).isDirectory() ? files(p) : [p];
  });
}

const found = files(".next/static");
let keyHits = 0;
let nameHits = 0;
for (const f of found) {
  const text = readFileSync(f, "utf8");
  if (text.includes(key)) keyHits += 1;
  if (text.includes("ANTHROPIC_API_KEY")) nameHits += 1;
}
console.log(`files the browser can download (.next/static): ${found.length}`);
console.log(`files containing the key value: ${keyHits}`);
console.log(`files containing the name ANTHROPIC_API_KEY: ${nameHits}`);
process.exit(keyHits === 0 && nameHits === 0 ? 0 : 1);
