// Call the route handler directly and print when each piece of the answer arrives.
// usage: node scripts/call-route.mjs [--bad]
const URL = "http://127.0.0.1:8129/api/chat";
const bad = process.argv.includes("--bad");
const body = bad
  ? { messages: [{ role: "assistant", content: "I start the conversation." }] }
  : { messages: [{ role: "user", content: "In two short sentences, why should a demo show an answer as it is written?" }] };

const start = performance.now();
const res = await fetch(URL, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify(body) });
console.log(`status ${res.status}, content-type ${res.headers.get("content-type")}`);
if (!res.ok) {
  console.log("body:", await res.text());
  process.exit(bad ? 0 : 1);
}
const decoder = new TextDecoder();
let n = 0;
let text = "";
for await (const value of res.body) {
  n += 1;
  const piece = decoder.decode(value, { stream: true });
  text += piece;
  if (n <= 6) console.log(`chunk ${n} at ${Math.round(performance.now() - start)} ms: ${JSON.stringify(piece)}`);
}
console.log(`... ${n} chunks in all, last at ${Math.round(performance.now() - start)} ms`);
console.log("full answer:", text);
process.exit(n > 1 ? 0 : 1);
