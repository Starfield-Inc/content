"""Show that CrewAI telemetry is switched off by the environment settings."""
import os

os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("CREWAI_DISABLE_TRACKING", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

from crewai.telemetry.telemetry import Telemetry

for name in ("CREWAI_DISABLE_TELEMETRY", "CREWAI_DISABLE_TRACKING", "OTEL_SDK_DISABLED"):
    print(f"{name}={os.environ[name]}")
print("telemetry disabled:", Telemetry._is_telemetry_disabled())
