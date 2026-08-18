from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError, APIStatusError
import os
import sys
import dotenv

dotenv.load_dotenv()

# Provider config — swap via env vars, no code changes needed
PROVIDER_CONFIGS = {
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "api_key_env": "GROQ_API_KEY",
        "default_model": "openai/gpt-oss-120b",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "api_key_env": None,  # Ollama doesn't need a real key
        "default_model": "gemma3:1b",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "api_key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
    },
}

PROVIDER = os.environ.get("AICLI_PROVIDER", "groq")
MODEL = os.environ.get("AICLI_MODEL")  # optional override

if PROVIDER not in PROVIDER_CONFIGS:
    print(f"Unknown provider '{PROVIDER}'. Choose from: {', '.join(PROVIDER_CONFIGS)}")
    sys.exit(1)

config = PROVIDER_CONFIGS[PROVIDER]
model = MODEL or config["default_model"]

api_key = "ollama"  # dummy value, Ollama ignores it
if config["api_key_env"]:
    api_key = os.environ.get(config["api_key_env"])
    if not api_key:
        print(f"Missing {config['api_key_env']} in environment. Add it to your .env file.")
        sys.exit(1)

client = OpenAI(
    base_url=config["base_url"],
    api_key=api_key,
)


def ask(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content

    except AuthenticationError:
        print(f"Authentication failed for {PROVIDER}. Check your API key.")
        sys.exit(1)
    except RateLimitError:
        print(f"Rate limit hit on {PROVIDER}. Wait a bit and try again.")
        sys.exit(1)
    except APIConnectionError:
        print(f"Couldn't reach {PROVIDER} at {config['base_url']}. Is it running / are you online?")
        sys.exit(1)
    except APIStatusError as e:
        print(f"{PROVIDER} returned an error: {e.status_code} — {e.message}")
        sys.exit(1)