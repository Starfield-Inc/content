// Fetch what a browser would receive and look for the key in it. The key is never printed.
const key = process.env.ANTHROPIC_API_KEY;
if (!key) {
  console.error("ANTHROPIC_API_KEY is not set. Export it or start Node with --env-file=.env.");
  process.exit(1);
}
const base = "http://127.0.0.1:8111";
let leaked = false;
for (const path of ["/", "/app.js"]) {
  const body = await (await fetch(base + path)).text();
  const found = body.includes(key);
  console.log(`GET ${path.padEnd(7)} ${body.length} bytes, contains the key: ${found ? "YES" : "no"}`);
  if (found) leaked = true;
}
const answer = await (await fetch(base + "/api/ask", {
  method: "POST", headers: { "content-type": "application/json" },
  body: JSON.stringify({ question: "Say hello in three words." }),
})).text();
console.log(`POST /api/ask reply contains the key: ${answer.includes(key) ? "YES" : "no"}`);
console.log(leaked ? "LEAK: the key is in the page." : "The key stays on the server.");
process.exit(leaked ? 1 : 0);
