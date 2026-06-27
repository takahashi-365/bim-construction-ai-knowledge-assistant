from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 7: Generate sample grounded answers
#
# Input:
#   output/retrieval_results_v001.csv
#   output/rag_documents_v001.jsonl
#
# Output:
#   output/sample_answers_v001.md
#
# Purpose:
#   Generate grounded sample answers from retrieval results.
#   Each answer includes referenced sources, metadata, Human Review,
#   Deep Dive, and caution text.
#
# Note:
#   This is not LLM-based free generation.
#   This is a template-based MVP answer generator.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"

RETRIEVAL_RESULTS_CSV = OUTPUT_DIR / "retrieval_results_v001.csv"
RAG_DOCUMENTS_JSONL = OUTPUT_DIR / "rag_documents_v001.jsonl"

SAMPLE_ANSWERS_MD = OUTPUT_DIR / "sample_answers_v001.md"


HUMAN_REVIEW_CAUTION = (
    "この回答は協議用の参考情報です。"
    "設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です。"
    "AIは最終判断を行いません。"
)

DEEP_DIVE_CAUTION = (
    "この内容は追加確認が必要です。"
    "入力情報、判断条件、関係者確認、業務範囲などを確認したうえで、"
    "AI/DX活用方針を協議する必要があります。"
)

NO_RESULT_CAUTION = (
    "検索結果だけでは十分な根拠が不足しています。"
    "追加の資料確認、キーワード調整、または人間レビューが必要です。"
)


def read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """
    Read CSV rows as dictionaries.
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Input file not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def load_jsonl(jsonl_path: Path) -> list[dict[str, Any]]:
    """
    Load JSONL documents.
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
                documents.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"Invalid JSON at line {line_number} in {jsonl_path}: {e}"
                ) from e

    return documents


def safe_get(row: dict[str, Any], key: str, default: str = "") -> str:
    """
    Safely get a value as stripped text.
    """
    value = row.get(key, default)
    if value is None:
        return default
    return str(value).strip()


def to_bool(value: Any) -> bool:
    """
    Convert common boolean text to bool.
    """
    if isinstance(value, bool):
        return value

    text = str(value).strip().lower()
    return text in {"true", "1", "yes"}


def group_retrieval_results(
    retrieval_rows: list[dict[str, str]],
) -> dict[str, list[dict[str, str]]]:
    """
    Group retrieval results by QuestionId.
    """
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)

    for row in retrieval_rows:
        question_id = safe_get(row, "QuestionId")
        grouped[question_id].append(row)

    return dict(grouped)


def build_document_lookup(
    documents: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """
    Build document lookup by document_id.
    """
    lookup: dict[str, dict[str, Any]] = {}

    for document in documents:
        document_id = safe_get(document, "document_id")
        if document_id:
            lookup[document_id] = document

    return lookup


def get_question_header(question_rows: list[dict[str, str]]) -> dict[str, str]:
    """
    Get a representative question row from grouped retrieval rows.
    """
    if not question_rows:
        return {}

    return question_rows[0]


def filter_valid_results(question_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Remove no-result rows and sort by rank.
    """
    valid_rows = [
        row for row in question_rows
        if safe_get(row, "DocumentId")
    ]

    def rank_key(row: dict[str, str]) -> int:
        rank_text = safe_get(row, "Rank")
        try:
            return int(rank_text)
        except ValueError:
            return 9999

    return sorted(valid_rows, key=rank_key)


def collect_flags(result_rows: list[dict[str, str]]) -> tuple[bool, bool]:
    """
    Collect HumanReviewRequired and DeepDiveRequired from retrieved rows.
    """
    human_review_required = any(
        to_bool(safe_get(row, "HumanReviewRequired"))
        for row in result_rows
    )
    deep_dive_required = any(
        to_bool(safe_get(row, "DeepDiveRequired"))
        for row in result_rows
    )

    return human_review_required, deep_dive_required


def summarize_primary_document(
    primary_row: dict[str, str],
    document_lookup: dict[str, dict[str, Any]],
) -> str:
    """
    Build a short answer summary from the top-ranked retrieved document.
    """
    document_id = safe_get(primary_row, "DocumentId")
    document = document_lookup.get(document_id, {})

    title = safe_get(primary_row, "Title")
    source_poc = safe_get(primary_row, "SourcePoC")
    source_type = safe_get(primary_row, "SourceType")
    rule_id = safe_get(primary_row, "RuleId")
    use_case_id = safe_get(primary_row, "UseCaseId")
    recommended_approach = safe_get(primary_row, "RecommendedApproach")

    content = safe_get(document, "content")

    lines: list[str] = []

    lines.append(
        f"検索結果では、主に `{source_poc}` の `{source_type}` である "
        f"`{title}` が関連情報として取得されました。"
    )

    if rule_id:
        lines.append(f"関連するRuleIdは `{rule_id}` です。")

    if use_case_id:
        lines.append(f"関連するUseCaseIdは `{use_case_id}` です。")

    if recommended_approach:
        lines.append(f"RecommendedApproachは `{recommended_approach}` です。")

    if content:
        lines.append("")
        lines.append("取得された主な内容は以下です。")
        lines.append("")
        lines.append("> " + content.replace("\n", "\n> "))

    return "\n".join(lines)


def build_reasoning_summary(
    result_rows: list[dict[str, str]],
) -> str:
    """
    Build reasoning summary from retrieved documents.
    """
    if not result_rows:
        return NO_RESULT_CAUTION

    lines: list[str] = []

    lines.append(
        "この回答は、質問文およびKeywordsと、RAG-style documentの"
        "title、content、metadata、keywordsの一致に基づいて生成しています。"
    )

    top_titles = [
        safe_get(row, "Title")
        for row in result_rows
        if safe_get(row, "Title")
    ]

    if top_titles:
        lines.append("上位検索結果として以下のdocumentが参照されました。")
        for title in top_titles:
            lines.append(f"- {title}")

    return "\n".join(lines)


def build_referenced_sources(result_rows: list[dict[str, str]]) -> str:
    """
    Build referenced sources list.
    """
    if not result_rows:
        return "- No referenced source found."

    lines: list[str] = []

    for row in result_rows:
        lines.append(
            "- "
            f"Rank {safe_get(row, 'Rank')}: "
            f"`{safe_get(row, 'DocumentId')}` / "
            f"{safe_get(row, 'SourcePoC')} / "
            f"{safe_get(row, 'SourceType')} / "
            f"{safe_get(row, 'Title')} / "
            f"Score: {safe_get(row, 'Score')} / "
            f"SourceFile: `{safe_get(row, 'SourceFile')}`"
        )

    return "\n".join(lines)


def collect_metadata_values(
    result_rows: list[dict[str, str]],
    key: str,
) -> list[str]:
    """
    Collect unique metadata values from retrieval rows.
    """
    values: list[str] = []

    for row in result_rows:
        value = safe_get(row, key)
        if value and value not in values:
            values.append(value)

    return values


def build_metadata_section(result_rows: list[dict[str, str]]) -> str:
    """
    Build RuleId / UseCaseId / RecommendedApproach summary.
    """
    rule_ids = collect_metadata_values(result_rows, "RuleId")
    use_case_ids = collect_metadata_values(result_rows, "UseCaseId")
    recommended_approaches = collect_metadata_values(result_rows, "RecommendedApproach")

    lines: list[str] = []

    lines.append(f"- RuleId: {', '.join(rule_ids) if rule_ids else '-'}")
    lines.append(f"- UseCaseId: {', '.join(use_case_ids) if use_case_ids else '-'}")
    lines.append(
        "- RecommendedApproach: "
        f"{', '.join(recommended_approaches) if recommended_approaches else '-'}"
    )

    return "\n".join(lines)


def build_caution_section(
    result_rows: list[dict[str, str]],
    human_review_required: bool,
    deep_dive_required: bool,
) -> str:
    """
    Build caution text based on retrieval results.
    """
    if not result_rows:
        return NO_RESULT_CAUTION

    cautions: list[str] = []

    if human_review_required:
        cautions.append(HUMAN_REVIEW_CAUTION)

    if deep_dive_required:
        cautions.append(DEEP_DIVE_CAUTION)

    if not cautions:
        cautions.append(
            "この回答は検索結果に基づく参考情報です。"
            "実案件への適用や最終判断が必要な場合は、人間レビューを行ってください。"
        )

    return "\n\n".join(cautions)


def build_one_answer_markdown(
    question_id: str,
    question_rows: list[dict[str, str]],
    document_lookup: dict[str, dict[str, Any]],
) -> str:
    """
    Build markdown for one question answer.
    """
    question_header = get_question_header(question_rows)
    result_rows = filter_valid_results(question_rows)

    question = safe_get(question_header, "Question")
    question_type = safe_get(question_header, "QuestionType")
    expected_focus = safe_get(question_header, "ExpectedFocus")

    human_review_required, deep_dive_required = collect_flags(result_rows)

    lines: list[str] = []

    lines.append(f"## {question_id}: {question}")
    lines.append("")
    lines.append(f"- QuestionType: {question_type}")
    lines.append(f"- ExpectedFocus: {expected_focus}")
    lines.append("")

    lines.append("### Answer")
    lines.append("")

    if result_rows:
        lines.append(summarize_primary_document(result_rows[0], document_lookup))
    else:
        lines.append(
            "この質問に対して、現在の簡易キーワード検索では関連documentを取得できませんでした。"
            "質問キーワード、サンプルナレッジ、または検索ロジックの調整が必要です。"
        )

    lines.append("")
    lines.append("### Reasoning Summary")
    lines.append("")
    lines.append(build_reasoning_summary(result_rows))

    lines.append("")
    lines.append("### Referenced Sources")
    lines.append("")
    lines.append(build_referenced_sources(result_rows))

    lines.append("")
    lines.append("### Metadata Summary")
    lines.append("")
    lines.append(build_metadata_section(result_rows))

    lines.append("")
    lines.append("### HumanReviewRequired")
    lines.append("")
    lines.append("True" if human_review_required else "False")

    lines.append("")
    lines.append("### DeepDiveRequired")
    lines.append("")
    lines.append("True" if deep_dive_required else "False")

    lines.append("")
    lines.append("### Caution")
    lines.append("")
    lines.append(
        build_caution_section(
            result_rows=result_rows,
            human_review_required=human_review_required,
            deep_dive_required=deep_dive_required,
        )
    )

    lines.append("")
    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def build_markdown_document(
    grouped_results: dict[str, list[dict[str, str]]],
    document_lookup: dict[str, dict[str, Any]],
) -> str:
    """
    Build the full sample_answers_v001.md content.
    """
    lines: list[str] = []

    lines.append("# Sample Grounded Answers v001")
    lines.append("")
    lines.append("## Overview")
    lines.append("")
    lines.append(
        "This file contains template-based grounded answers generated from "
        "`output/retrieval_results_v001.csv` and `output/rag_documents_v001.jsonl`."
    )
    lines.append("")
    lines.append(
        "This is not LLM-based free generation. "
        "It is a local MVP answer generation step for PoC 3."
    )
    lines.append("")
    lines.append("## Important Notes")
    lines.append("")
    lines.append("- Answers are based on retrieved RAG-style documents.")
    lines.append("- Referenced Sources are shown for traceability.")
    lines.append("- HumanReviewRequired and DeepDiveRequired are reflected from retrieved documents.")
    lines.append("- AI does not make final design, construction, legal, safety, or contractual decisions.")
    lines.append("- Revit models are not automatically modified.")
    lines.append("")
    lines.append("---")
    lines.append("")

    sorted_question_ids = sorted(
        grouped_results.keys(),
        key=lambda qid: int(qid.replace("Q", "")) if qid.startswith("Q") and qid[1:].isdigit() else 9999,
    )

    for question_id in sorted_question_ids:
        lines.append(
            build_one_answer_markdown(
                question_id=question_id,
                question_rows=grouped_results[question_id],
                document_lookup=document_lookup,
            )
        )

    return "\n".join(lines)


def write_text(text: str, output_path: Path) -> None:
    """
    Write text file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def generate_sample_answers() -> str:
    """
    Generate sample grounded answers markdown.
    """
    retrieval_rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    rag_documents = load_jsonl(RAG_DOCUMENTS_JSONL)

    grouped_results = group_retrieval_results(retrieval_rows)
    document_lookup = build_document_lookup(rag_documents)

    markdown = build_markdown_document(grouped_results, document_lookup)

    return markdown


def main() -> None:
    """
    Entry point.
    """
    markdown = generate_sample_answers()
    write_text(markdown, SAMPLE_ANSWERS_MD)

    retrieval_rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    grouped_results = group_retrieval_results(retrieval_rows)

    question_count = len(grouped_results)
    no_result_question_count = 0

    for question_rows in grouped_results.values():
        valid_results = filter_valid_results(question_rows)
        if not valid_results:
            no_result_question_count += 1

    print("Sample grounded answers generated successfully.")
    print(f"Input retrieval results: {RETRIEVAL_RESULTS_CSV}")
    print(f"Input RAG documents: {RAG_DOCUMENTS_JSONL}")
    print(f"Output: {SAMPLE_ANSWERS_MD}")
    print(f"Questions: {question_count}")
    print(f"No-result questions: {no_result_question_count}")


if __name__ == "__main__":
    main()