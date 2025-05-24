import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.faq_api import router as faq_router
from apis.call_agents import router as call_agent_router

app = FastAPI(
    title="TechNova HR FAQ Bot",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(faq_router, prefix="/api")
app.include_router(call_agent_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "TechNova HR FAQ Bot is running ✅",
        "try_post_faq": "/api/faq",
        "try_post_call": "/api/call-agent",
        "docs": "/docs"
    }
