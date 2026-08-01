from rag.policy_rag import lookup_policy as _lookup_policy
from livekit.agents import function_tool


@function_tool
async def lookup_policy(question: str) -> str:
    """Retrieve answers from local delivery, returns, refund, flower-care, or FAQ policy."""
    return _lookup_policy(question)
