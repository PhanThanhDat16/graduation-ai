from langchain_openai import ChatOpenAI
from src.core.config import settings


def langchain_ChatOpenAI(**kwargs):
    return ChatOpenAI(api_key=settings.OPENAI_API_KEY, **kwargs)