import typer
from aicli.ai import ask
from aicli.commands.commit import commit_command
from aicli.commands.ask import ask_command

app = typer.Typer()
app.command(name="commit")(commit_command)
app.command(name="ask")(ask_command)

@app.command()
def chat(prompt: str):
    print(ask(prompt))

if __name__ == "__main__":
    app()
