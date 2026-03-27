from fastapi import APIRouter, Request

router = APIRouter()


@router.post("/")
async def chat(request: Request):
    return "hello"