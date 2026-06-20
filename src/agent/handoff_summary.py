"""
Generates a structured handoff summary when escalation occurs.
The summary is designed to give a human agent everything they need
to pick up the conversation without starting from scratch.
"""

from __future__ import annotations
import json
from datetime import datetime, timezone
from src.agent.persona_detector import PersonaResult
from src.agent.escalation_handler import EscalationResult
from src.rag.retriever import RetrievedChunk, get_unique_sources
from config import settings


def _summarise_issue(conversation_history, persona):
    import ollama
    from config import settings

    user_messages = [m["content"] for m in conversation_history if m["role"] == "user"]
    history_text = "\n".join(f"- {m}" for m in user_messages)

    prompt = (
        f"A customer ({persona.display_name}) contacted support.\n"
        f"Messages:\n{history_text}\n\n"
        "Summarise the core issue in 1-2 sentences. Output only the summary, nothing else."
    )

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"].strip()


def _extract_attempted_steps(conversation_history: list[dict]) -> list[str]:
    """Pull out the AI's suggested action steps from conversation history."""
    steps: list[str] = []
    for msg in conversation_history:
        if msg["role"] == "assistant":
            # Extract numbered or bulleted lines as "steps"
            for line in msg["content"].split("\n"):
                line = line.strip()
                if line and (
                    line[0].isdigit()
                    or line.startswith("-")
                    or line.startswith("•")
                    or line.lower().startswith("step")
                ):
                    clean = line.lstrip("0123456789.-•) ").strip()
                    if len(clean) > 10:
                        steps.append(clean)
    return steps[:8]  # cap at 8


def generate_handoff_summary(
    session_id: str,
    persona: PersonaResult,
    escalation: EscalationResult,
    conversation_history: list[dict],
    retrieved_chunks: list[RetrievedChunk],
) -> dict:
    """Return a structured dict suitable for JSON export or UI display."""

    issue_summary = _summarise_issue(conversation_history, persona)
    attempted_steps = _extract_attempted_steps(conversation_history)
    sources_used = get_unique_sources(retrieved_chunks)

    # Determine recommended next steps based on escalation triggers
    recommendations: list[str] = []
    for trigger in escalation.triggers:
        if "keyword" in trigger:
            recommendations.append("Review account for billing/legal flags before responding.")
        if "frustration" in trigger:
            recommendations.append("Open with direct acknowledgment of the customer's wait time.")
        if "no_relevant_docs" in trigger or "low_confidence" in trigger:
            recommendations.append("Consult internal wiki or senior engineer — documentation gap detected.")
        if "turn_limit" in trigger:
            recommendations.append("Customer has been waiting too long; prioritise immediate resolution.")
        if "sensitive" in trigger:
            recommendations.append("Route to billing/security specialist if not already done.")

    if not recommendations:
        recommendations.append("Review conversation history and continue support.")

    summary = {
        "session_id": session_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "priority": escalation.priority,
        "persona": {
            "type": persona.persona,
            "display_name": persona.display_name,
            "confidence": round(persona.confidence, 2),
        },
        "issue_summary": issue_summary,
        "escalation_reason": escalation.reason,
        "escalation_triggers": escalation.triggers,
        "documents_referenced": sources_used,
        "attempted_steps": attempted_steps if attempted_steps else ["No specific steps extracted."],
        "recommended_next_steps": recommendations,
        "conversation_turns": len([m for m in conversation_history if m["role"] == "user"]),
    }

    return summary


def format_handoff_for_display(summary: dict) -> str:
    """Pretty-print the summary as formatted JSON string."""
    return json.dumps(summary, indent=2)
