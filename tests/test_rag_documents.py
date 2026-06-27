from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 9: pytest for RAG-style documents
#
# Target:
#   output/rag_documents_v001.jsonl
#
# Purpose:
#   Validate generated RAG-style documents.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"
RAG_DOCUMENTS_JSONL = OUTPUT_DIR / "rag_documents_v001.jsonl"


REQUIRED_TOP_LEVEL_FIELDS = {
    "document_id",
    "source_poc",
    "source_type",
    "title",
    "content",
    "metadata",
    "keywords",
}

REQUIRED_METADATA_FIELDS = {
    "category",
    "rule_id",
    "use_case_id",
    "severity",
    "recommended_approach",
    "human_review_required",
    "deep_dive_required",
    "source_file",
}


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    """
    Load JSONL file as a list of dictionaries.
    """
    assert path.exists(), f"File does not exist: {path}"

    documents: list[dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                documents.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise AssertionError(
                    f"Invalid JSON at line {line_number}: {e}"
                ) from e

    return documents


def test_rag_documents_file_exists() -> None:
    """
    rag_documents_v001.jsonl should exist.
    """
    assert RAG_DOCUMENTS_JSONL.exists()


def test_rag_documents_are_not_empty() -> None:
    """
    rag_documents_v001.jsonl should contain one or more documents.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    assert len(documents) > 0


def test_all_documents_have_required_top_level_fields() -> None:
    """
    Each document should have required top-level fields.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    for document in documents:
        missing_fields = REQUIRED_TOP_LEVEL_FIELDS - set(document.keys())

        assert not missing_fields, (
            f"Document {document.get('document_id')} is missing fields: "
            f"{missing_fields}"
        )


def test_all_documents_have_required_metadata_fields() -> None:
    """
    Each document should have required metadata fields.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    for document in documents:
        metadata = document.get("metadata")

        assert isinstance(metadata, dict), (
            f"metadata must be dict: {document.get('document_id')}"
        )

        missing_fields = REQUIRED_METADATA_FIELDS - set(metadata.keys())

        assert not missing_fields, (
            f"Document {document.get('document_id')} metadata is missing fields: "
            f"{missing_fields}"
        )


def test_document_ids_are_unique() -> None:
    """
    document_id should be unique.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    document_ids = [document["document_id"] for document in documents]

    assert len(document_ids) == len(set(document_ids)), (
        "Duplicate document_id found."
    )


def test_document_ids_are_not_empty() -> None:
    """
    document_id should not be empty.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    for document in documents:
        assert document["document_id"], "document_id is empty."


def test_required_text_fields_are_not_empty() -> None:
    """
    source_poc, source_type, title, and content should not be empty.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    for document in documents:
        document_id = document["document_id"]

        assert document["source_poc"], f"source_poc is empty: {document_id}"
        assert document["source_type"], f"source_type is empty: {document_id}"
        assert document["title"], f"title is empty: {document_id}"
        assert document["content"], f"content is empty: {document_id}"


def test_keywords_are_lists() -> None:
    """
    keywords should be a list.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    for document in documents:
        document_id = document["document_id"]

        assert isinstance(document["keywords"], list), (
            f"keywords must be list: {document_id}"
        )


def test_human_review_and_deep_dive_are_booleans() -> None:
    """
    human_review_required and deep_dive_required should be booleans.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    for document in documents:
        document_id = document["document_id"]
        metadata = document["metadata"]

        assert isinstance(metadata["human_review_required"], bool), (
            f"human_review_required must be bool: {document_id}"
        )

        assert isinstance(metadata["deep_dive_required"], bool), (
            f"deep_dive_required must be bool: {document_id}"
        )


def test_contains_poc1_documents() -> None:
    """
    Documents should include PoC1 knowledge.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    poc1_documents = [
        document for document in documents
        if document["source_poc"] == "PoC1"
    ]

    assert len(poc1_documents) > 0


def test_contains_poc2_documents() -> None:
    """
    Documents should include PoC2 knowledge.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    poc2_documents = [
        document for document in documents
        if document["source_poc"] == "PoC2"
    ]

    assert len(poc2_documents) > 0


def test_contains_rule_master_documents() -> None:
    """
    Documents should include RuleMaster source type.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    rule_master_documents = [
        document for document in documents
        if document["source_type"] == "RuleMaster"
    ]

    assert len(rule_master_documents) > 0


def test_contains_use_case_mapping_documents() -> None:
    """
    Documents should include UseCaseMapping source type.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    use_case_documents = [
        document for document in documents
        if document["source_type"] == "UseCaseMapping"
    ]

    assert len(use_case_documents) > 0


def test_contains_human_review_required_documents() -> None:
    """
    At least one document should require Human Review.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    human_review_documents = [
        document for document in documents
        if document["metadata"]["human_review_required"] is True
    ]

    assert len(human_review_documents) > 0


def test_contains_deep_dive_required_documents() -> None:
    """
    At least one document should require Deep Dive.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    deep_dive_documents = [
        document for document in documents
        if document["metadata"]["deep_dive_required"] is True
    ]

    assert len(deep_dive_documents) > 0


def test_contains_door_rule_document() -> None:
    """
    Door RuleId D-001 should be included.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    matching_documents = [
        document for document in documents
        if document["metadata"].get("rule_id") == "D-001"
    ]

    assert len(matching_documents) > 0


def test_contains_room_rule_document() -> None:
    """
    Room RuleId R-101 should be included.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    matching_documents = [
        document for document in documents
        if document["metadata"].get("rule_id") == "R-101"
    ]

    assert len(matching_documents) > 0


def test_contains_use_case_id_document() -> None:
    """
    UseCaseId UC-001 should be included.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    matching_documents = [
        document for document in documents
        if document["metadata"].get("use_case_id") == "UC-001"
    ]

    assert len(matching_documents) > 0


def test_no_prohibited_final_decision_phrases() -> None:
    """
    Documents should not include prohibited final-decision expressions.
    """
    documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    prohibited_phrases = [
        "AIが最終判断します",
        "AIが自動で承認します",
        "AIが設計判断します",
        "AIが施工判断します",
        "AIが法規判断します",
        "AIが安全判断します",
        "AIが契約判断します",
        "Revitモデルを自動修正します",
        "人間確認は不要です",
        "確認なしで実行できます",
        "この判断は確定です",
        "必ず正しいです",
    ]

    for document in documents:
        document_id = document["document_id"]
        document_text = json.dumps(document, ensure_ascii=False)

        for phrase in prohibited_phrases:
            assert phrase not in document_text, (
                f"Prohibited phrase found in {document_id}: {phrase}"
            )