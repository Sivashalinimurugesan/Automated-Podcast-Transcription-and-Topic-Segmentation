from faster_whisper import WhisperModel
import logging
import torch
import json
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Transcriber:
    def __init__(self, model_size="base", device=None, compute_type="int8"):
        """
        Initializes the Faster-Whisper model efficiently.
        """
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device
            
        logger.info(f"Loading Faster-Whisper model: {model_size} on {self.device} with {compute_type}")
        
        try:
            self.model = WhisperModel(model_size, device=self.device, compute_type=compute_type)
        except Exception as e:
            logger.warning(f"Failed to load with {compute_type}, falling back to float32. Error: {e}")
            try:
                 self.model = WhisperModel(model_size, device=self.device, compute_type="float32")
            except Exception as e2:
                 logger.error(f"Critical error loading model: {e2}")
                 raise

    def transcribe(self, audio_path):
        """
        Transcribes audio file and returns result dict with text, segments, and info.
        Uses beam search and VAD (silence filtering).
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        logger.info(f"Transcribing {audio_path}...")
        try:
            # vad_filter=True enables silence filtering
            segments_generator, info = self.model.transcribe(
                audio_path, 
                beam_size=5, 
                vad_filter=True
            )
            
            segments = []
            full_text = ""
            
            for segment in segments_generator:
                segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip()
                })
                full_text += segment.text + " "
                
            logger.info(f"Transcription complete. Detected language: {info.language} (probability: {info.language_probability:.2f})")
            
            return {
                "text": full_text.strip(),
                "segments": segments,
                "language": info.language
            }
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise

    def save_outputs(self, result, audio_filename, transcript_dir="transcripts", segments_dir="segments"):
        """
        Saves full transcription text to transcripts/ and segments to segments/.
        """
        try:
            # Ensure directories exist
            os.makedirs(transcript_dir, exist_ok=True)
            os.makedirs(segments_dir, exist_ok=True)
            
            base_name = os.path.splitext(audio_filename)[0]
            
            # Save Text (.txt)
            txt_path = os.path.join(transcript_dir, f"{base_name}.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            logger.info(f"Saved transcript to {txt_path}")
            
            # Save Segments (.json)
            # Also saving language info in the same file for completeness? 
            # Request asked for "Detailed segment data". I'll save the segments list wrapped in a dict or just the list.
            # Usually strict JSON structure is preferred.
            json_path = os.path.join(segments_dir, f"{base_name}.json")
            output_data = {
                "language": result['language'],
                "segments": result['segments']
            }
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved segments to {json_path}")
            
            return txt_path, json_path
            
        except Exception as e:
            logger.error(f"Failed to save outputs: {e}")
            raise

    def diarize_audio(self, audio_path, hf_token):
        """
        Performs speaker diarization using pyannote.audio.
        """
        if not hf_token:
            logger.warning("No Hugging Face token provided. Skipping diarization.")
            return None
            
        logger.info("Initializing Diarization Pipeline (pyannote.audio)...")
        try:
            from pyannote.audio import Pipeline
            pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=hf_token
            )
            
            if pipeline is None:
                logger.error("Failed to download/load diarization pipeline (check HF token and model access permissions).")
                return None
                
            # Move to GPU if available
            if self.device == "cuda":
                pipeline.to(torch.device("cuda"))
                
            logger.info("Running diarization...")
            diarization = pipeline(audio_path)
            
            # Convert to list of segments
            # diarization.itertracks(yield_label=True) yields (segment, track, label)
            # segment has .start and .end
            speaker_segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                speaker_segments.append({
                    "start": turn.start,
                    "end": turn.end,
                    "speaker": speaker
                })
            
            logger.info(f"Diarization complete. Found {len(speaker_segments)} speaker turns.")
            return speaker_segments
            
        except ImportError:
            logger.error("pyannote.audio not installed. Cannot perform diarization.")
            return None
        except Exception as e:
            logger.error(f"Diarization failed: {e}")
            return None

    def assign_speakers(self, transcript_segments, speaker_segments):
        """
        Assigns speakers to transcript segments based on temporal overlap.
        """
        if not speaker_segments:
            for seg in transcript_segments:
                seg['speaker'] = "Speaker 1"
            return transcript_segments
            
        for t_seg in transcript_segments:
            t_start = t_seg['start']
            t_end = t_seg['end']
            
            # Find all speaker turns that overlap with this transcript segment
            overlaps = []
            for s_seg in speaker_segments:
                # Calculate intersection
                s_start = max(t_start, s_seg['start'])
                s_end = min(t_end, s_seg['end'])
                duration = max(0, s_end - s_start)
                
                if duration > 0:
                    overlaps.append((s_seg['speaker'], duration))
            
            if overlaps:
                # Assign to speaker with max overlap duration
                # Sum duration per speaker in case of fragmented turns
                speaker_durations = {}
                for spk, dur in overlaps:
                    speaker_durations[spk] = speaker_durations.get(spk, 0) + dur
                    
                major_speaker = max(speaker_durations, key=speaker_durations.get)
                t_seg['speaker'] = major_speaker
            else:
                # No overlap found (rare), defaults to nearest? or just "Unknown"
                # Let's try to look for the closest speaker segment
                t_seg['speaker'] = "Unknown" # Or default to previous?
        
        # Post-processing: fill Unknown with nearest neighbors
        for i, seg in enumerate(transcript_segments):
            if seg['speaker'] == "Unknown":
                if i > 0:
                    seg['speaker'] = transcript_segments[i-1]['speaker']
                elif i < len(transcript_segments) - 1:
                     # Wait for next loop to fill? No, just assign "Speaker 00" default if absolute start
                     seg['speaker'] = "SPEAKER_00" 
                     
        return transcript_segments

    def process_file(self, audio_path, transcript_dir, segments_dir, hf_token=None):
        """
        Orchestrates transcription, optional diarization, and saving.
        """
        # 1. Transcribe
        result = self.transcribe(audio_path)
        
        # 2. Diarize (if token provided)
        if hf_token:
            speaker_segments = self.diarize_audio(audio_path, hf_token)
            if speaker_segments:
                result['segments'] = self.assign_speakers(result['segments'], speaker_segments)
            else:
                # Default if diarization failed/skipped
                for seg in result['segments']:
                    seg['speaker'] = "Speaker 1"
        else:
             for seg in result['segments']:
                seg['speaker'] = "Speaker 1"
        
        # 3. Save
        filename = os.path.basename(audio_path)
        self.save_outputs(result, filename, transcript_dir, segments_dir)
        return result
