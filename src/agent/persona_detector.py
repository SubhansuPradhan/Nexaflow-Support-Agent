from __future__ import annotations
import json
import re
from dataclasses import dataclass
import ollama
from config import settings

PERSONAS = {
    "TECHNICAL_EXPERT": "Technical Expert",
    "FRUSTRATED_USER": "Frustrated User",
    "BUSINESS_EXECUTIVE": "Business Executive",
}
PERSONA_ICONS = {
    "TECHNICAL_EXPERT": "🛠️",
    "FRUSTRATED_USER": "😤",
    "BUSINESS_EXECUTIVE": "💼",
}
PERSONA_DESCRIPTIONS = {
    "TECHNICAL_EXPERT": "Uses technical terminology, wants detailed explanations.",
    "FRUSTRATED_USER": "Emotional language, urgent tone, repeated complaints.",
    "BUSINESS_EXECUTIVE": "Outcome-focused, wants concise summaries.",
}

@dataclass
class PersonaResult:
    persona: str
    display_name: str
    confidence: float
    reasoning: str
    icon: str

    @property
    def description(self) -> str:
        return PERSONA_DESCRIPTIONS.get(self.persona, "")

_CLASSIFICATION_PROMPT = """You are a customer support persona classifier. Classify the user message into exactly ONE persona.

PERSONAS:
- TECHNICAL_EXPERT: Uses technical terms, wants root cause, step-by-step debug info
- FRUSTRATED_USER: Emotional frustration, urgent tone, phrases like "nothing works"
- BUSINESS_EXECUTIVE: Outcome-focused, asks about impact/SLA/timelines, prefers brevity

USER MESSAGE: {message}
RECENT CONVERSATION: {history}

Respond ONLY with valid JSON, no markdown, no explanation:
{{"persona": "TECHNICAL_EXPERT" | "FRUSTRATED_USER" | "BUSINESS_EXECUTIVE", "confidence": 0.0-1.0, "reasoning": "one sentence"}}"""


def detect_persona(message: str, conversation_history: list[dict]) -> PersonaResult:
    user_turns = [m["content"] for m in conversation_history if m["role"] == "user"]
    history_str = "\n".join(f"- {t}" for t in user_turns[-3:]) if user_turns else "None"
    prompt = _CLASSIFICATION_PROMPT.format(message=message, history=history_str)

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response["message"]["content"].strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        data = json.loads(raw)
        persona = data.get("persona", "FRUSTRATED_USER")
        if persona not in PERSONAS:
            persona = "FRUSTRATED_USER"
        return PersonaResult(
            persona=persona,
            display_name=PERSONAS[persona],
            confidence=float(data.get("confidence", 0.7)),
            reasoning=data.get("reasoning", ""),
            icon=PERSONA_ICONS[persona],
        )
    except (json.JSONDecodeError, KeyError):
        return _keyword_fallback(message)


def _keyword_fallback(message: str) -> PersonaResult:
    msg = message.lower()
    if any(w in msg for w in ["api", "error", "log", "config", "token", "oauth"]):
        persona = "TECHNICAL_EXPERT"
    elif any(w in msg for w in ["nothing works", "unacceptable", "!!!", "frustrated"]):
        persona = "FRUSTRATED_USER"
    elif any(w in msg for w in ["business", "impact", "revenue", "timeline"]):
        persona = "BUSINESS_EXECUTIVE"
    else:
        persona = "FRUSTRATED_USER"
    return PersonaResult(
        persona=persona,
        display_name=PERSONAS[persona],
        confidence=0.6,
        reasoning="Keyword-based fallback.",
        icon=PERSONA_ICONS[persona],
    )