"""
Loads support documents from the /data directory.
Handles .txt, .md, and .pdf files.
Returns a list of dicts: {content, source, page}
"""

from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Document:
    content: str
    source: str       # filename
    page: int = 1     # page number (for PDFs) or section index


def load_text_file(path: Path) -> list[Document]:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().strip()
    if not content:
        return []
    return [Document(content=content, source=path.name, page=1)]


def load_pdf_file(path: Path) -> list[Document]:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("Install pypdf: pip install pypdf")

    reader = PdfReader(str(path))
    docs = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            docs.append(Document(content=text, source=path.name, page=i))
    return docs


def load_all_documents(data_dir: str = "./data") -> list[Document]:
    """Walk the data directory and load every supported file."""
    root = Path(data_dir)
    all_docs: list[Document] = []

    loaders = {
        ".txt": load_text_file,
        ".md": load_text_file,
        ".pdf": load_pdf_file,
    }

    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue
        ext = file_path.suffix.lower()
        if ext not in loaders:
            continue
        try:
            docs = loaders[ext](file_path)
            all_docs.extend(docs)
            print(f"  Loaded {len(docs)} section(s) from {file_path.name}")
        except Exception as e:
            print(f"  Warning: could not load {file_path.name}: {e}")

    print(f"\nTotal documents loaded: {len(all_docs)}")
    return all_docs
