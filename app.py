import chainlit as cl
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


@cl.on_chat_start
async def start():
    await cl.Message(content="Hello 👋 I'm your AI chatbot!").send()


@cl.on_message
async def main(message: cl.Message):

    response = llm.invoke(message.content)

    await cl.Message(content=response.content).send()
