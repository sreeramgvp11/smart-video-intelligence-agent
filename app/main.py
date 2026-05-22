from fastapi import FastAPI, UploadFile, File
from app.services.video_service import save_uploaded_video, extract_audio
from app.services.transcription_service import transcribe_audio

app = FastAPI(title="Smart Video Intelligence Agent")


@app.get("/")
def root():
    return {
        "message": "Smart Video Intelligence Agent API is running"
    }


@app.post("/upload-video")
def upload_video(file: UploadFile = File(...)):
    video_path = save_uploaded_video(file)
    audio_path = extract_audio(video_path)
    transcript = transcribe_audio(audio_path)

    return {
        "status": "success",
        "video_path": str(video_path),
        "audio_path": str(audio_path),
        "transcript": transcript
    }