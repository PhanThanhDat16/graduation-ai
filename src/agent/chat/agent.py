import logging
from typing import TypedDict

from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.chat.tools import ALL_TOOLS
from src.integrations.open_ai import langchain_ChatOpenAI
from src.agent.chat.prompt import build_system_prompt
from src.integrations.backend_client import fetch_messages, post_ai_message
from src.agent.detect_language import detect_language

logger = logging.getLogger(__name__)


# ==================== Context Schema ====================
class AgentContext(TypedDict):
    """Context passed to the agent on each invocation (not persisted in state)."""

    language: str


# ==================== Agent Setup ====================

model = langchain_ChatOpenAI(temperature=0.7)
checkpointer = InMemorySaver()

chat_agent = create_agent(
    model=model,
    tools=ALL_TOOLS,
    middleware=[build_system_prompt],
    state_schema=AgentState,
    context_schema=AgentContext,
    checkpointer=checkpointer,
)


# ==================== Agent Invocation ====================
async def chat_with_assistant(
    message: str,
    group_id: str,
    user_id: str,
    user_type: str = "freelancer",
) -> str:
    """Process a chat message using the create_agent-based agent.

    Flow:
    1. Fetch last 10 messages from backend API for conversation context
    2. Detect user language via lightweight LLM call
    3. Invoke agent with language passed through context_schema
    4. Post the AI response back to the backend API

    Args:
        message: User message text
        group_id: Conversation/group ObjectId from main chat system
        user_id: Backend User ObjectId string
        user_type: "freelancer" or "contractor"

    Returns:
        Assistant response text
    """
    # 1. Fetch recent messages for context
    history_messages = []
    recent_messages = await fetch_messages(group_id, limit=10)
    if recent_messages:
        for msg in recent_messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if content:
                history_messages.append({"role": role, "content": content})

    # 2. Add current user message
    all_messages = history_messages + [{"role": "user", "content": message}]

    # 3. Detect language from the user's latest message
    detected_lang = await detect_language(message)

    # 4. Invoke agent with language in context
    result = await chat_agent.ainvoke(
        {"messages": all_messages},
        config={"configurable": {"thread_id": group_id}},
        context={"language": detected_lang},
    )

    # 5. Extract assistant response
    assistant_text = result["messages"][-1].content or ""

    # 6. Post AI response back to backend API
    await post_ai_message(group_id, assistant_text)
    return assistant_text
