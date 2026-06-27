from __future__ import annotations

import csv
from pathlib import Path


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 9: pytest for retrieval results
#
# Target:
#   output/retrieval_results_v001.csv
#
# Purpose:
#   Validate retrieval results generated from sample questions.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"
RETRIEVAL_RESULTS_CSV = OUTPUT_DIR / "retrieval_results_v001.csv"


REQUIRED_FIELDS = {
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
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """
    Read CSV rows as dictionaries.
    """
    assert path.exists(), f"File does not exist: {path}"

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = [dict(row) for row in reader]

    return rows


def get_rows_by_question_id(rows: list[dict[str, str]], question_id: str) -> list[dict[str, str]]:
    """
    Get retrieval rows by QuestionId.
    """
    return [
        row for row in rows
        if row.get("QuestionId") == question_id
    ]


def get_valid_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """
    Return rows that have a retrieved DocumentId.
    """
    return [
        row for row in rows
        if row.get("DocumentId")
    ]


def test_retrieval_results_file_exists() -> None:
    """
    retrieval_results_v001.csv should exist.
    """
    assert RETRIEVAL_RESULTS_CSV.exists()


def test_retrieval_results_are_not_empty() -> None:
    """
    retrieval_results_v001.csv should contain one or more rows.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

    assert len(rows) > 0


def test_retrieval_results_have_required_fields() -> None:
    """
    retrieval result rows should have required fields.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

    for row in rows:
        missing_fields = REQUIRED_FIELDS - set(row.keys())

        assert not missing_fields, (
            f"Retrieval result row is missing fields: {missing_fields}"
        )


def test_all_questions_have_at_least_one_result() -> None:
    """
    All sample questions should have at least one retrieved document.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

    question_ids = {
        row["QuestionId"]
        for row in rows
    }

    for question_id in question_ids:
        question_rows = get_rows_by_question_id(rows, question_id)
        valid_rows = get_valid_rows(question_rows)

        assert len(valid_rows) > 0, (
            f"No retrieval result found for question: {question_id}"
        )


def test_no_result_rows_are_zero() -> None:
    """
    There should be no no-result rows after Q035 keyword adjustment.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

    no_result_rows = [
        row for row in rows
        if not row["DocumentId"]
    ]

    assert len(no_result_rows) == 0


def test_expected_question_count_is_35() -> None:
    """
    Current sample question set should contain 35 questions.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

    question_ids = {
        row["QuestionId"]
        for row in rows
    }

    assert len(question_ids) == 35


def test_rank_values_are_present_for_valid_rows() -> None:
    """
    Valid retrieval rows should have Rank values.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        assert row["Rank"], (
            f"Rank is empty for QuestionId={row['QuestionId']} "
            f"DocumentId={row['DocumentId']}"
        )


def test_rank_values_are_positive_integers() -> None:
    """
    Rank values should be positive integers.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        rank = int(row["Rank"])

        assert rank >= 1


def test_score_values_are_present_for_valid_rows() -> None:
    """
    Valid retrieval rows should have Score values.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        assert row["Score"] != "", (
            f"Score is empty for QuestionId={row['QuestionId']} "
            f"DocumentId={row['DocumentId']}"
        )


def test_score_values_are_positive_for_valid_rows() -> None:
    """
    Valid retrieval rows should have positive scores.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        score = int(row["Score"])

        assert score > 0, (
            f"Score should be positive for QuestionId={row['QuestionId']} "
            f"DocumentId={row['DocumentId']}"
        )


def test_required_document_fields_are_present_for_valid_rows() -> None:
    """
    Valid retrieval rows should have document-related fields.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        assert row["DocumentId"], f"DocumentId is empty: {row['QuestionId']}"
        assert row["SourcePoC"], f"SourcePoC is empty: {row['QuestionId']}"
        assert row["SourceType"], f"SourceType is empty: {row['QuestionId']}"
        assert row["Title"], f"Title is empty: {row['QuestionId']}"
        assert row["SourceFile"], f"SourceFile is empty: {row['QuestionId']}"


def test_human_review_and_deep_dive_fields_are_present() -> None:
    """
    HumanReviewRequired and DeepDiveRequired should be present for valid rows.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        assert row["HumanReviewRequired"] in {"True", "False"}, (
            f"Invalid HumanReviewRequired value: {row['HumanReviewRequired']}"
        )

        assert row["DeepDiveRequired"] in {"True", "False"}, (
            f"Invalid DeepDiveRequired value: {row['DeepDiveRequired']}"
        )


def test_matched_keywords_are_present_for_valid_rows() -> None:
    """
    Valid retrieval rows should include matched keywords.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    for row in valid_rows:
        assert row["MatchedKeywords"], (
            f"MatchedKeywords is empty for QuestionId={row['QuestionId']} "
            f"DocumentId={row['DocumentId']}"
        )


def test_each_question_has_at_most_top_3_results() -> None:
    """
    Each question should have at most Top K = 3 valid results.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

    question_ids = {
        row["QuestionId"]
        for row in rows
    }

    for question_id in question_ids:
        question_rows = get_rows_by_question_id(rows, question_id)
        valid_rows = get_valid_rows(question_rows)

        assert len(valid_rows) <= 3, (
            f"Question {question_id} has more than 3 retrieval results."
        )


def test_q001_retrieves_door_name_missing_rule() -> None:
    """
    Q001 should retrieve a document related to RuleId D-001.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    q001_rows = get_rows_by_question_id(rows, "Q001")

    rule_ids = {
        row["RuleId"]
        for row in q001_rows
        if row["RuleId"]
    }

    assert "D-001" in rule_ids


def test_q004_retrieves_room_name_missing_rule() -> None:
    """
    Q004 should retrieve a document related to RuleId R-101.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    q004_rows = get_rows_by_question_id(rows, "Q004")

    rule_ids = {
        row["RuleId"]
        for row in q004_rows
        if row["RuleId"]
    }

    assert "R-101" in rule_ids


def test_q013_retrieves_uc001() -> None:
    """
    Q013 should retrieve a document related to UseCaseId UC-001.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    q013_rows = get_rows_by_question_id(rows, "Q013")

    use_case_ids = {
        row["UseCaseId"]
        for row in q013_rows
        if row["UseCaseId"]
    }

    assert "UC-001" in use_case_ids


def test_q017_has_deep_dive_related_result() -> None:
    """
    Q017 should retrieve at least one DeepDiveRequired=True result.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    q017_rows = get_rows_by_question_id(rows, "Q017")

    deep_dive_values = {
        row["DeepDiveRequired"]
        for row in q017_rows
    }

    assert "True" in deep_dive_values


def test_q022_has_human_review_required_result() -> None:
    """
    Q022 should retrieve at least one HumanReviewRequired=True result.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    q022_rows = get_rows_by_question_id(rows, "Q022")

    human_review_values = {
        row["HumanReviewRequired"]
        for row in q022_rows
    }

    assert "True" in human_review_values


def test_retrieval_results_contain_poc1_and_poc2_sources() -> None:
    """
    Retrieval results should include both PoC1 and PoC2 sources.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    source_pocs = {
        row["SourcePoC"]
        for row in valid_rows
    }

    assert "PoC1" in source_pocs
    assert "PoC2" in source_pocs


def test_retrieval_results_contain_rule_and_use_case_sources() -> None:
    """
    Retrieval results should include RuleMaster and UseCaseMapping source types.
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)
    valid_rows = get_valid_rows(rows)

    source_types = {
        row["SourceType"]
        for row in valid_rows
    }

    assert "RuleMaster" in source_types
    assert "UseCaseMapping" in source_types


def test_no_prohibited_final_decision_phrases_in_retrieval_results() -> None:
    """
    Retrieval result metadata should not include prohibited final-decision expressions.

    Note:
        The original Question text is excluded from this check because
        a question may intentionally ask about a prohibited phrase, such as
        "人間確認は不要ですか".
    """
    rows = read_csv_rows(RETRIEVAL_RESULTS_CSV)

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

    fields_to_check = [
        "DocumentId",
        "SourcePoC",
        "SourceType",
        "Title",
        "MatchedKeywords",
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

    csv_text = "\n".join(
        ",".join(row.get(field, "") for field in fields_to_check)
        for row in rows
    )

    for phrase in prohibited_phrases:
        assert phrase not in csv_text, (
            f"Prohibited phrase found in retrieval result metadata: {phrase}"
        )