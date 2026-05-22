from pathlib import Path
from faster_whisper import WhisperModel


# Use "base" first. Later we can switch to "small" or "medium".
model = WhisperModel("base", device="cpu", compute_type="int8")


def transcribe_audio(audio_path: Path) -> dict:
    segments, info = model.transcribe(str(audio_path), beam_size=5)

    transcript_segments = []
    full_text = []

    for segment in segments:
        item = {
            "start": round(segment.start, 2),
            "end": round(segment.end, 2),
            "text": segment.text.strip()
        }

        transcript_segments.append(item)
        full_text.append(segment.text.strip())

    return {
        "language": info.language,
        "duration": round(info.duration, 2),
        "text": " ".join(full_text),
        "segments": transcript_segments
    }
