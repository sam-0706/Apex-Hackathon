### apis/call_agents.py
from fastapi import APIRouter
from pydantic import BaseModel
from core_modules.call_agent import run_call_agent

router = APIRouter()

class CallRequest(BaseModel):
    phone_number: str

@router.post("/call-agent")
async def call_agent_endpoint(request: CallRequest):
    return run_call_agent(request.phone_number)


