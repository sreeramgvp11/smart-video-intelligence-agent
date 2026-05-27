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

import cv2


def generate_thumbnail(video_path: Path) -> Path:
    thumbnail_path = PROCESSED_DIR / f"{video_path.stem}_thumbnail.jpg"

    command = [
        "ffmpeg",
        "-y",
        "-i", str(video_path),
        "-ss", "00:00:03",
        "-vframes", "1",
        str(thumbnail_path)
    ]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Thumbnail generation failed: {result.stderr}")

    return thumbnail_path


def detect_scenes(video_path: Path, threshold: float = 30.0) -> list:
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise RuntimeError("Could not open video for scene detection")

    fps = cap.get(cv2.CAP_PROP_FPS)
    scenes = []

    success, prev_frame = cap.read()
    if not success:
        cap.release()
        return scenes

    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    frame_number = 1

    while True:
        success, frame = cap.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        score = diff.mean()

        if score > threshold:
            timestamp = round(frame_number / fps, 2)
            scenes.append({
                "timestamp": timestamp,
                "change_score": round(float(score), 2)
            })

        prev_gray = gray
        frame_number += 1

    cap.release()

    return scenes[:20]