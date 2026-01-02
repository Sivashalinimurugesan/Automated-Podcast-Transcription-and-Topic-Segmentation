import os
import tempfile
from src.keyword_cloud import generate_keyword_cloud

def test_keyword_cloud_creates_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        output_path = tmp.name

    result_path = generate_keyword_cloud(
        "diabetes diabetes blood pressure",
        output_path
    )

    #  Validate correct behavior
    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 0

    # Cleanup
    os.remove(result_path)
