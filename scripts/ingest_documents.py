"""
One-time ingestion script.
Run this FIRST before starting the support agent.

Usage:
    python scripts/ingest_documents.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.rag.document_loader import load_all_documents
from src.rag.chunker import chunk_documents
from src.rag.embedder import build_index, get_chroma_collection
from config import settings


def generate_pdf(output_path: str) -> None:
    """Generate the required PDF document using reportlab."""
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.units import cm
    except ImportError:
        print("  reportlab not installed. Skipping PDF generation.")
        print("  Run: pip install reportlab")
        return

    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story = []

    title = Paragraph("NexaFlow Refund and Cancellation Policy", styles["Title"])
    story.append(title)
    story.append(Spacer(1, 0.5*cm))

    content = [
        ("Refund Policy", """
NexaFlow offers a 14-day money-back guarantee on all paid plans for new customers. Refund requests
must be submitted within 14 days of the initial purchase date. Refunds are not available for
renewal charges, add-on purchases, or accounts that have exceeded fair usage limits.

To request a refund, contact support@nexaflow.io with your account email and order ID. Approved
refunds are processed within 5-7 business days to the original payment method.
"""),
        ("Cancellation Policy", """
You may cancel your NexaFlow subscription at any time. Cancellation takes effect at the end of
the current billing cycle. You will retain access to paid features until the cycle ends.

To cancel, navigate to Account Settings > Billing > Cancel Subscription. You will receive a
confirmation email within 24 hours.

Annual subscriptions cancelled after the 14-day refund window are not eligible for pro-rated
refunds. Monthly subscriptions may be cancelled at any time without penalty.
"""),
        ("Disputed Charges", """
If you believe you were charged in error, contact our billing team immediately at billing@nexaflow.io.
Include your transaction ID and a description of the issue. We investigate all disputes within
3 business days. Unresolved billing disputes should be escalated to a senior billing specialist.
"""),
        ("Account Suspension Policy", """
Accounts may be suspended for non-payment after 7 days past the due date. A grace period warning
email is sent 3 days before suspension. Suspended accounts retain data for 30 days before permanent
deletion. To reinstate a suspended account, settle the outstanding balance via the billing portal.
"""),
    ]

    for heading, body in content:
        story.append(Paragraph(heading, styles["Heading2"]))
        story.append(Spacer(1, 0.2*cm))
        for para in body.strip().split("\n\n"):
            if para.strip():
                story.append(Paragraph(para.strip(), styles["BodyText"]))
                story.append(Spacer(1, 0.3*cm))

    doc.build(story)
    print(f"  Generated PDF: {output_path}")


def main():
    print("=" * 60)
    print("  NexaFlow Support Agent — Document Ingestion")
    print("=" * 60)

    # Generate the required PDF
    pdf_path = os.path.join(settings.DATA_DIR, "pdf", "refund_cancellation_policy.pdf")
    if not os.path.exists(pdf_path):
        print("\nGenerating PDF document...")
        generate_pdf(pdf_path)
    else:
        print(f"\nPDF already exists: {pdf_path}")

    # Check existing index
    collection = get_chroma_collection()
    existing_count = collection.count()
    if existing_count > 0:
        print(f"\nChromaDB already has {existing_count} chunks.")
        answer = input("Re-ingest? (y/N): ").strip().lower()
        if answer != "y":
            print("Skipping ingestion. Existing index retained.")
            return
        # Clear existing collection
        collection.delete(where={"source": {"$ne": ""}})
        print("Cleared existing index.")

    # Load
    print("\nLoading documents...")
    documents = load_all_documents(settings.DATA_DIR)
    if not documents:
        print("No documents found. Add files to the /data directory.")
        return

    # Chunk
    print("\nChunking documents...")
    chunks = chunk_documents(documents)

    # Embed and index
    print("\nBuilding vector index...")
    build_index(chunks)

    print("\n✅ Ingestion complete. You can now start the agent.")
    print("   Streamlit UI: streamlit run src/ui/streamlit_app.py")
    print("   CLI:          python main.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
