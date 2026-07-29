import subprocess
import typer
from rich.console import Console
from aicli.ai import ask

console = Console()


def commit_command():
    # Get currently staged changes
    diff = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True
    ).stdout

    if not diff:
        console.print("[yellow]No staged changes found. Did you run `git add`?[/yellow]")
        return

    prompt = f"""
You are a senior developer.

Generate a concise Git commit message for this diff.

Follow Conventional Commits format:
<type>: <description>

Only output the commit message.

Diff:
{diff}
"""

    console.print("[cyan]Generating commit message...[/cyan]")

    message = ask(prompt).strip()

    console.print("\n[green]Suggested commit:[/green]")
    console.print(message)

    if typer.confirm("\nUse this commit message?"):
        subprocess.run(["git", "commit", "-m", message])
        console.print("[green]Committed.[/green]")
    else:
        console.print("[yellow]Skipped — no commit made.[/yellow]")