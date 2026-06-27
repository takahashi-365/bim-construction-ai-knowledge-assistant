from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 6: Retrieve documents
#
# Input:
#   input/sample_questions_v001.csv
#   output/rag_index_v001.json
#
# Output:
#   output/retrieval_results_v001.csv
#
# Purpose:
#   Retrieve relevant RAG-style documents for each sample question
#   using a simple local keyword-based scoring method.
#
# Note:
#   This is not vector search.
#   This is a lightweight MVP retrieval implementation.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

QUESTIONS_CSV = INPUT_DIR / "sample_questions_v001.csv"
RAG_INDEX_JSON = OUTPUT_DIR / "rag_index_v001.json"

RETRIEVAL_RESULTS_CSV = OUTPUT_DIR / "retrieval_results_v001.csv"

TOP_K = 3


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """
    Read CSV rows as dictionaries.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def load_json(json_path: Path) -> dict[str, Any]:
    """
    Load JSON file.
    """
    if not json_path.exists():
        raise FileNotFoundError(f"Input file not found: {json_path}")

    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def safe_get(row: dict[str, Any], key: str, default: str = "") -> str:
    """
    Safely get a value as stripped text.
    """
    value = row.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def normalize_text(value: Any) -> str:
    """
    Normalize text for simple keyword matching.
    """
    if value is None:
        return ""

    text = str(value).lower()
    text = re.sub(r"\s+", " ", text).strip()

    return text


def tokenize_simple(text: str) -> list[str]:
    """
    Create simple tokens for MVP keyword search.

    This keeps Japanese text and lowercased English-like tokens.
    """
    normalized = normalize_text(text)
    raw_tokens = re.split(r"[^\w\u3040-\u30ff\u3400-\u9fff]+", normalized)

    tokens: list[str] = []
    for token in raw_tokens:
        token = token.strip()
        if not token:
            continue

        has_japanese = bool(re.search(r"[\u3040-\u30ff\u3400-\u9fff]", token))

        if has_japanese or len(token) >= 2:
            tokens.append(token)

    return tokens


def split_keywords(value: str | None) -> list[str]:
    """
    Convert pipe-separated keywords into a clean keyword list.
    """
    if not value:
        return []

    keywords: list[str] = []

    for item in value.split("|"):
        item = item.strip()
        if item:
            keywords.append(item)

    return keywords


def to_bool_text(value: Any) -> str:
    """
    Convert boolean-like values to CSV-friendly True / False text.
    """
    if isinstance(value, bool):
        return "True" if value else "False"

    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return "True"

    return "False"


def build_query_tokens(question_row: dict[str, str]) -> list[str]:
    """
    Build search tokens from Question and Keywords.

    ExpectedRuleId and ExpectedUseCaseId are intentionally not used here,
    because they are evaluation hints, not search input.
    """
    question = safe_get(question_row, "Question")
    keywords = split_keywords(safe_get(question_row, "Keywords"))

    query_text = " ".join([question, " ".join(keywords)])
    tokens = tokenize_simple(query_text)

    # Deduplicate while preserving order.
    return list(dict.fromkeys(tokens))


def calculate_score(
    query_tokens: list[str],
    document_entry: dict[str, Any],
) -> tuple[int, list[str]]:
    """
    Calculate a simple keyword-based retrieval score.

    Scoring policy:
      - Exact token match in index tokens: +3
      - Substring match in search_text: +1
      - Match against document keywords: +5

    This is intentionally simple for the MVP.
    """
    document_tokens = document_entry.get("tokens", [])
    search_text = normalize_text(document_entry.get("search_text", ""))
    document_keywords = document_entry.get("keywords", [])

    if not isinstance(document_tokens, list):
        document_tokens = []

    if not isinstance(document_keywords, list):
        document_keywords = []

    document_token_set = {normalize_text(token) for token in document_tokens}
    document_keyword_set = {normalize_text(keyword) for keyword in document_keywords}

    score = 0
    matched_keywords: list[str] = []

    for token in query_tokens:
        normalized_token = normalize_text(token)

        if not normalized_token:
            continue

        token_matched = False

        if normalized_token in document_token_set:
            score += 3
            token_matched = True

        if normalized_token in document_keyword_set:
            score += 5
            token_matched = True

        if normalized_token not in document_token_set and normalized_token in search_text:
            score += 1
            token_matched = True

        if token_matched:
            matched_keywords.append(token)

    # Deduplicate while preserving order.
    matched_keywords = list(dict.fromkeys(matched_keywords))

    return score, matched_keywords


def retrieve_top_documents(
    question_row: dict[str, str],
    index_documents: list[dict[str, Any]],
    top_k: int = TOP_K,
) -> list[dict[str, Any]]:
    """
    Retrieve top matching documents for one question.
    """
    query_tokens = build_query_tokens(question_row)

    scored_results: list[dict[str, Any]] = []

    for document_entry in index_documents:
        score, matched_keywords = calculate_score(query_tokens, document_entry)

        if score <= 0:
            continue

        result = {
            "score": score,
            "matched_keywords": matched_keywords,
            "document": document_entry,
        }
        scored_results.append(result)

    scored_results.sort(
        key=lambda item: (
            item["score"],
            len(item["matched_keywords"]),
            item["document"].get("document_id", ""),
        ),
        reverse=True,
    )

    return scored_results[:top_k]


def build_result_row(
    question_row: dict[str, str],
    retrieval_result: dict[str, Any],
    rank: int,
) -> dict[str, Any]:
    """
    Build one CSV row for retrieval_results_v001.csv.
    """
    document = retrieval_result["document"]

    return {
        "QuestionId": safe_get(question_row, "QuestionId"),
        "Question": safe_get(question_row, "Question"),
        "QuestionType": safe_get(question_row, "QuestionType"),
        "Rank": rank,
        "DocumentId": document.get("document_id", ""),
        "SourcePoC": document.get("source_poc", ""),
        "SourceType": document.get("source_type", ""),
        "Title": document.get("title", ""),
        "MatchedKeywords": "|".join(retrieval_result["matched_keywords"]),
        "Score": retrieval_result["score"],
        "RuleId": document.get("rule_id", ""),
        "UseCaseId": document.get("use_case_id", ""),
        "RecommendedApproach": document.get("recommended_approach", ""),
        "HumanReviewRequired": to_bool_text(document.get("human_review_required", False)),
        "DeepDiveRequired": to_bool_text(document.get("deep_dive_required", False)),
        "SourceFile": document.get("source_file", ""),
        "ExpectedSourcePoC": safe_get(question_row, "ExpectedSourcePoC"),
        "ExpectedSourceType": safe_get(question_row, "ExpectedSourceType"),
        "ExpectedRuleId": safe_get(question_row, "ExpectedRuleId"),
        "ExpectedUseCaseId": safe_get(question_row, "ExpectedUseCaseId"),
        "ExpectedFocus": safe_get(question_row, "ExpectedFocus"),
    }


def build_no_result_row(question_row: dict[str, str]) -> dict[str, Any]:
    """
    Build a fallback CSV row when no document is retrieved.
    """
    return {
        "QuestionId": safe_get(question_row, "QuestionId"),
        "Question": safe_get(question_row, "Question"),
        "QuestionType": safe_get(question_row, "QuestionType"),
        "Rank": "",
        "DocumentId": "",
        "SourcePoC": "",
        "SourceType": "",
        "Title": "",
        "MatchedKeywords": "",
        "Score": 0,
        "RuleId": "",
        "UseCaseId": "",
        "RecommendedApproach": "",
        "HumanReviewRequired": "",
        "DeepDiveRequired": "",
        "SourceFile": "",
        "ExpectedSourcePoC": safe_get(question_row, "ExpectedSourcePoC"),
        "ExpectedSourceType": safe_get(question_row, "ExpectedSourceType"),
        "ExpectedRuleId": safe_get(question_row, "ExpectedRuleId"),
        "ExpectedUseCaseId": safe_get(question_row, "ExpectedUseCaseId"),
        "ExpectedFocus": safe_get(question_row, "ExpectedFocus"),
    }


def write_csv(rows: list[dict[str, Any]], output_path: Path) -> None:
    """
    Write retrieval results to CSV.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "QuestionId",
        "Question",
        "QuestionType",
        "Rank",
        "DocumentId",
        "SourcePoC",
        "SourceType",
        "Title",
        "MatchedKeywords",
        "Score",
        "RuleId",
        "UseCaseId",
        "RecommendedApproach",
        "HumanReviewRequired",
        "DeepDiveRequired",
        "SourceFile",
        "ExpectedSourcePoC",
        "ExpectedSourceType",
        "ExpectedRuleId",
        "ExpectedUseCaseId",
        "ExpectedFocus",
    ]

    with output_path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def retrieve_documents() -> list[dict[str, Any]]:
    """
    Retrieve documents for all sample questions.
    """
    question_rows = read_csv_rows(QUESTIONS_CSV)
    rag_index = load_json(RAG_INDEX_JSON)

    index_documents = rag_index.get("documents", [])

    if not isinstance(index_documents, list):
        raise ValueError("Invalid rag_index_v001.json: 'documents' must be a list.")

    output_rows: list[dict[str, Any]] = []

    for question_row in question_rows:
        top_results = retrieve_top_documents(question_row, index_documents, TOP_K)

        if not top_results:
            output_rows.append(build_no_result_row(question_row))
            continue

        for rank, retrieval_result in enumerate(top_results, start=1):
            output_rows.append(build_result_row(question_row, retrieval_result, rank))

    return output_rows


def main() -> None:
    """
    Entry point.
    """
    result_rows = retrieve_documents()
    write_csv(result_rows, RETRIEVAL_RESULTS_CSV)

    question_count = len(read_csv_rows(QUESTIONS_CSV))
    retrieved_row_count = len(result_rows)
    no_result_count = sum(1 for row in result_rows if not row["DocumentId"])

    print("Document retrieval completed successfully.")
    print(f"Questions: {question_count}")
    print(f"Output: {RETRIEVAL_RESULTS_CSV}")
    print(f"Retrieval result rows: {retrieved_row_count}")
    print(f"No-result rows: {no_result_count}")
    print(f"Top K: {TOP_K}")


if __name__ == "__main__":
    main()