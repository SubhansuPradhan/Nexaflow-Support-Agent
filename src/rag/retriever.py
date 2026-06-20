"""
Retrieves the most relevant chunks from ChromaDB for a given query.
Returns results with similarity scores so the escalation handler
can decide if confidence is too low.
"""

from __future__ import annotations
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from src.rag.embedder import get_chroma_collection
from config import settings

# Load model once at module level (cached)
_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _model


@dataclass
class RetrievedChunk:
    text: str
    source: str
    page: int
    similarity: float   # 1.0 = identical, 0.0 = unrelated

    @property
    def is_relevant(self) -> bool:
        return self.similarity >= (1.0 - settings.LOW_CONFIDENCE_THRESHOLD)


def retrieve(query: str, top_k: int = settings.TOP_K_RESULTS) -> list[RetrievedChunk]:
    """Return top-k relevant chunks for the query, sorted by similarity."""
    model = _get_model()
    collection = get_chroma_collection()

    if collection.count() == 0:
        return []

    query_embedding = model.encode([query]).tolist()

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    chunks: list[RetrievedChunk] = []
    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, dist in zip(docs, metas, distances):
        # Cosine distance: 0=identical, higher=less similar
        # Convert to similarity score (1 = perfect, 0 = irrelevant)
        similarity = max(0.0, 1.0 - dist)
        chunks.append(
            RetrievedChunk(
                text=doc,
                source=meta.get("source", "unknown"),
                page=int(meta.get("page", 1)),
                similarity=similarity,
            )
        )

    return chunks


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks into a clean context block for the LLM."""
    if not chunks:
        return "No relevant documentation found."

    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(
            f"[Source {i}: {chunk.source}, Page {chunk.page}]\n{chunk.text}"
        )
    return "\n\n---\n\n".join(parts)


def get_unique_sources(chunks: list[RetrievedChunk]) -> list[str]:
    seen = set()
    sources = []
    for c in chunks:
        key = f"{c.source} (p.{c.page})"
        if key not in seen:
            seen.add(key)
            sources.append(key)
    return sources
