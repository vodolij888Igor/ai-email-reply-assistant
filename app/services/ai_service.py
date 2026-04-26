"""
AI / LLM integration layer.

Right now this module uses **placeholder** logic only: no network calls to OpenAI.
Later you will replace `generate_reply_placeholder` with a real client that reads
`OPENAI_API_KEY` from the environment and calls the Chat Completions (or Responses) API.
"""

from app.schemas.email_schema import GenerateReplyRequest


def generate_reply_placeholder(request: GenerateReplyRequest) -> str:
    """
    Build a fake draft reply so the REST API works end-to-end without an API key.

    This keeps the portfolio project runnable on day one while you wire up the model.
    """
    # Short preview of the incoming message (avoid dumping huge bodies in the placeholder)
    body_preview = (request.email_body.strip() or "(no body)").splitlines()[0][:200]
    if len(request.email_body) > 200:
        body_preview += "..."

    # Echo the requested tone so you can see the parameter flowing through the stack
    lines = [
        f"Hi {request.sender_name},",
        "",
        f'Thank you for your email regarding "{request.email_subject}".',
        f"I've noted your message: {body_preview}",
        "",
        f"[Placeholder reply - tone requested: {request.reply_tone}]",
        "",
        "This text is generated locally. Replace `generate_reply_placeholder` in "
        "`app/services/ai_service.py` with an OpenAI API call when you are ready.",
        "",
        "Best regards,",
        "Your Name",
    ]
    return "\n".join(lines)
