from pathlib import Path
from typing import Annotated

import typer
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.chat import Chat
from src.config import config
from src.repositories import DocumentRepository

from .options import NameSpaceOption

app = typer.Typer()


@app.command("chat")
def chat_shell(
    namespace: NameSpaceOption,
    instructions: Annotated[Path | None, typer.Option("--instructions", "-i")] = None,
) -> None:
    if instructions:
        user_inst = instructions.read_text()
    else:
        user_inst = None
    docs_repo = DocumentRepository.connect(config.CHROMADB_PATH, namespace)
    chat = Chat(docs_repo, config.CHUNKS_COUNT, user_inst)

    session = PromptSession("\n> ", history=InMemoryHistory())

    typer.echo("🚀 Starting chat. Type 'exit' to quit.")
    while True:
        try:
            user_prompt = session.prompt()
        except (KeyboardInterrupt, EOFError):
            # Ctrl-C or Ctrl-D
            typer.echo("\n👋 Goodbye!")
            raise typer.Exit
        if user_prompt.strip().lower() in {"exit", "quit", ":q"}:
            typer.echo("👋 Goodbye!")
            raise typer.Exit

        with Progress(
            SpinnerColumn(style=typer.colors.CYAN),
            TextColumn("[progress.description]{task.description}", typer.colors.CYAN),
            transient=True,
        ) as progress:
            progress.add_task("Thinking ...", total=None)
            answer = chat.get_answer_or_exc(user_prompt)

        if isinstance(answer, Exception):
            typer.secho(
                f"Something went wrong, please try again! [{type(answer).__name__}]",
                fg=typer.colors.RED,
            )
        else:
            typer.secho(answer, fg=typer.colors.GREEN)
