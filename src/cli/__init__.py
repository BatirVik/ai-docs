import typer

from . import chat, knowledge

app = typer.Typer()
app.add_typer(chat.app)
app.add_typer(knowledge.app)
