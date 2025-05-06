from typing import Annotated

import typer
from rich.progress import Progress, SpinnerColumn, TextColumn

from src.chunker import Chunker
from src.config import config
from src.repositories import DocumentRepository

from .options import NameSpaceOption

app = typer.Typer(name="knowledge")


@app.command()
def add(
    namespace: NameSpaceOption,
    sources: Annotated[list[str], typer.Argument()],
) -> None:
    chunker = Chunker(config.ENCODING, config.MAX_TOKENS_PER_CHUNK)

    progress = Progress(
        SpinnerColumn(style=typer.colors.CYAN),
        TextColumn("[progress.description]{task.description}", typer.colors.CYAN),
        transient=True,
    )

    docs_repo = DocumentRepository.connect(config.CHROMADB_PATH, namespace)

    with progress:
        for src in sources:
            task = progress.add_task(src)
            for chunk in chunker.get_chunks(src):
                docs_repo.add(chunk.content, src=src)
            progress.remove_task(task)


@app.command()
def ls(namespace: NameSpaceOption) -> None:
    docs_repo = DocumentRepository.connect(config.CHROMADB_PATH, namespace)
    for src in docs_repo.get_all_sources():
        typer.echo(src)
