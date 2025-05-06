import os

import tiktoken
from docling_core.transforms.chunker.tokenizer.base import BaseTokenizer

os.environ["TOKENIZERS_PARALLELISM"] = "0"


class TokenizerOpenAI(BaseTokenizer):
    def __init__(self, encoding: str, max_tokens: int):
        self._enc = tiktoken.get_encoding(encoding)
        self._max_tokens = max_tokens

    def count_tokens(self, text: str) -> int:
        return len(self._enc.encode(text))

    def get_max_tokens(self) -> int:
        return self._max_tokens

    def get_tokenizer(self):
        return self._enc
