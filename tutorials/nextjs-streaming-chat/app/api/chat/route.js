import Anthropic from "@anthropic-ai/sdk";

const MODEL = "claude-haiku-5-5";
const MAX_TOKENS = 300;
const MAX_MESSAGES = 20;
const MAX_CHARS = 2000;

function fail(status, message) {
  return Response.json({ error: message }, { status });
}

// Check the body at the edge: the browser is not trusted.
function parseMessages(body) {
  const list = body?.messages;
  if (!Array.isArray(list) || list.length === 0 || list.length > MAX_MESSAGES) return null;
  for (const m of list) {
    if (m?.role !== "user" && m?.role !== "assistant") return null;
    if (typeof m.content !== "string" || m.content.length === 0 || m.content.length > MAX_CHARS) return null;
  }
  if (list[0].role !== "user" || list.at(-1).role !== "user") return null;
  return list.map(({ role, content }) => ({ role, content }));
}

export async function POST(request) {
  // The key is read here, on the server. It is never sent to the browser.
  if (!process.env.ANTHROPIC_API_KEY) {
    return fail(500, "ANTHROPIC_API_KEY is not set on the server.");
  }
  const messages = parseMessages(await request.json().catch(() => null));
  if (!messages) return fail(400, "Send 1 to 20 messages that start and end with a user message.");

  const upstream = new AbortController();
  request.signal.addEventListener("abort", () => upstream.abort());

  const client = new Anthropic();
  let events;
  try {
    // The call resolves once the API has accepted the request, so a bad key or a
    // bad request fails here, before any bytes are streamed.
    events = await client.messages.create(
      { model: MODEL, max_tokens: MAX_TOKENS, thinking: { type: "disabled" }, messages, stream: true },
      { signal: upstream.signal },
    );
  } catch (err) {
    if (upstream.signal.aborted) return new Response(null, { status: 499 });
    if (err instanceof Anthropic.APIError) {
      console.log(`api error: status ${err.status}`);
      return fail(502, `The model call failed (status ${err.status}).`);
    }
    throw err;
  }

  const encoder = new TextEncoder();
  let chunks = 0;
  const body = new ReadableStream({
    async start(controller) {
      try {
        for await (const event of events) {
          if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
            controller.enqueue(encoder.encode(event.delta.text));
            chunks += 1;
          } else if (event.type === "message_delta") {
            console.log(`done: ${chunks} chunks, output tokens ${event.usage.output_tokens}`);
          }
        }
        controller.close();
      } catch (err) {
        if (upstream.signal.aborted) return;
        console.log(`stream error after ${chunks} chunks`);
        controller.error(err);
      }
    },
    cancel() {
      // The browser went away or the user pressed Stop. Close the call to the API too.
      console.log(`client left after ${chunks} chunks, upstream request aborted`);
      upstream.abort();
    },
  });

  return new Response(body, { headers: { "content-type": "text/plain; charset=utf-8", "cache-control": "no-store" } });
}
