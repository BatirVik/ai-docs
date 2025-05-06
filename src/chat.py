from pydantic_ai.messages import ModelMessage

from src.agent import AppDeps, agent
from src.repositories import DocumentRepository


class Chat:
    def __init__(
        self,
        docs_repo: DocumentRepository,
        docs_limit: int,
        user_inst: str | None = None,
    ) -> None:
        self.docs_repo = docs_repo
        self.docs_limit = docs_limit
        self.user_inst = user_inst
        self.mh: list[ModelMessage] = []

    def get_answer(self, prompt: str) -> str:
        docs = self.docs_repo.search(prompt, self.docs_limit)
        deps = AppDeps(
            docs=docs, namespace=self.docs_repo.namespace, user_inst=self.user_inst
        )
        res = agent.run_sync(prompt, message_history=self.mh, deps=deps)
        self.mh = res.new_messages()
        return res.output

    def get_answer_or_exc(self, prompt: str) -> str | Exception:
        try:
            return self.get_answer(prompt)
        except Exception as e:
            # TODO: add logger
            return e
