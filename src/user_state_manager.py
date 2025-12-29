import json
import os

# Always keep session state inside sessions/
STATE_DIR = "sessions"
STATE_FILE = os.path.join(STATE_DIR, "session_state.json")

os.makedirs(STATE_DIR, exist_ok=True)

def _load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4)

def get_user_last_step(user_id):
    state = _load_state()
    return state.get(user_id, "preprocessing")

def update_user_step(user_id, step):
    state = _load_state()
    state[user_id] = step
    _save_state(state)

# ---------------------------------------------------------
# OPTIONAL TEST
# ---------------------------------------------------------
def main():
    test_user = "demo_user"

    print("Initial step:", get_user_last_step(test_user))
    update_user_step(test_user, "transcription")
    print("Updated step:", get_user_last_step(test_user))

if __name__ == "__main__":
    main()
