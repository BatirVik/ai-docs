import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

TEST = "pytest" in sys.modules
ENV_FILENAME = ".env.test" if TEST else ".env"
ENV_PATH = Path(__file__).parent.parent / ENV_FILENAME


class Config(BaseSettings):
    OPENAI_API_KEY: str
    LOGFIRE_TOKEN: str

    CHROMADB_PATH: Path = Path(__file__).parent.parent / ".chromadb"

    ENCODING: str = "o200k_base"
    MAX_TOKENS_PER_CHUNK: int = 10_000
    CHUNKS_COUNT: int = 10

    model_config = SettingsConfigDict(env_file=ENV_PATH)


config = Config()  # type: ignore
