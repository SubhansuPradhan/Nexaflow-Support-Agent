"""
Generates embeddings using sentence-transformers (free, no API key needed)
and stores them in ChromaDB with cosine similarity.
"""

from __future__ import annotations
import chromadb
from sentence_transformers import SentenceTransformer
from src.rag.chunker import Chunk
from config import settings


def get_chroma_collection() -> chromadb.Collection:
    client = chromadb.PersistentClient(path=settings.CHROMA_PERSIST_DIR)
    collection = client.get_or_create_collection(
        name=settings.CHROMA_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    return collection


def build_index(chunks: list[Chunk]) -> None:
    """Embed all chunks and upsert into ChromaDB. Safe to re-run."""
    print(f"\nLoading embedding model: {settings.EMBEDDING_MODEL}")
    model = SentenceTransformer(settings.EMBEDDING_MODEL)

    collection = get_chroma_collection()

    texts = [c.text for c in chunks]
    ids = [c.chunk_id for c in chunks]
    metadatas = [{"source": c.source, "page": c.page, "chunk_index": c.chunk_index} for c in chunks]

    print(f"Encoding {len(texts)} chunks...")
    embeddings = model.encode(texts, show_progress_bar=True, batch_size=32).tolist()

    # Upsert in batches of 100
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        collection.upsert(
            ids=ids[i : i + batch_size],
            embeddings=embeddings[i : i + batch_size],
            documents=texts[i : i + batch_size],
            metadatas=metadatas[i : i + batch_size],
        )

    print(f"Index built: {collection.count()} chunks in ChromaDB")
