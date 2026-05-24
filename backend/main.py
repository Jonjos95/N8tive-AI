"""
N8tive AI Agent Framework - FastAPI Backend
Main application entry point with CORS and middleware configuration
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from routes import chat, agents, config

# Load environment variables
load_dotenv()

app = FastAPI(
    title="N8tive AI Agent Framework",
    description="Full-stack AI Agent Builder with customizable agents",
    version="1.0.0"
)

# CORS configuration
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api", tags=["chat"])
app.include_router(agents.router, prefix="/api", tags=["agents"])
app.include_router(config.router, prefix="/api", tags=["config"])

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "N8tive AI Agent Framework",
        "version": "1.0.0"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

