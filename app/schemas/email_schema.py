"""
Pydantic models for the email reply API.

These define the *shape* of JSON the client sends and receives.
FastAPI uses them to validate input and document the API automatically.
"""

from pydantic import BaseModel, EmailStr, Field


class GenerateReplyRequest(BaseModel):
    """Fields the client sends when asking for a draft reply."""

    sender_name: str = Field(..., description="Display name of the person who sent the email")
    sender_email: EmailStr = Field(..., description="Email address of the sender")
    email_subject: str = Field(..., description="Subject line of the incoming message")
    email_body: str = Field(..., description="Plain text body of the email you are replying to")
    reply_tone: str = Field(
        ...,
        description="Desired tone for the reply, e.g. 'professional', 'friendly', 'brief'",
    )


class GenerateReplyResponse(BaseModel):
    """What the API returns after generating (or simulating) a reply."""

    generated_reply: str = Field(..., description="Draft email body you can edit and send")
