from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from src.core.config import settings


def langchain_ChatOpenAI(**kwargs):
    return ChatOpenAI(api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_MODEL, **kwargs)


def langchain_OpenAIEmbeddings(**kwargs):
    return OpenAIEmbeddings(
        api_key=settings.OPENAI_API_KEY, model=settings.OPENAI_EMBEDDING_MODEL, **kwargs
    )