from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from core_modules.faq_bot_qdrant import _get_llm_response

router = APIRouter()

class FAQRequest(BaseModel):
    chat_history: List[str]
    question: str

@router.post("/faq")
async def handle_faq(req: FAQRequest):
    response, duration = _get_llm_response(req.chat_history, req.question)
    return {
        "answer": response,
        "time_taken_sec": duration
    }
