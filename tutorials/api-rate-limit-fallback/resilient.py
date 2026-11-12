"""Ask the model with retry, backoff, jitter and a saved-answer fallback."""
import logging
import random
import time
from dataclasses import dataclass

import anthropic

from prompt import MAX_TOKENS, MODEL

log = logging.getLogger("resilient")

# Errors worth another try: rate limit, server trouble (500 and above, which
# includes 529 overloaded), and network failures. A 400 or 401 will not get
# better by waiting, so those are raised.
RETRYABLE = (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError)


@dataclass
class Answer:
    text: str
    source: str  # "live" or "saved"
    attempts: int


def retry_after_seconds(error):
    """The retry-after header as a number of seconds, or None."""
    response = getattr(error, "response", None)
    value = response.headers.get("retry-after") if response is not None else None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def backoff_delay(attempt, error, *, base=0.5, cap=8.0, rand=random.random):
    """Seconds to wait before the next attempt. `attempt` is 1 for the opening failure.

    If the server sent retry-after, wait that long plus a little jitter.
    Otherwise wait a random time between 0 and base * 2 ** (attempt - 1), capped.
    """
    wait = retry_after_seconds(error)
    if wait is not None:
        return wait + rand() * base
    return rand() * min(cap, base * 2 ** (attempt - 1))


def ask(client, prompt, saved_text, *, max_attempts=4, base=0.5, cap=8.0, max_wait=10.0,
        sleep=time.sleep, rand=random.random):
    """Return an Answer. Falls back to saved_text when the API keeps failing.

    Make the client with max_retries=0, so this function is the only retry layer.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.messages.create(
                model=MODEL, max_tokens=MAX_TOKENS, thinking={"type": "disabled"},
                messages=[{"role": "user", "content": prompt}],
            )
        except RETRYABLE as error:
            status = getattr(error, "status_code", None)
            kind = f"{type(error).__name__} (status {status})" if status else type(error).__name__
            if attempt == max_attempts:
                log.warning("attempt %d of %d failed: %s. Out of attempts, using the saved answer.", attempt, max_attempts, kind)
                break
            server_wait = retry_after_seconds(error)
            if server_wait is not None and server_wait > max_wait:
                log.warning("attempt %d of %d failed: %s. The server asks for %s s, more than %s s. Using the saved answer.",
                            attempt, max_attempts, kind, server_wait, max_wait)
                break
            delay = backoff_delay(attempt, error, base=base, cap=cap, rand=rand)
            header = f"retry-after {server_wait:g} s" if server_wait is not None else "no retry-after header"
            log.warning("retry %d of %d: %s, %s, waiting %.2f s", attempt, max_attempts - 1, kind, header, delay)
            sleep(delay)
        else:
            text = "".join(block.text for block in response.content if block.type == "text")
            return Answer(text, "live", attempt)
    return Answer(saved_text, "saved", attempt)
