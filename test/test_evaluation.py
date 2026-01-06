from src.evaluation_summary import get_evaluation_summary_for_ui


def test_accuracy_range_with_clean_transcript():
    # Check accuracy when clean transcript exists
    result = get_evaluation_summary_for_ui(
        predicted_text="patient has head pain and mild fever",
        file_id="GEN0001"
    )

    # Accuracy should be valid
    assert 0 <= result["avg_quality_score"] <= 100
    assert result["avg_similarity"] > 0
    assert result["avg_wer"] >= 0
    assert result["avg_cer"] >= 0


def test_high_error_still_returns_valid_accuracy():
    # Check system behavior for unrelated text
    result = get_evaluation_summary_for_ui(
        predicted_text="completely unrelated random sentence",
        file_id="GEN0001"
    )

    # Accuracy should still be computed
    assert 0 <= result["avg_quality_score"] <= 100
    assert result["avg_wer"] >= 0
    assert result["avg_cer"] >= 0


def test_best_match_used_when_file_not_found():
    # Check best-match logic when file_id is missing
    result = get_evaluation_summary_for_ui(
        predicted_text="patient feels dizzy and nauseous",
        file_id="UNKNOWN_FILE"
    )

    # Metrics should still be available
    assert 0 <= result["avg_quality_score"] <= 100
    assert result["avg_similarity"] > 0
    assert result["avg_wer"] >= 0
    assert result["avg_cer"] >= 0


def test_empty_input_returns_default():
    # Check fail-safe behavior for empty input
    result = get_evaluation_summary_for_ui(
        predicted_text="",
        file_id="GEN0001"
    )

    # Default values should be returned
    assert result["avg_quality_score"] == 0.0
    assert result["avg_similarity"] == 0.0
    assert result["avg_wer"] == 100.0
    assert result["avg_cer"] == 100.0
