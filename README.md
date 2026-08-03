# aicli

A personal command-line AI assistant. Chat with a model, ask one-off questions, or auto-generate a commit message from your staged git changes — all from the terminal, in any repo.

## Features

- **`aicli chat "<prompt>"`** — send a prompt, get a response
- **`aicli ask "<prompt>"`** — same as chat, formatted as a quick Q&A
- **`aicli commit`** — reads your staged git diff, generates a Conventional Commits–style message, and (with confirmation) commits for you
- Swappable AI provider (Groq, Ollama, OpenAI) via a single environment variable — no code changes needed
- Clean error handling for bad keys, rate limits, and connection issues

## Requirements

- Python 3.12+
- A [Groq](https://console.groq.com) API key (free tier) — the default provider
  - Alternatively: [Ollama](https://ollama.com) running locally, or an OpenAI API key

## Installation

Clone the repo and install it in editable mode so the `aicli` command is available globally:

```bash
git clone https://github.com/Wokexed/AI_CLI.git
cd AI_CLI
pip install -e .
```

> **Note:** if you move or rename this folder after installing, you'll need to re-run `pip install -e . --force-reinstall --no-deps` from the new location — editable installs are tied to the folder path.

## Configuration

Create a `.env` file in the project root (see `.env.example`):

```
GROQ_API_KEY=your-groq-key-here
```

Get a free key at [console.groq.com](https://console.groq.com) → API Keys.

### Switching providers

By default, `aicli` uses Groq. To use a different provider, set `AICLI_PROVIDER` in your `.env` file or shell session:

```
AICLI_PROVIDER=ollama
```

Supported values: `groq` (default), `ollama`, `openai`

Each provider needs its own key in `.env` (except Ollama, which runs locally and needs no key — just make sure `ollama serve` is running and you've pulled a model):

```
GROQ_API_KEY=...
OPENAI_API_KEY=...
```

### Overriding the model

Each provider has a sensible default model. To use a different one:

```
AICLI_MODEL=llama-3.1-8b-instant
```

## Usage

```bash
# Chat with the AI
aicli chat "explain what a closure is"

# Quick Q&A
aicli ask "what does this error mean: ModuleNotFoundError"

# Generate a commit message from staged changes
git add .
aicli commit
```

`aicli commit` will show the suggested message and ask for confirmation before actually committing — nothing is committed automatically without your approval.

## Project structure

```
AI_CLI/
├── aicli/
│   ├── __init__.py
│   ├── main.py            # CLI entry point (typer app)
│   ├── ai.py               # provider config + ask()
│   └── commands/
│       ├── __init__.py
│       ├── ask.py
│       └── commit.py
├── pyproject.toml
├── .env                     # local secrets, not committed
└── .env.example
```

## Security note

`.env` is git-ignored and should never be committed. If you rotate your API key, just update the value in `.env` — no code changes needed.
