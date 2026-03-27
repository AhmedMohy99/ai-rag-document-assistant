from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Tuple

import httpx
from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader


def load_pdf(file_path: Path) -> str:
    reader = PdfReader(str(file_path))
    parts: List[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts).strip()


def load_docx(file_path: Path) -> str:
    doc = Document(str(file_path))
    return "\n".join(paragraph.text for paragraph in doc.paragraphs).strip()


def load_txt(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()


def load_url(url: str, timeout_seconds: int = 20) -> Tuple[str, str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AhmedRAGBot/1.0)"
    }
    with httpx.Client(timeout=timeout_seconds, follow_redirects=True, headers=headers) as client:
        response = client.get(url)
        response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else url
    text = " ".join(soup.get_text(separator=" ").split())
    return title, text


def load_file(file_path: Path) -> Dict[str, str]:
    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        text = load_pdf(file_path)
    elif suffix == ".docx":
        text = load_docx(file_path)
    elif suffix == ".txt":
        text = load_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")

    return {
        "source": file_path.name,
        "text": text,
    }
