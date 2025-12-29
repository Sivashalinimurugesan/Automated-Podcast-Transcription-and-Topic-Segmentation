from src.logger import get_logger
from user_state_manager import (
    get_user_last_step,
    update_user_step
)

pipeline_logger = get_logger("PIPELINE", "pipeline.log")

PIPELINE_STEPS = [
    "preprocessing",
    "transcription",
    "segmentation",
    "sentiment",
    "keywords",
    "evaluation"
]

# ---------------------------------------------------------
# CORE PIPELINE LOGIC (USER-AWARE, RESUMABLE)
# ---------------------------------------------------------
def run_pipeline(user_id):
    start_step = get_user_last_step(user_id)

    pipeline_logger.info(
        f"User {user_id} resuming pipeline from step: {start_step}"
    )

    for step in PIPELINE_STEPS:
        if PIPELINE_STEPS.index(step) < PIPELINE_STEPS.index(start_step):
            continue

        try:
            pipeline_logger.info(f"Starting step: {step}")
            execute_step(step)
            update_user_step(user_id, step)
            pipeline_logger.info(f"Completed step: {step}")

        except Exception as e:
            pipeline_logger.error(
                f"Pipeline FAILED for user {user_id} at step {step}: {str(e)}"
            )
            break

    pipeline_logger.info(f"Pipeline finished for user {user_id}")

# ---------------------------------------------------------
# STEP EXECUTION (UNCHANGED LOGIC)
# ---------------------------------------------------------
def execute_step(step):

    if step == "preprocessing":
        import preprocessing
        preprocessing.main()

    elif step == "transcription":
        import transcription
        transcription.main()

    elif step == "segmentation":
        import segmentation
        segmentation.main()

    elif step == "sentiment":
        import sentiment
        sentiment.run()

    elif step == "keywords":
        import keywords
        keywords.run()

    elif step == "evaluation":
        import evaluation
        evaluation.evaluate_transcripts()

# ---------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------
def main():
    """
    Entry point for CLI / testing.
    In real app, user_id comes from login / UI.
    """
    user_id = "demo_user"
    run_pipeline(user_id)

# ---------------------------------------------------------
# RUN
# ---------------------------------------------------------
if __name__ == "__main__":
    main()
