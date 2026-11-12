"""Three-role pipeline with CrewAI: researcher -> writer -> reviewer."""
import os
import sys

# Check the key first. CrewAI reads a .env file on import, so checking afterwards
# would hide a key that is missing from your shell.
if not os.environ.get("ANTHROPIC_API_KEY"):
    sys.exit("ANTHROPIC_API_KEY is not set. Export it or load your .env first.")

# Opt out of telemetry before crewai is imported.
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("CREWAI_DISABLE_TRACKING", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from crewai import Agent, Crew, LLM, Process, Task

TOPIC = "keeping an API key out of a public git repository"

llm = LLM(model="anthropic/claude-haiku-5-5", max_tokens=500)


def agent(role, goal):
    return Agent(role=role, goal=goal, backstory=f"You are the {role} on a small team.",
                 llm=llm, allow_delegation=False, max_iter=2, verbose=False)


researcher = agent("researcher", "List accurate points about a topic")
writer = agent("writer", "Turn research notes into a short, clear note")
reviewer = agent("reviewer", "Check a draft against the research notes")

research = Task(description=f"List 4 short factual points about {TOPIC}. One line each.",
                expected_output="A numbered list of 4 lines.", agent=researcher)
draft = Task(description="Write a note of at most 80 words from the research points.",
             expected_output="One paragraph, at most 80 words.", agent=writer, context=[research])
review = Task(description="Compare the draft with the research points. Start with APPROVE or REVISE, "
              "then give one sentence of reasons.",
              expected_output="APPROVE or REVISE, then one sentence.", agent=reviewer,
              context=[research, draft])

crew = Crew(agents=[researcher, writer, reviewer], tasks=[research, draft, review],
            process=Process.sequential, verbose=False)
result = crew.kickoff()

for name, task in (("researcher", research), ("writer", draft), ("reviewer", review)):
    print(f"--- {name} ---\n{task.output.raw}\n")
usage = result.token_usage
print(f"[calls: {usage.successful_requests}, tokens: input {usage.prompt_tokens}, output {usage.completion_tokens}]")
