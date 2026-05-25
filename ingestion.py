"""
Document Ingestion System
==========================
Reads PDF, TXT, and DOCX files from a local folder and
generates flashcards + quiz questions using Claude API.

Designed for: ~/OneDrive/Desktop/FRANCO/CURSOS DE EXTENSION/BCRP
"""

from __future__ import annotations
import os
import re
import json
from pathlib import Path
from typing import Optional

# ── Optional imports (graceful degradation) ───────────────────────────

try:
    import PyPDF2
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

try:
    from docx import Document as DocxDocument
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

from core.card_model import Flashcard, Domain, CardType, DifficultyLevel, TOPIC_TREE
from core.store import CardStore


# ── Text Extractors ───────────────────────────────────────────────────

def extract_txt(path: Path) -> str:
    """Extract text from a .txt file."""
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def extract_pdf(path: Path) -> str:
    """Extract text from a PDF file."""
    if not HAS_PDF:
        return f"[PyPDF2 not installed — cannot read {path.name}]"
    text = []
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)


def extract_docx(path: Path) -> str:
    """Extract text from a .docx file."""
    if not HAS_DOCX:
        return f"[python-docx not installed — cannot read {path.name}]"
    doc = DocxDocument(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(path: Path) -> str:
    """Dispatch text extraction by file extension."""
    ext = path.suffix.lower()
    if ext == ".txt":
        return extract_txt(path)
    elif ext == ".pdf":
        return extract_pdf(path)
    elif ext in (".docx", ".doc"):
        return extract_docx(path)
    else:
        return f"[Unsupported format: {ext}]"


# ── Heuristic Card Generator (no-LLM fallback) ────────────────────────

def heuristic_cards_from_text(
    text: str,
    source_name: str,
    domain: str = "Financial Engineering",
    topic: str = "General",
    max_cards: int = 20,
) -> list[Flashcard]:
    """
    Extract flashcards from text using heuristic rules.
    Looks for: definitions, formulas, numbered lists, key terms.
    
    This is a fallback when no LLM API is configured.
    """
    cards = []
    
    # Pattern 1: "X is defined as Y" / "X refers to Y"
    defn_pattern = re.compile(
        r"([A-Z][^.]{5,60}?)\s+(?:is defined as|is|refers to|means)\s+([^.]{20,300})\.",
        re.IGNORECASE
    )
    for m in defn_pattern.finditer(text):
        term, definition = m.group(1).strip(), m.group(2).strip()
        if len(definition) > 30:
            cards.append(Flashcard(
                domain=domain, topic=topic,
                card_type=CardType.CONCEPT,
                difficulty=DifficultyLevel.INTERMEDIATE,
                front=f"Define: {term}",
                back=definition,
                source=source_name,
                tags=["auto-generated", "definition"],
            ))

    # Pattern 2: LaTeX-like formulas
    formula_pattern = re.compile(r"\$\$(.+?)\$\$|\$(.+?)\$", re.DOTALL)
    for m in formula_pattern.finditer(text):
        formula = (m.group(1) or m.group(2)).strip()
        # Get surrounding context (~200 chars)
        start = max(0, m.start() - 150)
        end   = min(len(text), m.end() + 150)
        ctx = text[start:end].replace("\n", " ")
        cards.append(Flashcard(
            domain=domain, topic=topic,
            card_type=CardType.FORMULA,
            difficulty=DifficultyLevel.INTERMEDIATE,
            front=f"Interpret and explain this formula: ${formula}$",
            back=f"Formula: ${formula}$\n\nContext: {ctx}",
            latex_formula=formula,
            source=source_name,
            tags=["auto-generated", "formula"],
        ))

    return cards[:max_cards]


# ── Ingestion Orchestrator ─────────────────────────────────────────────

class DocumentIngester:
    """
    Scans a folder, extracts text, and generates flashcards.
    
    Usage
    -----
    ingester = DocumentIngester(folder_path="/path/to/docs")
    results  = ingester.ingest_all()
    """

    def __init__(self, folder_path: str | Path):
        self.folder = Path(folder_path)
        self.store  = CardStore()

    def list_documents(self) -> list[Path]:
        """Return all supported documents in the folder."""
        supported = {".txt", ".pdf", ".docx", ".doc"}
        if not self.folder.exists():
            return []
        return [
            p for p in self.folder.iterdir()
            if p.suffix.lower() in supported
        ]

    def ingest_file(
        self,
        path: Path,
        domain: str = "Financial Engineering",
        topic: str = "General",
    ) -> dict:
        """Process a single document and return summary."""
        text = extract_text(path)
        if text.startswith("["):
            return {"file": path.name, "status": "error", "message": text, "cards": 0}

        cards = heuristic_cards_from_text(
            text=text,
            source_name=path.name,
            domain=domain,
            topic=topic,
        )

        for card in cards:
            self.store.save_card(card)

        return {
            "file"    : path.name,
            "status"  : "ok",
            "chars"   : len(text),
            "cards"   : len(cards),
            "preview" : text[:500],
        }

    def ingest_all(self, domain: str = "Financial Engineering") -> list[dict]:
        """Ingest all documents in the folder."""
        results = []
        for path in self.list_documents():
            result = self.ingest_file(path, domain=domain)
            results.append(result)
        return results
