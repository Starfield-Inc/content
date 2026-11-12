"""Print the SDK's own retry rules, read from the installed package."""
import inspect

import anthropic
from anthropic import _constants
from anthropic._base_client import BaseClient

print("anthropic version:", anthropic.__version__)
print("DEFAULT_MAX_RETRIES =", _constants.DEFAULT_MAX_RETRIES)
print("INITIAL_RETRY_DELAY =", _constants.INITIAL_RETRY_DELAY)
print("MAX_RETRY_DELAY =", _constants.MAX_RETRY_DELAY)

print("\n_should_retry, the lines that name a header or a status code:")
for line in inspect.getsource(BaseClient._should_retry).splitlines():
    if ("status_code" in line or "x-should-retry" in line) and "log.debug" not in line and "#" not in line:
        print(" ", line.strip())

print("\n_should_retry_exception, the error types it retries:")
for line in inspect.getsource(BaseClient._should_retry_exception).splitlines():
    if "isinstance" in line:
        print(" ", line.strip())

print("\n_calculate_retry_timeout, without comments:")
for line in inspect.getsource(BaseClient._calculate_retry_timeout).splitlines()[7:]:
    if line.strip() and not line.strip().startswith("#"):
        print(" ", line.strip())
