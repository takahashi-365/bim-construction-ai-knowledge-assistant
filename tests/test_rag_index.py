from __future__ import annotations

import json
from pathlib import Path
from typing import Any


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 9: pytest for RAG-style keyword index
#
# Target:
#   output/rag_index_v001.json
#
# Purpose:
#   Validate generated simple keyword index.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"
RAG_INDEX_JSON = OUTPUT_DIR / "rag_index_v001.json"


REQUIRED_INDEX_TOP_LEVEL_FIELDS = {
    "index_version",
    "index_type",
    "description",
    "document_count",
    "token_count",
    "documents",
    "inverted_index",
}

REQUIRED_INDEX_DOCUMENT_FIELDS = {
    "document_id",
    "source_poc",
    "source_type",
    "title",
    "rule_id",
    "use_case_id",
    "category",
    "recommended_approach",
    "human_review_required",
    "deep_dive_required",
    "source_file",
    "keywords",
    "tokens",
    "search_text",
}


def load_json(path: Path) -> dict[str, Any]:
    """
    Load JSON file.
    """
    assert path.exists(), f"File does not exist: {path}"

    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, dict), "RAG index should be a JSON object."

    return data


def test_rag_index_file_exists() -> None:
    """
    rag_index_v001.json should exist.
    """
    assert RAG_INDEX_JSON.exists()


def test_rag_index_has_required_top_level_fields() -> None:
    """
    RAG index should have required top-level fields.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    missing_fields = REQUIRED_INDEX_TOP_LEVEL_FIELDS - set(rag_index.keys())

    assert not missing_fields, (
        f"rag_index_v001.json is missing fields: {missing_fields}"
    )


def test_rag_index_type_is_simple_keyword_index() -> None:
    """
    Index type should clearly show this is a simple keyword index.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert rag_index["index_type"] == "simple_keyword_index"


def test_rag_index_description_does_not_claim_vector_search() -> None:
    """
    Description should not overstate the implementation as vector search.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    description = rag_index.get("description", "")

    assert "not an embedding index" in description
    assert "vector database" in description


def test_rag_index_documents_is_list() -> None:
    """
    documents should be a list.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert isinstance(rag_index["documents"], list)


def test_rag_index_documents_are_not_empty() -> None:
    """
    documents should contain one or more index entries.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert len(rag_index["documents"]) > 0


def test_rag_index_document_count_matches_documents_length() -> None:
    """
    document_count should match the number of documents.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert rag_index["document_count"] == len(rag_index["documents"])


def test_rag_index_inverted_index_is_dict() -> None:
    """
    inverted_index should be a dictionary.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert isinstance(rag_index["inverted_index"], dict)


def test_rag_index_inverted_index_is_not_empty() -> None:
    """
    inverted_index should contain one or more tokens.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert len(rag_index["inverted_index"]) > 0


def test_rag_index_token_count_matches_inverted_index_length() -> None:
    """
    token_count should match the number of keys in inverted_index.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    assert rag_index["token_count"] == len(rag_index["inverted_index"])


def test_all_index_documents_have_required_fields() -> None:
    """
    Each index document should have required fields.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    for document in rag_index["documents"]:
        missing_fields = REQUIRED_INDEX_DOCUMENT_FIELDS - set(document.keys())

        assert not missing_fields, (
            f"Index document {document.get('document_id')} is missing fields: "
            f"{missing_fields}"
        )


def test_index_document_ids_are_unique() -> None:
    """
    document_id values in index should be unique.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    document_ids = [
        document["document_id"]
        for document in rag_index["documents"]
    ]

    assert len(document_ids) == len(set(document_ids)), (
        "Duplicate document_id found in rag_index_v001.json."
    )


def test_index_document_required_text_fields_are_not_empty() -> None:
    """
    document_id, source_poc, source_type, title, and search_text should not be empty.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    for document in rag_index["documents"]:
        document_id = document["document_id"]

        assert document["document_id"], "document_id is empty."
        assert document["source_poc"], f"source_poc is empty: {document_id}"
        assert document["source_type"], f"source_type is empty: {document_id}"
        assert document["title"], f"title is empty: {document_id}"
        assert document["search_text"], f"search_text is empty: {document_id}"


def test_index_keywords_and_tokens_are_lists() -> None:
    """
    keywords and tokens should be lists.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    for document in rag_index["documents"]:
        document_id = document["document_id"]

        assert isinstance(document["keywords"], list), (
            f"keywords must be list: {document_id}"
        )

        assert isinstance(document["tokens"], list), (
            f"tokens must be list: {document_id}"
        )


def test_each_index_document_has_tokens() -> None:
    """
    Each index document should have at least one token.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    for document in rag_index["documents"]:
        document_id = document["document_id"]

        assert len(document["tokens"]) > 0, (
            f"tokens should not be empty: {document_id}"
        )


def test_human_review_and_deep_dive_flags_are_booleans() -> None:
    """
    human_review_required and deep_dive_required should be booleans.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    for document in rag_index["documents"]:
        document_id = document["document_id"]

        assert isinstance(document["human_review_required"], bool), (
            f"human_review_required must be bool: {document_id}"
        )

        assert isinstance(document["deep_dive_required"], bool), (
            f"deep_dive_required must be bool: {document_id}"
        )


def test_inverted_index_values_are_document_id_lists() -> None:
    """
    Each inverted_index value should be a list of document IDs.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    all_document_ids = {
        document["document_id"]
        for document in rag_index["documents"]
    }

    for token, document_ids in rag_index["inverted_index"].items():
        assert isinstance(token, str), "inverted_index token should be string."
        assert token, "inverted_index token should not be empty."
        assert isinstance(document_ids, list), (
            f"inverted_index value should be list: {token}"
        )
        assert len(document_ids) > 0, (
            f"inverted_index value should not be empty: {token}"
        )

        for document_id in document_ids:
            assert document_id in all_document_ids, (
                f"inverted_index references unknown document_id: {document_id}"
            )


def test_inverted_index_contains_expected_terms() -> None:
    """
    Inverted index should contain important search terms.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    inverted_index = rag_index["inverted_index"]

    expected_terms = [
        "door",
        "room",
        "rag",
        "human",
        "review",
    ]

    for term in expected_terms:
        assert term in inverted_index, (
            f"Expected term not found in inverted_index: {term}"
        )


def test_index_contains_poc1_and_poc2_documents() -> None:
    """
    Index should include both PoC1 and PoC2 documents.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    source_pocs = {
        document["source_poc"]
        for document in rag_index["documents"]
    }

    assert "PoC1" in source_pocs
    assert "PoC2" in source_pocs


def test_index_contains_rule_and_use_case_documents() -> None:
    """
    Index should contain both RuleMaster and UseCaseMapping documents.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    source_types = {
        document["source_type"]
        for document in rag_index["documents"]
    }

    assert "RuleMaster" in source_types
    assert "UseCaseMapping" in source_types


def test_index_contains_door_rule_d001() -> None:
    """
    Index should contain Door RuleId D-001.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    matching_documents = [
        document for document in rag_index["documents"]
        if document["rule_id"] == "D-001"
    ]

    assert len(matching_documents) > 0


def test_index_contains_room_rule_r101() -> None:
    """
    Index should contain Room RuleId R-101.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    matching_documents = [
        document for document in rag_index["documents"]
        if document["rule_id"] == "R-101"
    ]

    assert len(matching_documents) > 0


def test_index_contains_use_case_uc001() -> None:
    """
    Index should contain UseCaseId UC-001.
    """
    rag_index = load_json(RAG_INDEX_JSON)

    matching_documents = [
        document for document in rag_index["documents"]
        if document["use_case_id"] == "UC-001"
    ]

    assert len(matching_documents) > 0


def test_no_prohibited_final_decision_phrases_in_index() -> None:
    """
    Index should not include prohibited final-decision expressions.
    """
    rag_index = load_json(RAG_INDEX_JSON)

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

    index_text = json.dumps(rag_index, ensure_ascii=False)

    for phrase in prohibited_phrases:
        assert phrase not in index_text, (
            f"Prohibited phrase found in rag_index_v001.json: {phrase}"
        )