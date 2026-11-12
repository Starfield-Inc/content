import os
import sys

from anthropic import Anthropic

MODEL = "claude-haiku-5-5"


def build_prompt(topic):
    return f"Write one short, friendly sentence that welcomes a beginner to {topic}."


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set. Add it to a .env file or export it first.")

    topic = sys.argv[1] if len(sys.argv) > 1 else "Python in Visual Studio Code"
    prompt = build_prompt(topic)

    client = Anthropic()
    response = client.messages.create(
        model=MODEL,
        max_tokens=100,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(block.text for block in response.content if block.type == "text").strip()

    print(f"Prompt: {prompt}")
    print(f"Reply:  {text}")
    print(f"[tokens used: {response.usage.input_tokens} in, {response.usage.output_tokens} out]")


if __name__ == "__main__":
    main()
