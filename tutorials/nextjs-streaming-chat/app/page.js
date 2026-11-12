"use client";

import { useEffect, useRef, useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const controllerRef = useRef(null);
  const historyRef = useRef([]);
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ block: "end" });
  }, [messages]);

  // Send `history` (ending with a user message) and stream the answer into a new assistant message.
  async function run(history) {
    historyRef.current = history;
    const controller = new AbortController();
    controllerRef.current = controller;
    setError(null);
    setBusy(true);
    setMessages([...history, { role: "assistant", content: "" }]);
    let answer = "";
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ messages: history.map(({ role, content }) => ({ role, content })) }),
        signal: controller.signal,
      });
      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.error ?? `The request failed (status ${res.status}).`);
      }
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        answer += decoder.decode(value, { stream: true });
        setMessages([...history, { role: "assistant", content: answer }]);
      }
    } catch (err) {
      if (err.name === "AbortError") {
        // Stop pressed: keep what arrived, and mark it.
        setMessages(answer ? [...history, { role: "assistant", content: answer, stopped: true }] : history);
      } else {
        setError(answer ? "The answer was cut off. " + err.message : err.message);
        setMessages(answer ? [...history, { role: "assistant", content: answer }] : history);
      }
    } finally {
      setBusy(false);
      controllerRef.current = null;
    }
  }

  function send(event) {
    event.preventDefault();
    const text = input.trim();
    if (!text || busy) return;
    setInput("");
    run([...messages.filter((m) => m.content), { role: "user", content: text }]);
  }

  return (
    <main>
      <h1>Streaming chat</h1>
      <div id="log" aria-live="polite">
        {messages.length === 0 && <p className="hint">Ask a question to start.</p>}
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.role}`}>
            <span className="who">{m.role === "user" ? "You" : "Assistant"}</span>
            <p>
              {m.content || "..."}
              {m.stopped && <em className="tag"> [stopped]</em>}
            </p>
          </div>
        ))}
        <div ref={endRef} />
      </div>
      {error && (
        <div id="error" role="alert">
          <span>{error}</span>
          <button id="retry" type="button" onClick={() => run(historyRef.current)} disabled={busy}>
            Try again
          </button>
        </div>
      )}
      <form onSubmit={send}>
        <input
          id="input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message"
          maxLength={2000}
          autoComplete="off"
        />
        {busy ? (
          <button id="stop" type="button" onClick={() => controllerRef.current?.abort()}>
            Stop
          </button>
        ) : (
          <button id="send" type="submit" disabled={!input.trim()}>
            Send
          </button>
        )}
      </form>
    </main>
  );
}
