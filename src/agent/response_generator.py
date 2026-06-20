from __future__ import annotations
import ollama
from src.rag.retriever import RetrievedChunk, format_context
from src.agent.persona_detector import PersonaResult
from config import settings

_PERSONA_SYSTEM_PROMPTS = {
    "TECHNICAL_EXPERT": """You are a senior technical support engineer at NexaFlow.
- Use precise technical terminology
- Provide root cause analysis
- Include step-by-step commands and error code explanations
- Be thorough and detailed
Tone: professional, direct, peer-to-peer.""",

    "FRUSTRATED_USER": """You are an empathetic customer support specialist at NexaFlow.
- Open with acknowledgment of their frustration
- Use plain simple language, zero jargon
- Focus on the next immediate action
- Be concise and reassuring
Tone: warm, calm, human.""",

    "BUSINESS_EXECUTIVE": """You are a senior support consultant at NexaFlow.
- Lead with the bottom line
- Use bullet points
- No technical jargon
- Include resolution timeframe if available
- Keep under 150 words
Tone: concise, confident, executive-level.""",
}

_RESPONSE_TEMPLATE = """KNOWLEDGE BASE CONTEXT:
{context}

---

CUSTOMER MESSAGE:
{message}

Answer using ONLY the knowledge base context above. If context is insufficient, say so honestly. Do not invent facts."""


def generate_response(
    message: str,
    persona: PersonaResult,
    retrieved_chunks: list[RetrievedChunk],
    conversation_history: list[dict],
) -> str:
    system_prompt = _PERSONA_SYSTEM_PROMPTS.get(
        persona.persona, _PERSONA_SYSTEM_PROMPTS["FRUSTRATED_USER"]
    )

    context = format_context(retrieved_chunks)
    user_content = _RESPONSE_TEMPLATE.format(context=context, message=message)

    messages = [{"role": "system", "content": system_prompt}]
    for turn in conversation_history[-6:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_content})

    response = ollama.chat(
        model=settings.OLLAMA_MODEL,
        messages=messages,
    )

    return response["message"]["content"].strip()