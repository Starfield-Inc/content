// A small server. It holds the key, serves the page, and exposes one endpoint: POST /api/ask.
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";

const MODEL = process.env.MODEL || "claude-haiku-5-5";
const PORT = Number(process.env.PORT || 8111);
const MAX_QUESTION = 500;

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("ANTHROPIC_API_KEY is not set. Export it or start Node with --env-file=.env.");
  process.exit(1);
}

const FILES = {
  "/": ["index.html", "text/html; charset=utf-8"],
  "/app.js": ["app.js", "text/javascript; charset=utf-8"],
};

function send(res, status, body, type = "application/json") {
  res.writeHead(status, { "content-type": type });
  res.end(typeof body === "string" ? body : JSON.stringify(body));
}

async function readJson(req) {
  let raw = "";
  for await (const chunk of req) {
    raw += chunk;
    if (raw.length > 10_000) throw new Error("body too large");
  }
  return JSON.parse(raw || "{}");
}

async function ask(question) {
  const upstream = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": apiKey, // only the server ever sees this
      "anthropic-version": "2023-06-01",
    },
    body: JSON.stringify({
      model: MODEL,
      max_tokens: 200,
      messages: [{ role: "user", content: question }],
    }),
  });
  const data = await upstream.json();
  return { upstream, data };
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, "http://localhost");

  if (req.method === "GET" && FILES[url.pathname]) {
    const [file, type] = FILES[url.pathname];
    return send(res, 200, await readFile(new URL(file, import.meta.url), "utf8"), type);
  }

  if (req.method === "GET" && url.pathname === "/hold.js") {
    // Only used by the screenshot run, see app.js.
    return setTimeout(() => send(res, 200, "", "text/javascript"), 6000);
  }

  if (req.method === "POST" && url.pathname === "/api/ask") {
    let question;
    try {
      question = String((await readJson(req)).question ?? "").trim();
    } catch {
      return send(res, 400, { error: "Send JSON like {\"question\": \"...\"}." });
    }
    if (!question) return send(res, 400, { error: "The question is empty." });
    if (question.length > MAX_QUESTION) {
      return send(res, 400, { error: `The question is longer than ${MAX_QUESTION} characters.` });
    }
    try {
      const { upstream, data } = await ask(question);
      if (!upstream.ok) {
        // Log the detail on the server. Tell the browser only what it needs.
        console.error(`upstream ${upstream.status}: ${data.error?.message}`);
        return send(res, 502, { error: "The model service returned an error. Try again later." });
      }
      const answer = data.content.filter((b) => b.type === "text").map((b) => b.text).join("");
      return send(res, 200, { answer, usage: data.usage });
    } catch (err) {
      console.error("request failed:", err.message);
      return send(res, 502, { error: "Could not reach the model service." });
    }
  }

  send(res, 404, { error: "Not found." });
});

server.listen(PORT, "127.0.0.1", () => console.log(`listening on http://127.0.0.1:${PORT}`));
