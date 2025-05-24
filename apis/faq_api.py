from fastapi import APIRouter,Request
from pydantic import BaseModel
from typing import List
from core_modules.faq_bot_qdrant import _get_llm_response
from core_modules.serviceroutes import getalljobs,get_resumes_by_job,add_job,add_resume,send_mail

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
    response = add_job(response['job_id'], response['job_description'] , response['job_name'])
    return response

@router.post("/add_resume")
async def add_new_resume(request: Request):
    response =  await request.json()
    response = add_resume(response['job_id'], response['resume'], response['name'],response['email'])
    return response

@router.post("/send_email")
async def send_email(request: Request):
    request =  await request.json()
    response = send_mail(sender_email="rahultejmora18@gmail.com",
                        sender_password="wcbo xeye rjie fatl",
                        candidate_email=request["Email"],
                        candidate_name= request["Name"],
                        position=request["Position"],
                        interview_date= request["Date"],
                        interview_time= request["Time"],
                        interview_location= "Remote",
                        status= request["Status"],
                        feedback_message=request.get("Feedback", "")
                        )
    return response
