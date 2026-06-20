"""
Splits documents into overlapping chunks for better retrieval coverage.
No external dependencies - pure Python.
"""

from __future__ import annotations
from dataclasses import dataclass
from src.rag.document_loader import Document
from config import settings


@dataclass
class Chunk:
    text: str
    source: str
    page: int
    chunk_index: int

    @property
    def chunk_id(self) -> str:
        return f"{self.source}__p{self.page}__c{self.chunk_index}"


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Recursive-style character splitter with overlap."""
    # First try to split on double newlines (paragraphs)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 <= chunk_size:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            # If a single paragraph is bigger than chunk_size, hard-split it
            if len(para) > chunk_size:
                start = 0
                while start < len(para):
                    end = start + chunk_size
                    chunks.append(para[start:end])
                    start = end - overlap
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = settings.CHUNK_SIZE,
    overlap: int = settings.CHUNK_OVERLAP,
) -> list[Chunk]:
    all_chunks: list[Chunk] = []

    for doc in documents:
        raw_chunks = _split_text(doc.content, chunk_size, overlap)
        for i, text in enumerate(raw_chunks):
            if text.strip():
                all_chunks.append(
                    Chunk(
                        text=text.strip(),
                        source=doc.source,
                        page=doc.page,
                        chunk_index=i,
                    )
                )

    print(f"Total chunks created: {len(all_chunks)}")
    return all_chunks
