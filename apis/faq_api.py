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

@router.get("/get_jobs")
async def get_jobs():
    response= getalljobs()
    return response

@router.get("/get_job_by_id")
async def get_job_by_id(job_id: str):
    response = get_resumes_by_job(job_id)
    return response

@router.post("/add_job")
async def add_new_job(request: Request):
    response =  await request.json()
    response = add_job(response['job_id'], response['job_description'])
    return response

@router.post("/add_resume")
async def add_new_resume(request: Request):
    response =  await request.json()
    response = add_resume(response['job_id'], response['resume'], response['name'])
    return response
