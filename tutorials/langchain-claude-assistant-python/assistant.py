"""A small personal assistant: prompt template, memory and two local tools."""
import os
import sys
import uuid
from datetime import date

from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import InMemorySaver

from tools import TOOLS

MODEL = os.environ.get("TUTORIAL_MODEL", "claude-haiku-5-5")

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are {assistant_name}, a personal assistant. Today is {today}. "
     "Use the calculator for any arithmetic and read_notes for questions about "
     "the user's notes. Answer in at most two short sentences."),
])


def build_assistant():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Load your .env file first.")
    system = PROMPT.format_messages(assistant_name="Pip", today=date.today().isoformat())[0]
    return create_agent(
        ChatAnthropic(model=MODEL, max_tokens=300),
        TOOLS,
        system_prompt=system,
        checkpointer=InMemorySaver(),
    )


def ask(agent, thread_id, question):
    config = {"configurable": {"thread_id": thread_id}}
    result = agent.invoke({"messages": [HumanMessage(question)]}, config)
    messages = result["messages"]
    # Show only what happened in this turn: everything after the last human message.
    last_human = max(i for i, m in enumerate(messages) if isinstance(m, HumanMessage))
    for m in messages[last_human + 1:]:
        if isinstance(m, AIMessage):
            for call in m.tool_calls:
                print(f"  [tool] {call['name']}({call['args']})")
    print(f"You: {question}")
    print(f"Pip: {messages[-1].text}\n")


if __name__ == "__main__":
    questions = sys.argv[1:] or ["Hello! What can you do?"]
    agent = build_assistant()
    thread = str(uuid.uuid4())[:8]
    print(f"model: {MODEL}  thread: new\n")
    for q in questions:
        ask(agent, thread, q)
