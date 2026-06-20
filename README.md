# NexaFlow Persona-Adaptive Customer Support Agent

An intelligent customer support agent that detects user personas, retrieves relevant knowledge from a local vector database, and adapts its response tone accordingly. Built with Ollama (local LLM), ChromaDB, and Sentence Transformers — no external API keys required.

---

## Project Overview

This agent handles customer support queries for **NexaFlow** (a fictional SaaS platform). For every incoming message it:

1. Detects the customer's persona (Technical Expert, Frustrated User, or Business Executive)
2. Retrieves the most relevant documentation chunks from a local ChromaDB vector store
3. Generates a response in a tone and style matched to that persona
4. Escalates to a human agent when the situation exceeds what the AI can resolve

The entire system runs locally. No API keys, no cloud dependencies, no billing.

---

## Tech Stack

| Component        | Choice                          | Version   |
|------------------|---------------------------------|-----------|
| LLM              | Ollama (llama3.2, local)        | latest    |
| Embedding Model  | sentence-transformers MiniLM-L6 | 2.7.0+    |
| Vector Database  | ChromaDB                        | 0.5.0+    |
| UI Framework     | Streamlit                       | 1.35.0+   |
| PDF Generation   | ReportLab                       | 4.2.0+    |
| PDF Reading      | pypdf                           | 4.2.0+    |
| CLI Output       | rich                            | 13.7.0+   |
| Language         | Python                          | 3.10+     |

---

## Architecture

```
User Query
    │
    ▼
┌─────────────────────┐
│  Persona Detector   │  -- Ollama classifies into 3 personas
│  (persona_detector) │     Returns: persona type + confidence score
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   RAG Retriever     │  -- Sentence Transformers embed the query
│   (retriever.py)    │     ChromaDB returns top-4 relevant chunks
└────────┬────────────┘     with cosine similarity scores
         │
         ▼
┌─────────────────────┐
│  Response Generator │  -- Persona-specific system prompt injected
│  (response_gen...)  │     Retrieved chunks used as grounded context
└────────┬────────────┘     Ollama generates the final response
         │
         ▼
┌─────────────────────┐
│  Escalation Check   │  -- Multi-signal: keywords, low confidence,
│  (escalation_...)   │     turn limit, repeated frustration
└────────┬────────────┘
         │
    ┌────┴────┐
    │         │
  Normal   Escalate
  Reply       │
              ▼
        ┌──────────────┐
        │ Handoff      │  -- Structured JSON summary for human agent
        │ Summary Gen  │     Includes: persona, issue, docs used,
        └──────────────┘     steps attempted, recommendations
```

---

## Persona Detection Strategy

**Classification Method**: Ollama LLM call with a structured prompt.

Each incoming message is sent to the local LLM with the last 3 user turns as context. The model responds with a JSON object containing:
- `persona`: one of `TECHNICAL_EXPERT`, `FRUSTRATED_USER`, `BUSINESS_EXECUTIVE`
- `confidence`: float 0.0-1.0
- `reasoning`: one-sentence explanation

**Prompt Design**: The prompt provides exact behavioral definitions for each persona with concrete examples, then demands strict JSON output to eliminate parsing issues.

**Fallback**: If the LLM returns malformed JSON, a keyword-matching fallback classifies based on terms like "API", "error", "unacceptable", "impact", etc. This ensures the system never crashes due to an unexpected model output.

**Why not a fine-tuned classifier?** For this assignment without labelled training data, a few-shot prompt to a local LLM is faster to build, easier to adjust, and performs well on short support messages without requiring any additional infrastructure.

---

## RAG Pipeline Design

### Chunking Strategy
- Split on double newlines (paragraphs) first — preserves semantic coherence
- Fall back to hard character splits for oversized paragraphs
- Chunk size: 500 characters, overlap: 60 characters
- Overlap prevents answer context from being cut across chunk boundaries

### Embedding Model
`all-MiniLM-L6-v2` via sentence-transformers:
- Completely free, no API key required
- 384-dimensional dense embeddings
- ~80MB model, downloads once and is cached locally
- Strong performance on short query-document retrieval tasks

### Vector Database
**ChromaDB** with cosine similarity (`hnsw:space: cosine`):
- Persists to disk in `./chroma_db/`
- Cosine distance is more appropriate than Euclidean for normalized text embeddings
- Low-confidence threshold: distance > 0.65 (similarity < 0.35) triggers escalation signal

### Retrieval Strategy
- Retrieve top-4 chunks per query
- Each chunk carries source filename and page number as metadata
- Relevance check: `similarity >= 0.35` marks a chunk as relevant
- If no chunks pass the threshold, escalation is triggered automatically

---

## Escalation Logic

Six independent signals, all configurable in `config/settings.py`:

| Signal                  | Trigger Condition                                   | Priority |
|-------------------------|-----------------------------------------------------|----------|
| `no_relevant_docs`      | ChromaDB returns no chunks at all                   | LOW      |
| `low_confidence`        | All retrieved chunks have similarity < 0.35         | LOW      |
| `keyword_detected`      | Message contains legal/billing/threat keywords      | HIGH     |
| `turn_limit_reached`    | Conversation exceeds 10 turns without resolution    | MEDIUM   |
| `repeated_frustration`  | FRUSTRATED_USER persona detected 6+ times           | MEDIUM   |
| `sensitive_topic`       | "billing", "account suspended", "data loss", etc.   | HIGH     |

Any triggered signal causes escalation. Priority is the maximum level across all triggered signals.

---

## Knowledge Base

16 support documents covering the fictional NexaFlow SaaS platform:

| File                           | Type | Content                             |
|--------------------------------|------|-------------------------------------|
| getting_started_guide.md       | MD   | Account setup, plans, dashboard     |
| api_authentication.md          | MD   | API keys, OAuth 2.0, token refresh  |
| password_reset_guide.md        | MD   | Reset flows, 2FA, account lockout   |
| billing_and_payments.md        | MD   | Pricing, invoices, failed payments  |
| troubleshooting_guide.md       | MD   | Connectivity, 500 errors, webhooks  |
| sla_and_uptime_policy.md       | MD   | Uptime SLA, credits, support tiers  |
| api_rate_limits.md             | MD   | Rate limit tiers, headers, 429      |
| error_codes_reference.md       | MD   | HTTP codes, NF error codes          |
| webhook_setup_guide.md         | MD   | Webhooks, signatures, retry policy  |
| data_security_privacy.md       | MD   | Encryption, compliance, GDPR        |
| account_management.md          | MD   | Email change, deletion, SSO         |
| team_and_permissions.md        | MD   | Roles, invitations, bulk import     |
| third_party_integrations.md    | MD   | Slack, GitHub, Zapier integrations  |
| data_export_guide.md           | MD   | Export formats, scheduled exports   |
| faq.md                         | MD   | General, billing, technical FAQs    |
| refund_cancellation_policy.pdf | PDF  | Refund policy, cancellations        |

---

## Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Ollama installed on your machine (https://ollama.com/download)
- Minimum 8GB RAM recommended

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/nexaflow-support-agent.git
cd nexaflow-support-agent
```

### Step 2: Install Ollama and pull the model
Download Ollama from https://ollama.com/download and install it.

Then pull the LLM:
```bash
ollama pull llama3.2
```

Verify it works:
```bash
ollama run llama3.2 "say hello in one word"
```

### Step 3: Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Step 4: Install dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 5: Ingest the knowledge base (run once)
```bash
python scripts/ingest_documents.py
```

This will:
- Generate the PDF document using ReportLab
- Load all 16 documents from `/data`
- Create text chunks (approximately 120 chunks total)
- Download and cache the sentence-transformers embedding model (~80MB, first run only)
- Store all vectors in ChromaDB at `./chroma_db/`

### Step 6: Start the agent

**Option A — Streamlit UI (recommended):**
```bash
python -m streamlit run src/ui/streamlit_app.py
```
Opens at http://localhost:8501

**Option B — Command-line interface:**
```bash
python main.py
```

---

## Environment Variables

This project runs fully locally with Ollama. No API keys are required.

If you switch the LLM backend to Claude or Gemini, add the relevant key to a `.env` file:

```
ANTHROPIC_API_KEY=your_key_here   # if using Claude
GEMINI_API_KEY=your_key_here      # if using Gemini
```

---

## Example Queries

**Technical Expert:**
```
I'm getting NF-1004 errors on token refresh. The OAuth flow works initially
but fails after the first hour. Is the refresh token expiry configurable?
```

**Frustrated User:**
```
I've been trying to log in for 3 days and NOTHING WORKS.
I've cleared cache, tried different browsers, everything!
```

**Business Executive:**
```
Our team has been unable to access the dashboard since this morning.
What is the business impact and when can we expect resolution?
```

**Escalation trigger — legal keyword:**
```
I want a refund immediately. I'm going to contact my lawyer if this isn't resolved.
```

**Escalation trigger — no matching docs:**
```
Can you explain your company's policy on NFT-based subscription tokens?
```

---

## Known Limitations

1. **No persistent memory across sessions**: Each browser session starts fresh. Multi-session memory would require SQLite or Redis.
2. **English-only**: Persona detection and responses work in English only. Non-English input degrades accuracy.
3. **Embedding model quality**: `all-MiniLM-L6-v2` is fast and lightweight but not the strongest retrieval model. `BAAI/bge-base-en-v1.5` would improve retrieval accuracy at ~10% extra latency.
4. **Static knowledge base**: Documents must be re-ingested manually when updated. A production system would need incremental indexing.
5. **Single-agent architecture**: No multi-agent orchestration. LangGraph could add specialised sub-agents for billing, technical, and policy queries separately.
6. **Local LLM quality ceiling**: Llama 3.2 is strong for its size but produces noticeably weaker outputs than GPT-4 or Claude Sonnet on complex technical queries. This is the direct tradeoff for running fully offline.

---

## Bonus Features Implemented

- Multi-turn conversation memory within sessions
- Confidence scoring displayed visually in the sidebar
- Structured human handoff summary with JSON export
- Priority classification (HIGH/MEDIUM/LOW) on escalation events
- Source document citations shown below each AI response
- Downloadable handoff JSON from the Streamlit UI
- Keyword-based persona fallback when LLM output is malformed
#   N e x a F l o w - S u p p o r t - A g e n t  
 