"""
CLI entry point for the NexaFlow Support Agent.
Uses `rich` for professional terminal output.

Run: python main.py
"""

import sys
import os
import json

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich import box

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.agent.persona_detector import detect_persona, PERSONA_ICONS
from src.agent.response_generator import generate_response
from src.agent.escalation_handler import check_escalation
from src.agent.handoff_summary import generate_handoff_summary
from src.memory.conversation_memory import ConversationMemory
from src.rag.retriever import retrieve, get_unique_sources
from config import settings

console = Console()

PERSONA_COLORS = {
    "TECHNICAL_EXPERT": "cyan",
    "FRUSTRATED_USER": "red",
    "BUSINESS_EXECUTIVE": "yellow",
}

PRIORITY_COLORS = {
    "HIGH": "bright_red",
    "MEDIUM": "yellow",
    "LOW": "green",
    "NONE": "dim",
}


def print_header():
    console.print(Panel(
        "[bold blue]NexaFlow Persona-Adaptive Support Agent[/bold blue]\n"
        "[dim]Type your support query. Type 'quit' or 'exit' to end.[/dim]",
        box=box.DOUBLE,
        expand=False,
        padding=(1, 4),
    ))


def print_persona(persona):
    icon = persona.icon
    color = PERSONA_COLORS.get(persona.persona, "white")
    conf_pct = int(persona.confidence * 100)
    bar = "█" * (conf_pct // 5) + "░" * (20 - conf_pct // 5)
    console.print(
        f"\n  [{color}]{icon} {persona.display_name}[/{color}]  "
        f"[dim]{bar} {conf_pct}%[/dim]  "
        f"[dim italic]{persona.reasoning}[/dim italic]"
    )


def print_sources(sources: list[str]):
    if not sources:
        return
    chips = "  ".join(f"[dim]📄 {s}[/dim]" for s in sources)
    console.print(f"  Sources: {chips}")


def print_response(text: str):
    console.print(Panel(
        text,
        title="[bold green]Support Agent[/bold green]",
        border_style="green",
        padding=(1, 2),
    ))


def print_escalation(escalation, summary: dict):
    priority_color = PRIORITY_COLORS.get(escalation.priority, "white")
    console.print(Panel(
        f"[bold red]⚠ ESCALATED TO HUMAN AGENT[/bold red]\n\n"
        f"Priority: [{priority_color}]{escalation.priority}[/{priority_color}]\n"
        f"Reason: [italic]{escalation.reason}[/italic]",
        border_style="red",
        padding=(1, 2),
    ))

    console.print("\n[bold]Handoff Summary:[/bold]")
    console.print_json(json.dumps(summary, indent=2))


def run_cli():
    print_header()

    # Validate API key
    if not settings.GEMINI_API_KEY:
        console.print("[red]Error: GEMINI_API_KEY not set. Copy .env.example to .env and add your key.[/red]")
        sys.exit(1)

    # Check ChromaDB
    from src.rag.embedder import get_chroma_collection
    collection = get_chroma_collection()
    if collection.count() == 0:
        console.print("[yellow]Warning: No documents in vector index. Run:[/yellow]")
        console.print("  [bold]python scripts/ingest_documents.py[/bold]")

    memory = ConversationMemory()
    console.print(f"\n[dim]Session: {memory.session_id}[/dim]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold blue]You[/bold blue]").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "bye"):
            console.print("[dim]Ending session. Goodbye.[/dim]")
            break

        memory.add_user_message(user_input)

        with console.status("[dim]Thinking...[/dim]"):
            # 1. Detect persona
            persona = detect_persona(user_input, memory.get_history_for_llm())
            memory.update_persona(persona.persona)

            # 2. Retrieve
            chunks = retrieve(user_input)
            memory.update_chunks(chunks)
            sources = get_unique_sources([c for c in chunks if c.is_relevant])

            # 3. Check escalation
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
                conversation_history=memory.get_history_for_llm()[:-1],
            )

            memory.add_assistant_message(response_text)

        # Display
        print_persona(persona)
        print_response(response_text)
        print_sources(sources)

        if escalation.should_escalate:
            summary = generate_handoff_summary(
                session_id=memory.session_id,
                persona=persona,
                escalation=escalation,
                conversation_history=memory.get_history_for_llm(),
                retrieved_chunks=memory.retrieved_chunks,
            )
            memory.mark_escalated(summary)
            print_escalation(escalation, summary)
            console.print("\n[red]Session ended — escalated to human agent.[/red]")
            break

        console.print()


if __name__ == "__main__":
    run_cli()
