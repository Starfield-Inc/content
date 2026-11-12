from app.settings import load_env


def main():
    settings = load_env()
    if not settings:
        print("No .env file found. Run: cp .env.example .env")
        raise SystemExit(1)
    print(f"Team: {settings.get('TEAM_NAME', '(not set)')}")
    # Say whether the key is there. Never print it.
    print("API_KEY: set (hidden)" if settings.get("API_KEY") else "API_KEY: missing")


if __name__ == "__main__":
    main()
