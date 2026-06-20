import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# ── LLM ──────────────────────────────────────────────
OLLAMA_MODEL: str = "llama3.2"
OLLAMA_BASE_URL: str = "http://localhost:11434"

# ── Embedding ─────────────────────────────────────────
EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

# ── ChromaDB ─────────────────────────────────────────
CHROMA_PERSIST_DIR: str = "./chroma_db"
CHROMA_COLLECTION_NAME: str = "nexaflow_support"

# ── RAG ──────────────────────────────────────────────
CHUNK_SIZE: int = 500
CHUNK_OVERLAP: int = 60
TOP_K_RESULTS: int = 4
LOW_CONFIDENCE_THRESHOLD: float = 0.65

# ── Escalation ───────────────────────────────────────
MAX_TURNS_BEFORE_ESCALATION: int = 10
ESCALATION_KEYWORDS: list[str] = [
    "refund", "lawyer", "legal", "sue",
    "data breach", "fraud", "chargeback",
    "attorney", "cancel account",
]

# ── Data ─────────────────────────────────────────────
DATA_DIR: str = "./data"