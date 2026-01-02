from src.segmentation import generate_segmentation_for_ui

def test_segmentation_returns_dict():
    result = generate_segmentation_for_ui("The patient has fever and cough")

    assert isinstance(result, dict)
    assert "segments" in result
    assert isinstance(result["segments"], list)
