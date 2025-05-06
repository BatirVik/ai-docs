#!/usr/bin/env -S uv run --script
import logfire

from src.cli import app
from src.config import config

if __name__ == "__main__":
    logfire.configure(token=config.LOGFIRE_TOKEN, console=False)
    app()
