"""
FastAPI entrypoint for the AI Email Reply Assistant.

Run locally:
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs for interactive API documentation.
"""

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app.schemas.email_schema import GenerateReplyRequest, GenerateReplyResponse
from app.services.ai_service import EmailReplyError, generate_email_reply

# Load `.env` early so any code imported later sees OPENAI_API_KEY.
load_dotenv()

app = FastAPI(
    title="AI Email Reply Assistant",
    description="Simulated inbox input and draft reply generation via the OpenAI API.",
    version="0.2.0",
)


@app.post("/generate-reply", response_model=GenerateReplyResponse)
def generate_reply(payload: GenerateReplyRequest) -> GenerateReplyResponse:
    """
    Accept simulated email metadata + body, return a draft reply from OpenAI.

    Requires OPENAI_API_KEY in the environment (see `.env.example`).
    """
    try:
        text = generate_email_reply(payload)
    except EmailReplyError as exc:
        raise HTTPException(status_code=exc.status_code, detail=str(exc)) from exc

    return GenerateReplyResponse(generated_reply=text)
