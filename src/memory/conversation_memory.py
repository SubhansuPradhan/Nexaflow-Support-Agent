"""
In-memory session state for a single support conversation.
Tracks messages, persona history, turn counts, escalation status,
and which documents were used — everything needed for the handoff summary.
"""

from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from src.rag.retriever import RetrievedChunk


@dataclass
class ConversationMemory:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    messages: list[dict] = field(default_factory=list)       # {role, content}
    persona_history: list[str] = field(default_factory=list) # e.g. ["FRUSTRATED_USER", ...]
    retrieved_chunks: list[RetrievedChunk] = field(default_factory=list)
    is_escalated: bool = False
    handoff_summary: dict | None = None

    @property
    def turn_count(self) -> int:
        return len([m for m in self.messages if m["role"] == "user"])

    @property
    def frustrated_turn_count(self) -> int:
        return self.persona_history.count("FRUSTRATED_USER")

    @property
    def last_persona(self) -> str | None:
        return self.persona_history[-1] if self.persona_history else None

    def add_user_message(self, content: str) -> None:
        self.messages.append({"role": "user", "content": content})

    def add_assistant_message(self, content: str) -> None:
        self.messages.append({"role": "assistant", "content": content})

    def update_persona(self, persona: str) -> None:
        self.persona_history.append(persona)

    def update_chunks(self, chunks: list[RetrievedChunk]) -> None:
        """Accumulate retrieved chunks (deduplicated by source+text)."""
        existing_texts = {c.text for c in self.retrieved_chunks}
        for chunk in chunks:
            if chunk.text not in existing_texts:
                self.retrieved_chunks.append(chunk)
                existing_texts.add(chunk.text)

    def mark_escalated(self, summary: dict) -> None:
        self.is_escalated = True
        self.handoff_summary = summary

    def get_history_for_llm(self) -> list[dict]:
        """Return message history in the format Claude expects."""
        return self.messages.copy()
