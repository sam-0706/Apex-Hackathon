from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apis.faq_api import router as faq_router

app = FastAPI(
    title="TechNova HR FAQ Bot",
    version="1.0.0"
)

# Enable CORS for all origins (for development/demo purposes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
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
