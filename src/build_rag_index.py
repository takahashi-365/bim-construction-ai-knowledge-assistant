from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 5: Build simple RAG-style index
#
# Input:
#   output/rag_documents_v001.jsonl
#
# Output:
#   output/rag_index_v001.json
#
# Purpose:
#   Build a simple local keyword index from RAG-style documents.
#   This is not a vector index.
#   This is a lightweight MVP index for keyword-based retrieval.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"

RAG_DOCUMENTS_JSONL = OUTPUT_DIR / "rag_documents_v001.jsonl"
RAG_INDEX_JSON = OUTPUT_DIR / "rag_index_v001.json"


def load_jsonl(jsonl_path: Path) -> list[dict[str, Any]]:
    """
    Load JSONL file.

    Each line is expected to be one JSON object.
    """
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Input file not found: {jsonl_path}")

    documents: list[dict[str, Any]] = []

    with jsonl_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                document = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid JSON at line {line_number} in {jsonl_path}: {e}"
                ) from e

            documents.append(document)

    return documents


def normalize_text(value: Any) -> str:
    """
    Normalize text for simple keyword matching.

    This MVP normalization keeps Japanese text as-is and lowercases
    English text. It also normalizes extra spaces.
    """
    if value is None:
        return ""

    text = str(value).lower()
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_simple(text: str) -> list[str]:
    """
    Create simple tokens for MVP keyword search.

    This is intentionally simple:
    - keeps Japanese terms from explicit keyword lists
    - splits English-like text by non-word characters
    - removes very short noise tokens
    """
    normalized = normalize_text(text)

    raw_tokens = re.split(r"[^\w\u3040-\u30ff\u3400-\u9fff]+", normalized)

    tokens: list[str] = []
    for token in raw_tokens:
        token = token.strip()
        if not token:
            continue

        # Keep Japanese tokens even if short.
        has_japanese = bool(re.search(r"[\u3040-\u30ff\u3400-\u9fff]", token))

        if has_japanese or len(token) >= 2:
            tokens.append(token)

    return tokens


def flatten_metadata(metadata: dict[str, Any]) -> str:
    """
    Convert metadata values into searchable text.
    """
    values: list[str] = []

    for value in metadata.values():
        if isinstance(value, bool):
            values.append(str(value))
        elif isinstance(value, list):
            values.extend(str(item) for item in value)
        elif value is not None:
            values.append(str(value))

    return " ".join(values)


def build_search_text(document: dict[str, Any]) -> str:
    """
    Build searchable text from one RAG-style document.
    """
    title = document.get("title", "")
    content = document.get("content", "")
    source_poc = document.get("source_poc", "")
    source_type = document.get("source_type", "")
    keywords = document.get("keywords", [])
    metadata = document.get("metadata", {})

    if not isinstance(keywords, list):
        keywords = []

    if not isinstance(metadata, dict):
        metadata = {}

    keyword_text = " ".join(str(keyword) for keyword in keywords)
    metadata_text = flatten_metadata(metadata)

    return " ".join(
        [
            str(title),
            str(content),
            str(source_poc),
            str(source_type),
            keyword_text,
            metadata_text,
        ]
    )


def build_index_entry(document: dict[str, Any]) -> dict[str, Any]:
    """
    Build one index entry for a RAG-style document.
    """
    document_id = document.get("document_id", "")
    metadata = document.get("metadata", {})

    if not isinstance(metadata, dict):
        metadata = {}

    search_text = build_search_text(document)
    tokens = tokenize_simple(search_text)

    # Deduplicate tokens while preserving order.
    unique_tokens = list(dict.fromkeys(tokens))

    return {
        "document_id": document_id,
        "source_poc": document.get("source_poc", ""),
        "source_type": document.get("source_type", ""),
        "title": document.get("title", ""),
        "rule_id": metadata.get("rule_id", ""),
        "use_case_id": metadata.get("use_case_id", ""),
        "category": metadata.get("category", ""),
        "recommended_approach": metadata.get("recommended_approach", ""),
        "human_review_required": metadata.get("human_review_required", False),
        "deep_dive_required": metadata.get("deep_dive_required", False),
        "source_file": metadata.get("source_file", ""),
        "keywords": document.get("keywords", []),
        "tokens": unique_tokens,
        "search_text": normalize_text(search_text),
    }


def validate_index_entry(entry: dict[str, Any]) -> None:
    """
    Validate minimum fields for index entries.
    """
    required_fields = [
        "document_id",
        "source_poc",
        "source_type",
        "title",
        "keywords",
        "tokens",
        "search_text",
    ]

    for field in required_fields:
        if field not in entry:
            raise ValueError(f"Missing required index field '{field}': {entry}")

    if not entry["document_id"]:
        raise ValueError(f"document_id is empty in index entry: {entry}")

    if not isinstance(entry["keywords"], list):
        raise ValueError(f"keywords must be a list: {entry['document_id']}")

    if not isinstance(entry["tokens"], list):
        raise ValueError(f"tokens must be a list: {entry['document_id']}")

    if not entry["search_text"]:
        raise ValueError(f"search_text is empty: {entry['document_id']}")


def build_inverted_index(index_entries: list[dict[str, Any]]) -> dict[str, list[str]]:
    """
    Build a simple inverted index.

    Format:
        {
          "door": ["P1-RULE-D001", "P1-FIX-F001"],
          "room": ["P1-RULE-R101", "P2-USECASE-UC005"]
        }
    """
    inverted_index: dict[str, list[str]] = {}

    for entry in index_entries:
        document_id = entry["document_id"]

        for token in entry["tokens"]:
            if token not in inverted_index:
                inverted_index[token] = []

            if document_id not in inverted_index[token]:
                inverted_index[token].append(document_id)

    return inverted_index


def build_rag_index(documents: list[dict[str, Any]]) -> dict[str, Any]:
    """
    Build the complete MVP index.
    """
    index_entries: list[dict[str, Any]] = []

    for document in documents:
        entry = build_index_entry(document)
        validate_index_entry(entry)
        index_entries.append(entry)

    inverted_index = build_inverted_index(index_entries)

    return {
        "index_version": "v001",
        "index_type": "simple_keyword_index",
        "description": (
            "Local MVP keyword index for PoC 3. "
            "This is not an embedding index or vector database."
        ),
        "document_count": len(index_entries),
        "token_count": len(inverted_index),
        "documents": index_entries,
        "inverted_index": inverted_index,
    }


def write_json(data: dict[str, Any], output_path: Path) -> None:
    """
    Write JSON file with readable Japanese text.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main() -> None:
    """
    Entry point.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)
    rag_index = build_rag_index(documents)
    write_json(rag_index, RAG_INDEX_JSON)

    poc1_count = sum(1 for doc in rag_index["documents"] if doc["source_poc"] == "PoC1")
    poc2_count = sum(1 for doc in rag_index["documents"] if doc["source_poc"] == "PoC2")

    print("RAG-style keyword index generated successfully.")
    print(f"Input: {RAG_DOCUMENTS_JSONL}")
    print(f"Output: {RAG_INDEX_JSON}")
    print(f"Total documents: {rag_index['document_count']}")
    print(f"PoC1 documents: {poc1_count}")
    print(f"PoC2 documents: {poc2_count}")
    print(f"Unique tokens: {rag_index['token_count']}")


if __name__ == "__main__":
    main()