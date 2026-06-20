"""
Multi-signal escalation logic.
Escalation is triggered by any combination of configurable signals.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from src.rag.retriever import RetrievedChunk
from src.agent.persona_detector import PersonaResult
from config import settings


@dataclass
class EscalationResult:
    should_escalate: bool
    reason: str
    priority: str           # "HIGH", "MEDIUM", "LOW"
    triggers: list[str] = field(default_factory=list)


def check_escalation(
    message: str,
    persona: PersonaResult,
    retrieved_chunks: list[RetrievedChunk],
    conversation_history: list[dict],
    turn_count: int,
    frustrated_turn_count: int,
) -> EscalationResult:
    """
    Evaluate all escalation signals and return a decision.

    Signals (configurable in settings.py):
    1. no_relevant_docs       - All retrieved chunks have low similarity
    2. keyword_detected       - Sensitive/legal/billing keywords in message
    3. turn_limit_reached     - Exceeded MAX_TURNS_BEFORE_ESCALATION
    4. repeated_frustration   - FRUSTRATED_USER persona for 3+ consecutive turns
    5. empty_retrieval        - ChromaDB returned nothing at all
    """
    triggers: list[str] = []
    priority = "LOW"

    # Signal 1: No relevant documents found
    if not retrieved_chunks:
        triggers.append("no_relevant_docs")
    elif all(not c.is_relevant for c in retrieved_chunks):
        triggers.append("low_confidence_retrieval")

    # Signal 2: Escalation keywords
    msg_lower = message.lower()
    hit_keywords = [kw for kw in settings.ESCALATION_KEYWORDS if kw in msg_lower]
    if hit_keywords:
        triggers.append(f"keyword_detected:{','.join(hit_keywords)}")
        priority = "HIGH"

    # Signal 3: Turn limit
    if turn_count >= settings.MAX_TURNS_BEFORE_ESCALATION:
        triggers.append("turn_limit_reached")
        priority = max(priority, "MEDIUM")

    # Signal 4: Repeated frustration (3+ turns as FRUSTRATED_USER)
    if frustrated_turn_count >= 6:
        triggers.append("repeated_frustration")
        priority = max(priority, "MEDIUM")

    # Signal 5: Sensitive topics detected
    sensitive_phrases = ["billing", "payment", "account suspended", "data loss", "security breach"]
    if any(p in msg_lower for p in sensitive_phrases):
        triggers.append("sensitive_topic")
        priority = "HIGH"

    if not triggers:
        return EscalationResult(
            should_escalate=False,
            reason="No escalation signals detected.",
            priority="NONE",
            triggers=[],
        )

    # Build human-readable reason
    reason_map = {
        "no_relevant_docs": "No matching documentation found in knowledge base.",
        "low_confidence_retrieval": "Retrieved documents had low relevance to the query.",
        "turn_limit_reached": f"Conversation exceeded {settings.MAX_TURNS_BEFORE_ESCALATION} turns without resolution.",
        "repeated_frustration": "User expressed frustration across multiple turns.",
        "sensitive_topic": "Message contains sensitive billing or security topic.",
    }

    readable_reasons = []
    for t in triggers:
        base = t.split(":")[0]
        if base in reason_map:
            readable_reasons.append(reason_map[base])
        elif base == "keyword_detected":
            keywords = t.split(":")[1] if ":" in t else ""
            readable_reasons.append(f"Escalation keyword(s) detected: {keywords}.")

    return EscalationResult(
        should_escalate=True,
        reason=" | ".join(readable_reasons),
        priority=priority,
        triggers=triggers,
    )
