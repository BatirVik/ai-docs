from dataclasses import dataclass

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from src.config import config

model = OpenAIModel(
    "gpt-4.1-mini", provider=OpenAIProvider(api_key=config.OPENAI_API_KEY)
)


@dataclass
class AppDeps:
    user_inst: str | None
    docs: list[str] | None
    namespace: str


agent = Agent(
    model,
    deps_type=AppDeps,
    instrument=True,
    system_prompt="""
    You are helpful assistant available through cli, you have access to specific documents.
    """,
)


@agent.system_prompt
def user_instructions(ctx: RunContext[AppDeps]) -> str:
    if ctx.deps.user_inst is None:
        return "User didn't provide any custom instructions."
    return f"""
    User provided custom instructions:
    ----------------------------------
    {ctx.deps.user_inst}       
    """


@agent.system_prompt
def documents_context(ctx: RunContext[AppDeps]) -> str:
    if ctx.deps.docs is None:
        return "No relevant documents provided."
    return f"""
    Most relevant documents from the knowledge base from '{ctx.deps.namespace}' namespace:
    ----------------------------------
    {ctx.deps.docs}
    """
