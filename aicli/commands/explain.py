import typer
from aicli.ai import ask

app = typer.Typer()

@app.command()
def explain(text: str):
    prompt = f"Explain this clearly:\n\n{text}"
    print(ask(prompt))