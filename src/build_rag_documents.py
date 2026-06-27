from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 4: Build RAG-style documents
#
# Input:
#   input/poc1_knowledge_samples.csv
#   input/poc2_knowledge_samples.csv
#
# Output:
#   output/rag_documents_v001.jsonl
#
# Purpose:
#   Convert PoC 1 / PoC 2 sample knowledge CSV files into
#   RAG-style Knowledge Documents.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

POC1_INPUT = INPUT_DIR / "poc1_knowledge_samples.csv"
POC2_INPUT = INPUT_DIR / "poc2_knowledge_samples.csv"

OUTPUT_JSONL = OUTPUT_DIR / "rag_documents_v001.jsonl"


TRUE_VALUES = {"true", "True", "TRUE", "1", "yes", "Yes", "YES"}


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """
    Read CSV rows as dictionaries.

    The input CSV files are expected to be UTF-8 encoded.
    If the file does not exist, raise FileNotFoundError with a clear message.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def to_bool(value: Any) -> bool:
    """
    Convert CSV text values into boolean.

    Empty values and unknown values are treated as False.
    """
    if value is None:
        return False

    return str(value).strip() in TRUE_VALUES


def split_keywords(value: str | None) -> list[str]:
    """
    Convert pipe-separated keywords into a clean keyword list.

    Example:
        "door|name|missing" -> ["door", "name", "missing"]
    """
    if not value:
        return []

    keywords = []
    for item in value.split("|"):
        item = item.strip()
        if item:
            keywords.append(item)

    return keywords


def safe_get(row: dict[str, str], key: str, default: str = "") -> str:
    """
    Safely get a CSV value as stripped text.
    """
    value = row.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def build_poc1_content(row: dict[str, str]) -> str:
    """
    Build readable content text for PoC 1 knowledge.

    PoC 1 contains BIM data quality rules, Fix Guides,
    AI Readiness information, AI Context, pyRevit metadata,
    and Human Review policy.
    """
    title = safe_get(row, "Title")
    category = safe_get(row, "Category")
    rule_id = safe_get(row, "RuleId")
    issue = safe_get(row, "IssueDescription")
    check_logic = safe_get(row, "CheckLogic")
    fix_guide = safe_get(row, "FixGuide")
    ai_impact = safe_get(row, "AIReadinessImpact")

    parts = [
        f"Title: {title}",
        f"Category: {category}",
    ]

    if rule_id:
        parts.append(f"RuleId: {rule_id}")

    if issue:
        parts.append(f"Issue: {issue}")

    if check_logic:
        parts.append(f"Check Logic: {check_logic}")

    if fix_guide:
        parts.append(f"Fix Guide: {fix_guide}")

    if ai_impact:
        parts.append(f"AI Readiness Impact: {ai_impact}")

    return "\n".join(parts)


def build_poc2_content(row: dict[str, str]) -> str:
    """
    Build readable content text for PoC 2 knowledge.

    PoC 2 contains BIM / Construction AI use case mapping,
    RecommendedApproach, RAG / BI / Automation suitability,
    Human Review, Deep Dive, and discussion points.
    """
    title = safe_get(row, "Title")
    business_area = safe_get(row, "BusinessArea")
    use_case_id = safe_get(row, "UseCaseId")
    recommended_approach = safe_get(row, "RecommendedApproach")
    description = safe_get(row, "UseCaseDescription")
    input_data = safe_get(row, "InputData")
    process = safe_get(row, "Process")
    output = safe_get(row, "Output")
    discussion_point = safe_get(row, "DiscussionPoint")

    parts = [
        f"Title: {title}",
        f"Business Area: {business_area}",
    ]

    if use_case_id:
        parts.append(f"UseCaseId: {use_case_id}")

    if recommended_approach:
        parts.append(f"Recommended Approach: {recommended_approach}")

    if description:
        parts.append(f"Use Case Description: {description}")

    if input_data:
        parts.append(f"Input Data: {input_data}")

    if process:
        parts.append(f"Process: {process}")

    if output:
        parts.append(f"Output: {output}")

    if discussion_point:
        parts.append(f"Discussion Point: {discussion_point}")

    return "\n".join(parts)


def build_common_metadata(row: dict[str, str]) -> dict[str, Any]:
    """
    Build metadata shared by PoC 1 and PoC 2 documents.
    """
    return {
        "category": safe_get(row, "Category") or safe_get(row, "BusinessArea"),
        "rule_id": safe_get(row, "RuleId"),
        "use_case_id": safe_get(row, "UseCaseId"),
        "severity": safe_get(row, "Severity"),
        "recommended_approach": safe_get(row, "RecommendedApproach"),
        "human_review_required": to_bool(safe_get(row, "HumanReviewRequired")),
        "deep_dive_required": to_bool(safe_get(row, "DeepDiveRequired")),
        "source_file": safe_get(row, "SourceFile"),
    }


def build_poc1_document(row: dict[str, str]) -> dict[str, Any]:
    """
    Convert one PoC 1 CSV row into a RAG-style document.
    """
    knowledge_id = safe_get(row, "KnowledgeId")

    return {
        "document_id": knowledge_id,
        "source_poc": safe_get(row, "SourcePoC"),
        "source_type": safe_get(row, "SourceType"),
        "title": safe_get(row, "Title"),
        "content": build_poc1_content(row),
        "metadata": {
            **build_common_metadata(row),
            "issue_description": safe_get(row, "IssueDescription"),
            "check_logic": safe_get(row, "CheckLogic"),
            "fix_guide": safe_get(row, "FixGuide"),
            "ai_readiness_impact": safe_get(row, "AIReadinessImpact"),
        },
        "keywords": split_keywords(safe_get(row, "Keywords")),
    }


def build_poc2_document(row: dict[str, str]) -> dict[str, Any]:
    """
    Convert one PoC 2 CSV row into a RAG-style document.
    """
    knowledge_id = safe_get(row, "KnowledgeId")

    return {
        "document_id": knowledge_id,
        "source_poc": safe_get(row, "SourcePoC"),
        "source_type": safe_get(row, "SourceType"),
        "title": safe_get(row, "Title"),
        "content": build_poc2_content(row),
        "metadata": {
            **build_common_metadata(row),
            "business_area": safe_get(row, "BusinessArea"),
            "rag_suitable": to_bool(safe_get(row, "RAGSuitable")),
            "bi_suitable": to_bool(safe_get(row, "BISuitable")),
            "automation_suitable": to_bool(safe_get(row, "AutomationSuitable")),
            "rule_based_check_suitable": to_bool(
                safe_get(row, "RuleBasedCheckSuitable")
            ),
            "use_case_description": safe_get(row, "UseCaseDescription"),
            "input_data": safe_get(row, "InputData"),
            "process": safe_get(row, "Process"),
            "output": safe_get(row, "Output"),
            "discussion_point": safe_get(row, "DiscussionPoint"),
        },
        "keywords": split_keywords(safe_get(row, "Keywords")),
    }


def validate_document(document: dict[str, Any]) -> None:
    """
    Validate minimum required fields for a RAG-style document.

    This validation is intentionally simple for the MVP.
    Detailed checks will be added later in pytest.
    """
    required_top_level_fields = [
        "document_id",
        "source_poc",
        "source_type",
        "title",
        "content",
        "metadata",
        "keywords",
    ]

    for field in required_top_level_fields:
        if field not in document:
            raise ValueError(f"Missing required field '{field}' in document: {document}")

    if not document["document_id"]:
        raise ValueError(f"document_id is empty: {document}")

    if not document["source_poc"]:
        raise ValueError(f"source_poc is empty: {document['document_id']}")

    if not document["source_type"]:
        raise ValueError(f"source_type is empty: {document['document_id']}")

    if not document["title"]:
        raise ValueError(f"title is empty: {document['document_id']}")

    if not document["content"]:
        raise ValueError(f"content is empty: {document['document_id']}")

    if not isinstance(document["metadata"], dict):
        raise ValueError(f"metadata must be a dict: {document['document_id']}")

    if not isinstance(document["keywords"], list):
        raise ValueError(f"keywords must be a list: {document['document_id']}")


def validate_unique_document_ids(documents: list[dict[str, Any]]) -> None:
    """
    Ensure document_id values are unique.
    """
    seen: set[str] = set()

    for document in documents:
        document_id = document["document_id"]

        if document_id in seen:
            raise ValueError(f"Duplicate document_id found: {document_id}")

        seen.add(document_id)


def write_jsonl(documents: list[dict[str, Any]], output_path: Path) -> None:
    """
    Write documents to JSONL.

    Each line is one JSON document.
    ensure_ascii=False keeps Japanese text readable.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        for document in documents:
            f.write(json.dumps(document, ensure_ascii=False) + "\n")


def build_rag_documents() -> list[dict[str, Any]]:
    """
    Build all RAG-style documents from PoC 1 and PoC 2 CSV inputs.
    """
    documents: list[dict[str, Any]] = []

    poc1_rows = read_csv_rows(POC1_INPUT)
    poc2_rows = read_csv_rows(POC2_INPUT)

    for row in poc1_rows:
        document = build_poc1_document(row)
        validate_document(document)
        documents.append(document)

    for row in poc2_rows:
        document = build_poc2_document(row)
        validate_document(document)
        documents.append(document)

    validate_unique_document_ids(documents)

    return documents


def main() -> None:
    """
    Entry point.
    """
    documents = build_rag_documents()
    write_jsonl(documents, OUTPUT_JSONL)

    poc1_count = sum(1 for doc in documents if doc["source_poc"] == "PoC1")
    poc2_count = sum(1 for doc in documents if doc["source_poc"] == "PoC2")

    print("RAG-style documents generated successfully.")
    print(f"Output: {OUTPUT_JSONL}")
    print(f"Total documents: {len(documents)}")
    print(f"PoC1 documents: {poc1_count}")
    print(f"PoC2 documents: {poc2_count}")


if __name__ == "__main__":
    main()