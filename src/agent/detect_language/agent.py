from langchain_core.messages import HumanMessage, SystemMessage
import logging
from src.integrations.open_ai import langchain_ChatOpenAI

logger = logging.getLogger(__name__)


# ==================== Language Detection ====================
lang_detect_model = langchain_ChatOpenAI(temperature=0, max_tokens=20)

LANG_DETECT_PROMPT = """Detect the language of the following text.
Respond with ONLY the language name in English (e.g. "Vietnamese", "English", "Japanese").
Do not add any explanation.

Text: {text}"""


async def detect_language(text: str) -> str:
    """Detect the language of the given text using a lightweight LLM call."""
    try:
        response = await lang_detect_model.ainvoke(
            [
                SystemMessage(
                    content="You are a language detector. Respond with only the language name."
                ),
                HumanMessage(content=LANG_DETECT_PROMPT.format(text=text)),
            ]
        )

        detected = response.content.strip()
        logger.info(f"Detected language: {detected}")
        return detected or "English"
    except Exception as e:
        logger.warning(f"Language detection failed: {e}, defaulting to English")
        return "English"
