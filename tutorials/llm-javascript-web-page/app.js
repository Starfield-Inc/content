// Browser code. It talks to our own server at /api/ask. There is no key anywhere in this file.
const box = document.getElementById("question");
const button = document.getElementById("send");
const answerEl = document.getElementById("answer");
const errorEl = document.getElementById("error");
const metaEl = document.getElementById("meta");

async function ask() {
  errorEl.hidden = true;
  answerEl.hidden = true;
  metaEl.textContent = "";
  button.disabled = true;
  try {
    const res = await fetch("/api/ask", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ question: box.value }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
    answerEl.textContent = data.answer;
    answerEl.hidden = false;
    metaEl.textContent = `Input tokens: ${data.usage.input_tokens}. Output tokens: ${data.usage.output_tokens}.`;
  } catch (err) {
    errorEl.textContent = err.message;
    errorEl.hidden = false;
  } finally {
    button.disabled = false;
  }
}

button.addEventListener("click", ask);

// Optional: /?ask=... fills the box and asks once, so a run can be repeated without typing.
const preset = new URLSearchParams(location.search).get("ask");
if (preset) {
  // Only for the screenshot run: a script the server answers after 6 seconds keeps the page
  // "loading", so a tool that captures the page at load time sees the answer.
  document.head.append(Object.assign(document.createElement("script"), { src: "/hold.js" }));
  box.value = preset;
  ask();
}
