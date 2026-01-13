import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# Import Flask app module
import ui_app


# ------------------------
# HOME PAGE TEST
# ------------------------
def test_home_page():
    client = ui_app.app.test_client()
    response = client.get("/")
    assert response.status_code == 200


# ------------------------
# UPLOAD PAGE TEST
# ------------------------
def test_upload_page():
    client = ui_app.app.test_client()
    response = client.get("/upload")
    assert response.status_code == 200


# ------------------------
# ANALYTICS PAGE TEST
# ------------------------
def test_analytics_page():
    client = ui_app.app.test_client()
    response = client.get("/analytics")
    assert response.status_code == 200


# ------------------------
# PLAYER PAGE TEST
# ------------------------
def test_player_page():
    files = ui_app.list_existing_audio()

    if not files:
        return  # safely skip

    audio = files[0]
    client = ui_app.app.test_client()
    response = client.get(f"/player/{audio}")
    assert response.status_code == 200
