from collections.abc import Generator
from typing import NamedTuple

import openai
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker

from src.tokenizer import TokenizerOpenAI

openai_client = openai.OpenAI()


class Chunk(NamedTuple):
    content: str
    source: str


class Chunker:
    def __init__(self, encoding: str, max_tokens_per_chunk: int):
        self.converter = DocumentConverter()
        self.tokenizer = TokenizerOpenAI(encoding, max_tokens_per_chunk)
        self.chunker = HybridChunker(tokenizer=self.tokenizer)

    def get_chunks(self, src: str) -> Generator[Chunk]:
        for content in self._get_chunks(src):
            yield Chunk(content, src)

    def _get_chunks(self, src: str) -> Generator[str]:
        res = self.converter.convert(src)
        chunk_iter = self.chunker.chunk(res.document)
        for chunk in chunk_iter:
            yield chunk.text
