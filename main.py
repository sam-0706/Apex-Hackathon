from fastapi import FastAPI
from apis.faq_api import router as faq_router

app = FastAPI(
    title="TechNova HR FAQ Bot",
    version="1.0.0"
)

# Mount router
app.include_router(faq_router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "TechNova HR FAQ Bot is running ✅",
        "try_post": "/api/faq",
        "docs": "/docs"
    }
