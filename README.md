# AI Email Reply Assistant

A small **FastAPI** backend for a portfolio project aimed at **Junior AI Automation Engineer** and **AI Agent Developer** roles. The service accepts **simulated email input** (no Gmail or OAuth in this version) and returns a **draft reply** you could later connect to a real LLM or mailbox workflow.

## What it does

- Exposes a JSON API with one main action: **generate a reply** from sender details, subject, body, and a desired **tone**.
- Uses **Pydantic** schemas for clear request/response contracts and automatic OpenAPI docs.
- Ships with **placeholder** reply logic so the project runs without API keys or paid services. The OpenAI client is listed in dependencies for when you swap in a real call.

## Tech stack

| Piece | Role |
|--------|------|
| Python | Runtime |
| FastAPI | HTTP API framework |
| Uvicorn | ASGI server |
| Pydantic | Validation / serialization |
| python-dotenv | Load `.env` (e.g. future `OPENAI_API_KEY`) |
| OpenAI (optional next step) | Listed in `requirements.txt` for a future real integration |

## Project layout

```
.
├── README.md
├── .env.example
├── .gitignore
├── requirements.txt
└── app/
    ├── main.py                 # FastAPI app and routes
    ├── services/
    │   └── ai_service.py       # Reply generation (placeholder today)
    └── schemas/
        └── email_schema.py     # Request/response models
```

## Quick start

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv .venv
   ```

2. **Activate it** — on Windows (PowerShell):

   ```bash
   .\.venv\Scripts\Activate.ps1
   ```

   On macOS/Linux:

   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server** from the project root:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open **http://127.0.0.1:8000/docs** to try **POST `/generate-reply`** interactively.

## API

### `POST /generate-reply`

**Request body (JSON)**

| Field | Type | Description |
|--------|------|-------------|
| `sender_name` | string | Sender display name |
| `sender_email` | string | Valid email address |
| `email_subject` | string | Subject line |
| `email_body` | string | Message body (simulated) |
| `reply_tone` | string | e.g. `professional`, `friendly`, `brief` |

**Response**

| Field | Type | Description |
|--------|------|-------------|
| `generated_reply` | string | Draft reply text |

**Example**

```bash
curl -X POST "http://127.0.0.1:8000/generate-reply" ^
  -H "Content-Type: application/json" ^
  -d "{\"sender_name\":\"Alex\",\"sender_email\":\"alex@example.com\",\"email_subject\":\"Project timeline\",\"email_body\":\"Can we move the deadline to Friday?\",\"reply_tone\":\"professional\"}"
```

*(Use line continuation appropriate to your shell on non-Windows systems.)*

## Environment variables

Copy `.env.example` to `.env` when you add a real OpenAI integration. The placeholder implementation does not require a key.

## Roadmap ideas

- Replace `generate_reply_placeholder` in `app/services/ai_service.py` with the OpenAI API using `OPENAI_API_KEY` from `.env`.
- Add streaming responses, conversation history, or guardrails for PII.
- Optional: Gmail read-only or send flows behind explicit user consent.

## License

Use and modify freely for learning and portfolio use.
