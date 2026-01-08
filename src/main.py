from src.preprocessing import preprocess_audio
from src.transcription import transcribe_audio
from src.segmentation import segment_transcripts
from src.summarization import summarize_segments
from src.keyword_extraction import run_keyword_extraction
from src.evaluate_asr import evaluate_asr


# -------------------------------
# Directory paths
# -------------------------------
AUDIO_RAW = "audio_raw"
AUDIO_PROCESSED = "audio_processed"

REFERENCE_TRANSCRIPTS = "transcripts/raw_reference"
ASR_TRANSCRIPTS = "transcripts/asr"

SEGMENTS_DIR = "segments"
FINAL_TRANSCRIPTS = "transcripts/final"

RESULTS_PATH = "results/asr_evaluation.csv"


def main():
    print("\n===== HR INTERVIEW PIPELINE STARTED =====\n")

    # 1. Preprocess audio
    print("Step 1: Preprocessing audio...")
    preprocess_audio(AUDIO_RAW, AUDIO_PROCESSED)

    # 2. Transcribe using Whisper
    print("\nStep 2: Transcribing audio with Whisper...")
    transcribe_audio(AUDIO_PROCESSED, ASR_TRANSCRIPTS)

    # 3. Segment transcripts
    print("\nStep 3: Segmenting transcripts...")
    segment_transcripts(
        input_dir=ASR_TRANSCRIPTS,
        output_dir=SEGMENTS_DIR
    )

    # 4. Summarize segments
    print("\nStep 4: Summarizing segments...")
    summarize_segments()

    # 5. Keyword extraction
    print("\nStep 5: Extracting keywords...")
    run_keyword_extraction()

    # 6. Evaluate ASR
    print("\nStep 6: Evaluating ASR quality...")
    evaluate_asr(
        reference_dir=REFERENCE_TRANSCRIPTS,
        hypothesis_dir=ASR_TRANSCRIPTS,
        output_path=RESULTS_PATH
    )

    print("\n===== PIPELINE COMPLETED SUCCESSFULLY =====\n")
    print("Generated Outputs:")
    print("• ASR transcripts → transcripts/asr/")
    print("• Segments        → segments/")
    print("• Summaries       → transcripts/final/")
    print("• Keywords        → docs/keywords.txt")
    print("• Evaluation      → results/asr_evaluation.csv")


if __name__ == "__main__":
    main()
