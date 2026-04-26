"""
AI / LLM integration: draft email replies using the OpenAI Chat Completions API.

Reads OPENAI_API_KEY from the environment (usually set via a `.env` file and python-dotenv).
"""

import os

from dotenv import load_dotenv
from openai import APIConnectionError, APIError, OpenAI, RateLimitError

from app.schemas.email_schema import GenerateReplyRequest

# Load variables from `.env` into os.environ before we read OPENAI_API_KEY.
# (main.py also calls load_dotenv; calling twice is safe.)
load_dotenv()

# Model used for chat completions — good balance of quality and cost for short replies.
MODEL = "gpt-4o-mini"


class EmailReplyError(Exception):
    """
    Raised when we cannot return a reply (missing config, network, or OpenAI error).

    `status_code` is meant for mapping to an HTTP status in FastAPI.
    """

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


def _build_messages(request: GenerateReplyRequest) -> list[dict[str, str]]:
    """Turn the incoming email fields into chat messages for the model."""
    system = (
        "You are an assistant that writes helpful email replies. "
        "Produce only the reply body: greeting, clear response to the sender, and a polite closing. "
        "Do not repeat the subject line as a title. "
        "Match the requested tone (e.g. professional, friendly, brief, formal). "
        "If information is missing, stay general and courteous rather than inventing facts."
    )
    user = (
        f"Requested reply tone: {request.reply_tone}\n\n"
        f"--- Incoming email ---\n"
        f"From: {request.sender_name} <{request.sender_email}>\n"
        f"Subject: {request.email_subject}\n\n"
        f"{request.email_body}\n"
        f"--- End of email ---\n\n"
        "Write the reply text only. No markdown code fences."
    )
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]


def generate_email_reply(request: GenerateReplyRequest) -> str:
    """
    Call OpenAI and return the generated reply string.

    Raises EmailReplyError for configuration problems or API failures
    (your route layer can turn that into an HTTP error for the client).
    """
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise EmailReplyError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your API key.",
            status_code=503,
        )

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=_build_messages(request),
            temperature=0.7,
            max_tokens=1024,
        )
    except RateLimitError as exc:
        raise EmailReplyError(
            "OpenAI rate limit reached. Wait a moment and try again.",
        ) from exc
    except APIConnectionError as exc:
        raise EmailReplyError(
            "Could not connect to OpenAI. Check your internet connection.",
        ) from exc
    except APIError as exc:
        # Covers authentication errors, invalid requests, and server errors from OpenAI.
        raise EmailReplyError(f"OpenAI API error: {exc}") from exc
    except Exception as exc:
        raise EmailReplyError("Unexpected error while generating the reply.") from exc

    if not response.choices:
        raise EmailReplyError("OpenAI returned no reply choices.")

    content = response.choices[0].message.content
    if content is None or not str(content).strip():
        raise EmailReplyError("The model returned an empty reply.")

    return str(content).strip()
