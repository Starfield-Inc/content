// Send three bad requests to the running server and print what the browser would get.
const base = "http://127.0.0.1:8111";
async function post(label, body) {
  const res = await fetch(base + "/api/ask", { method: "POST", headers: { "content-type": "application/json" }, body });
  console.log(`${label}: ${res.status} ${await res.text()}`);
}
await post("empty question ", JSON.stringify({ question: "   " }));
await post("question too long", JSON.stringify({ question: "x".repeat(501) }));
await post("not JSON       ", "this is not json");
