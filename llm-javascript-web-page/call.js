// Step 1: call the model from Node. The key comes from the environment, not from the code.
const MODEL = process.env.MODEL || "claude-haiku-5-5";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) {
  console.error("ANTHROPIC_API_KEY is not set. Export it or start Node with --env-file=.env.");
  process.exit(1);
}

const response = await fetch("https://api.anthropic.com/v1/messages", {
  method: "POST",
  headers: {
    "content-type": "application/json",
    "x-api-key": apiKey,
    "anthropic-version": "2023-06-01",
  },
  body: JSON.stringify({
    model: MODEL,
    max_tokens: 150,
    messages: [{ role: "user", content: "In one sentence, what is a hackathon?" }],
  }),
});

const data = await response.json();
if (!response.ok) {
  console.error(`The API returned ${response.status}: ${data.error?.message}`);
  process.exit(1);
}

// A reply is a list of blocks. Join the text blocks.
const answer = data.content.filter((b) => b.type === "text").map((b) => b.text).join("");
console.log("model:", data.model);
console.log("answer:", answer);
console.log("input tokens:", data.usage.input_tokens, "output tokens:", data.usage.output_tokens);
