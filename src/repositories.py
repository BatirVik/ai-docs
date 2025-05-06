from os import PathLike
from typing import Self
from uuid import uuid4

from chromadb import Collection, PersistentClient

type StrPath = str | PathLike[str]


class DocumentRepository:
    def __init__(self, collection: Collection, namespace: str):
        self.cl = collection
        self.namespace = namespace

    @classmethod
    def connect(cls, path: StrPath, namespace: str) -> Self:
        client = PersistentClient(str(path))
        collection = client.get_or_create_collection(namespace)
        return cls(collection, namespace)

    def add(self, document: str, *, src: str = "unknown") -> None:
        doc_id = str(uuid4())
        self.cl.add(
            doc_id,
            documents=document,
            metadatas={"version": 1, "src": src},
        )

    def search(self, query: str, limit: int) -> list[str] | None:
        res = self.cl.query(query_texts=query, n_results=limit, include=["documents"])
        docs = res["documents"]
        if docs is None:
            return None
        return docs[0]

    def get_all_sources(self) -> set[str]:
        result = self.cl.get(include=["metadatas"])
        if result["metadatas"] is None:
            return set()
        return {str(metadata["src"]) for metadata in result["metadatas"]}
