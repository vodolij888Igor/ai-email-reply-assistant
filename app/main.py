"""
FastAPI entrypoint for the AI Email Reply Assistant.

Run locally:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for interactive API documentation.
"""

from dotenv import load_dotenv
from fastapi import FastAPI

from app.schemas.email_schema import GenerateReplyRequest, GenerateReplyResponse
from app.services.ai_service import generate_reply_placeholder

# Load variables from `.env` into the process environment (used later for OPENAI_API_KEY).
load_dotenv()

app = FastAPI(
    title="AI Email Reply Assistant",
    description="Simulated inbox input and draft reply generation (placeholder AI for v1).",
    version="0.1.0",
)


@app.post("/generate-reply", response_model=GenerateReplyResponse)
def generate_reply(payload: GenerateReplyRequest) -> GenerateReplyResponse:
    """
    Accept simulated email metadata + body, return a draft reply string.

    v1 uses placeholder logic in `ai_service.py` — no external LLM call yet.
    """
    text = generate_reply_placeholder(payload)
    return GenerateReplyResponse(generated_reply=text)
