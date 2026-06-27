from __future__ import annotations

from pathlib import Path


# ============================================================
# PoC 3: BIM / Construction AI Knowledge Assistant
# Step 9: pytest for sample grounded answers
#
# Target:
#   output/sample_answers_v001.md
#
# Purpose:
#   Validate generated grounded answer markdown.
# ============================================================


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUT_DIR = PROJECT_ROOT / "output"
SAMPLE_ANSWERS_MD = OUTPUT_DIR / "sample_answers_v001.md"


def read_text(path: Path) -> str:
    """
    Read text file.
    """
    assert path.exists(), f"File does not exist: {path}"

    return path.read_text(encoding="utf-8")


def test_sample_answers_file_exists() -> None:
    """
    sample_answers_v001.md should exist.
    """
    assert SAMPLE_ANSWERS_MD.exists()


def test_sample_answers_are_not_empty() -> None:
    """
    sample_answers_v001.md should not be empty.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert text.strip()


def test_sample_answers_has_title() -> None:
    """
    sample_answers_v001.md should have the expected title.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "# Sample Grounded Answers v001" in text


def test_sample_answers_has_overview() -> None:
    """
    sample_answers_v001.md should have an Overview section.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "## Overview" in text


def test_sample_answers_has_important_notes() -> None:
    """
    sample_answers_v001.md should have Important Notes section.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "## Important Notes" in text


def test_sample_answers_contains_35_question_sections() -> None:
    """
    Current sample answer set should contain 35 question sections.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    question_section_count = sum(
        1 for line in text.splitlines()
        if line.startswith("## Q")
    )

    assert question_section_count == 35


def test_sample_answers_contains_q001_and_q035() -> None:
    """
    sample_answers_v001.md should include first and last sample questions.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "## Q001:" in text
    assert "## Q035:" in text


def test_each_question_has_answer_section() -> None:
    """
    Each question section should include an Answer section.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### Answer" in question_text, (
            f"Answer section not found: {question_id}"
        )


def test_each_question_has_reasoning_summary_section() -> None:
    """
    Each question section should include a Reasoning Summary section.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### Reasoning Summary" in question_text, (
            f"Reasoning Summary section not found: {question_id}"
        )


def test_each_question_has_referenced_sources_section() -> None:
    """
    Each question section should include Referenced Sources.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### Referenced Sources" in question_text, (
            f"Referenced Sources section not found: {question_id}"
        )


def test_each_question_has_metadata_summary_section() -> None:
    """
    Each question section should include Metadata Summary.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### Metadata Summary" in question_text, (
            f"Metadata Summary section not found: {question_id}"
        )


def test_each_question_has_human_review_required_section() -> None:
    """
    Each question section should include HumanReviewRequired.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### HumanReviewRequired" in question_text, (
            f"HumanReviewRequired section not found: {question_id}"
        )


def test_each_question_has_deep_dive_required_section() -> None:
    """
    Each question section should include DeepDiveRequired.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### DeepDiveRequired" in question_text, (
            f"DeepDiveRequired section not found: {question_id}"
        )


def test_each_question_has_caution_section() -> None:
    """
    Each question section should include Caution.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    for question_number in range(1, 36):
        question_id = f"Q{question_number:03d}"

        question_start = text.find(f"## {question_id}:")
        assert question_start >= 0, f"Question section not found: {question_id}"

        next_question_start = text.find(f"## Q{question_number + 1:03d}:", question_start)

        if next_question_start >= 0:
            question_text = text[question_start:next_question_start]
        else:
            question_text = text[question_start:]

        assert "### Caution" in question_text, (
            f"Caution section not found: {question_id}"
        )


def test_sample_answers_have_referenced_sources() -> None:
    """
    sample_answers_v001.md should include referenced source entries.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "Rank 1:" in text
    assert "SourceFile:" in text


def test_sample_answers_have_no_missing_referenced_sources() -> None:
    """
    No question should have missing referenced sources after retrieval adjustment.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "No referenced source found." not in text


def test_sample_answers_include_poc1_and_poc2_sources() -> None:
    """
    sample_answers_v001.md should include both PoC1 and PoC2 references.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "PoC1" in text
    assert "PoC2" in text


def test_sample_answers_include_rule_and_use_case_metadata() -> None:
    """
    sample_answers_v001.md should include RuleId and UseCaseId metadata.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "RuleId:" in text
    assert "UseCaseId:" in text


def test_sample_answers_include_human_review_caution() -> None:
    """
    sample_answers_v001.md should include human review caution.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "設計判断、施工判断、法規判断、安全判断、契約判断は人間レビューが必要です" in text
    assert "AIは最終判断を行いません" in text


def test_sample_answers_include_revit_auto_modify_limitation() -> None:
    """
    sample_answers_v001.md should include a note that Revit models are not automatically modified.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "Revit models are not automatically modified." in text


def test_sample_answers_include_template_based_mvp_note() -> None:
    """
    sample_answers_v001.md should say this is not LLM-based free generation.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "This is not LLM-based free generation." in text
    assert "local MVP answer generation step" in text


def test_sample_answers_include_door_and_room_rules() -> None:
    """
    sample_answers_v001.md should include representative Door and Room RuleIds.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "D-001" in text
    assert "R-101" in text


def test_sample_answers_include_use_case_id() -> None:
    """
    sample_answers_v001.md should include representative UseCaseId.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "UC-001" in text


def test_sample_answers_do_not_include_no_result_message() -> None:
    """
    Since No-result questions are zero, no no-result answer text should remain.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

    assert "関連documentを取得できませんでした" not in text
    assert "検索結果だけでは十分な根拠が不足しています" not in text


def test_no_prohibited_final_decision_phrases_in_sample_answers() -> None:
    """
    sample_answers_v001.md should not include prohibited final-decision expressions.

    Note:
        The question heading may intentionally contain a risky phrase.
        Therefore, question headings are excluded before checking.
    """
    text = read_text(SAMPLE_ANSWERS_MD)

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

    checked_lines: list[str] = []

    for line in text.splitlines():
        if line.startswith("## Q"):
            continue

        checked_lines.append(line)

    checked_text = "\n".join(checked_lines)

    for phrase in prohibited_phrases:
        assert phrase not in checked_text, (
            f"Prohibited phrase found in sample_answers_v001.md: {phrase}"
        )