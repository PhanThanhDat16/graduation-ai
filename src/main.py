from fastapi import FastAPI

from src.api.chat import router as chat_router

app = FastAPI(
    title="AI Chatbot API",
    version="1.0.0"
)

app.include_router(chat_router, prefix="/api/chat", tags=["Chat"])


@app.get("/")
def root():
    return {"message": "AI Chatbot API running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
