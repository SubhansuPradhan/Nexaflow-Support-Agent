"""
Streamlit chat UI for the NexaFlow Persona-Adaptive Support Agent.
Run with: streamlit run src/ui/streamlit_app.py
"""

import json
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
from src.agent.persona_detector import detect_persona
from src.agent.response_generator import generate_response
from src.agent.escalation_handler import check_escalation
from src.agent.handoff_summary import generate_handoff_summary
from src.memory.conversation_memory import ConversationMemory
from src.rag.retriever import retrieve

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NexaFlow Support Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stChatMessage { border-radius: 12px; margin-bottom: 0.5rem; }
    .persona-card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        color: #f1f5f9;
    }
    .persona-name { font-size: 1.1rem; font-weight: 700; color: #38bdf8; }
    .confidence-bar { height: 6px; border-radius: 3px; background: #1e3a5f; margin-top: 6px; }
    .confidence-fill { height: 100%; border-radius: 3px; background: linear-gradient(90deg, #38bdf8, #818cf8); }
    .source-chip {
        display: inline-block;
        background: #1e293b;
        color: #94a3b8;
        border: 1px solid #334155;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.78rem;
        margin: 2px;
    }
    .escalation-banner {
        background: linear-gradient(135deg, #450a0a, #7f1d1d);
        border: 1px solid #ef4444;
        border-radius: 10px;
        padding: 1rem;
        color: #fef2f2;
        margin: 0.5rem 0;
    }
    .handoff-box {
        background: #0f172a;
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 1rem;
        font-family: monospace;
        font-size: 0.8rem;
        color: #94a3b8;
        white-space: pre-wrap;
        max-height: 400px;
        overflow-y: auto;
    }
    .stat-label { color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; }
    .stat-value { color: #f1f5f9; font-weight: 600; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)


# ── Session State ─────────────────────────────────────────────────────────────
def init_session():
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationMemory()
    if "current_persona" not in st.session_state:
        st.session_state.current_persona = None
    if "last_sources" not in st.session_state:
        st.session_state.last_sources = []
    if "display_messages" not in st.session_state:
        # Each item: {role, content, persona, sources, escalated}
        st.session_state.display_messages = []


init_session()
memory: ConversationMemory = st.session_state.memory


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🤖 NexaFlow Support")
    st.caption(f"Session ID: `{memory.session_id}`")
    st.divider()

    # Persona card
    if st.session_state.current_persona:
        p = st.session_state.current_persona
        conf_pct = int(p.confidence * 100)
        st.markdown(f"""
<div class="persona-card">
  <div style="font-size:2rem">{p.icon}</div>
  <div class="persona-name">{p.display_name}</div>
  <div style="color:#94a3b8;font-size:0.82rem;margin-top:4px">{p.description}</div>
  <div class="stat-label" style="margin-top:0.7rem">Confidence</div>
  <div class="confidence-bar">
    <div class="confidence-fill" style="width:{conf_pct}%"></div>
  </div>
  <div style="color:#64748b;font-size:0.75rem;margin-top:2px">{conf_pct}%</div>
</div>
""", unsafe_allow_html=True)
    else:
        st.info("Send a message to detect persona.")

    st.divider()

    # Session stats
    st.markdown("<div class='stat-label'>Turns</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-value'>{memory.turn_count}</div>", unsafe_allow_html=True)

    escalation_color = "#ef4444" if memory.is_escalated else "#22c55e"
    escalation_label = "ESCALATED" if memory.is_escalated else "ACTIVE"
    st.markdown(f"<div class='stat-label' style='margin-top:0.8rem'>Status</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='stat-value' style='color:{escalation_color}'>{escalation_label}</div>", unsafe_allow_html=True)

    st.divider()

    if st.button("🔄 New Session", use_container_width=True):
        for key in ["memory", "current_persona", "last_sources", "display_messages"]:
            st.session_state.pop(key, None)
        st.rerun()

    st.caption("Powered by Claude + ChromaDB + Sentence Transformers")


# ── Main Area ─────────────────────────────────────────────────────────────────
st.markdown("## 💬 Customer Support Chat")

# Render existing messages
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"], avatar="👤" if msg["role"] == "user" else "🤖"):
        st.markdown(msg["content"])

        # Show sources below AI messages
        if msg["role"] == "assistant" and msg.get("sources"):
            chips_html = "".join(f'<span class="source-chip">📄 {s}</span>' for s in msg["sources"])
            st.markdown(f"<div style='margin-top:6px'>{chips_html}</div>", unsafe_allow_html=True)

        # Show escalation banner
        if msg.get("escalated"):
            st.markdown("""
<div class="escalation-banner">
⚠️ <strong>Escalated to Human Agent</strong> — This conversation has been flagged for human review.
</div>
""", unsafe_allow_html=True)

# Show handoff summary if escalated
if memory.is_escalated and memory.handoff_summary:
    with st.expander("📋 Human Handoff Summary", expanded=True):
        st.markdown(f"""<div class="handoff-box">{json.dumps(memory.handoff_summary, indent=2)}</div>""",
                    unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            priority = memory.handoff_summary.get("priority", "MEDIUM")
            color = {"HIGH": "#ef4444", "MEDIUM": "#f59e0b", "LOW": "#22c55e"}.get(priority, "#94a3b8")
            st.markdown(f"**Priority:** <span style='color:{color}'>{priority}</span>", unsafe_allow_html=True)
        with col2:
            st.download_button(
                "⬇️ Export JSON",
                data=json.dumps(memory.handoff_summary, indent=2),
                file_name=f"handoff_{memory.session_id}.json",
                mime="application/json",
            )


# ── Chat Input ────────────────────────────────────────────────────────────────
if not memory.is_escalated:
    user_input = st.chat_input("Type your support query here...")
    if user_input:
        # Show user message immediately
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.display_messages.append({"role": "user", "content": user_input})

        memory.add_user_message(user_input)

        with st.spinner("Analysing query..."):
            # 1. Detect persona
            persona = detect_persona(user_input, memory.get_history_for_llm())
            st.session_state.current_persona = persona
            memory.update_persona(persona.persona)

            # 2. Retrieve relevant docs
            chunks = retrieve(user_input)
            memory.update_chunks(chunks)
            sources = list({c.source for c in chunks if c.is_relevant})

            # 3. Check escalation BEFORE generating response
            escalation = check_escalation(
                message=user_input,
                persona=persona,
                retrieved_chunks=chunks,
                conversation_history=memory.get_history_for_llm(),
                turn_count=memory.turn_count,
                frustrated_turn_count=memory.frustrated_turn_count,
            )

            # 4. Generate response
            response_text = generate_response(
                message=user_input,
                persona=persona,
                retrieved_chunks=chunks,
                conversation_history=memory.get_history_for_llm()[:-1],  # exclude current user msg
            )

            memory.add_assistant_message(response_text)

            # 5. Handle escalation
            if escalation.should_escalate:
                summary = generate_handoff_summary(
                    session_id=memory.session_id,
                    persona=persona,
                    escalation=escalation,
                    conversation_history=memory.get_history_for_llm(),
                    retrieved_chunks=memory.retrieved_chunks,
                )
                memory.mark_escalated(summary)

        # Show AI response
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(response_text)
            if sources:
                chips_html = "".join(f'<span class="source-chip">📄 {s}</span>' for s in sources)
                st.markdown(f"<div style='margin-top:6px'>{chips_html}</div>", unsafe_allow_html=True)
            if escalation.should_escalate:
                st.markdown("""
<div class="escalation-banner">
⚠️ <strong>Escalated to Human Agent</strong> — This conversation has been flagged for human review.
</div>
""", unsafe_allow_html=True)

        st.session_state.display_messages.append({
            "role": "assistant",
            "content": response_text,
            "sources": sources,
            "escalated": escalation.should_escalate,
        })

        st.rerun()

else:
    st.info("This session has been escalated. Start a new session to continue.")
