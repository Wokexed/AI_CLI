from aicli.ai import ask


def ask_command(prompt: str):
    response = ask(prompt)

    print("\nAI:")
    print(response)
