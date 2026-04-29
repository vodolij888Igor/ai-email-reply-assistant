from fastapi.testclient import TestClient

import app.main as main_module
from app.services.ai_service import EmailReplyError


client = TestClient(main_module.app)


VALID_PAYLOAD = {
    "sender_name": "John Smith",
    "sender_email": "john@example.com",
    "email_subject": "Question about your AI automation services",
    "email_body": "Hi, can you explain how AI can help automate email replies?",
    "reply_tone": "professional",
}


def test_generate_reply_success_returns_200_and_generated_reply(monkeypatch):
    """Successful request should return HTTP 200 and generated_reply field."""

    def fake_generate_email_reply(_payload):
        return "Thank you for your message. Here is your generated draft reply."

    monkeypatch.setattr(main_module, "generate_email_reply", fake_generate_email_reply)

    response = client.post("/generate-reply", json=VALID_PAYLOAD)

    assert response.status_code == 200
    body = response.json()
    assert "generated_reply" in body
    assert isinstance(body["generated_reply"], str)
    assert body["generated_reply"]


def test_generate_reply_invalid_payload_returns_422():
    """Missing required fields should fail FastAPI/Pydantic validation."""
    invalid_payload = {"sender_name": "John Smith"}

    response = client.post("/generate-reply", json=invalid_payload)

    assert response.status_code == 422


def test_generate_reply_missing_api_key_returns_503(monkeypatch):
    """If service raises missing-key error, route should map it to HTTP 503."""

    def fake_generate_email_reply(_payload):
        raise EmailReplyError(
            "OPENAI_API_KEY is not set. Copy .env.example to .env and add your API key.",
            status_code=503,
        )

    monkeypatch.setattr(main_module, "generate_email_reply", fake_generate_email_reply)

    response = client.post("/generate-reply", json=VALID_PAYLOAD)

    assert response.status_code == 503
    assert "OPENAI_API_KEY is not set" in response.json()["detail"]


def test_generate_reply_openai_failure_returns_502(monkeypatch):
    """If service raises OpenAI failure, route should map it to HTTP 502."""

    def fake_generate_email_reply(_payload):
        raise EmailReplyError("OpenAI API error: service unavailable", status_code=502)

    monkeypatch.setattr(main_module, "generate_email_reply", fake_generate_email_reply)

    response = client.post("/generate-reply", json=VALID_PAYLOAD)

    assert response.status_code == 502
    assert "OpenAI API error" in response.json()["detail"]
