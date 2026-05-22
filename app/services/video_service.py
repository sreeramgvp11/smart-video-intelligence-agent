from pathlib import Path
import subprocess
import uuid


UPLOAD_DIR = Path("data/uploads")
PROCESSED_DIR = Path("data/processed")

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_video(file) -> Path:
    file_id = str(uuid.uuid4())
    extension = Path(file.filename).suffix or ".mp4"

    video_path = UPLOAD_DIR / f"{file_id}{extension}"

    with open(video_path, "wb") as buffer:
        buffer.write(file.file.read())

    return video_path


def extract_audio(video_path: Path) -> Path:
    audio_path = PROCESSED_DIR / f"{video_path.stem}.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "16000",
        "-ac", "1",
        str(audio_path)
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")

    return audio_path