from fastapi import FastAPI, UploadFile, File
from app.services.video_service import save_uploaded_video, extract_audio
from app.agents.workflow import build_workflow

app = FastAPI()

workflow = build_workflow()


@app.post("/upload-video")
def upload_video(file: UploadFile = File(...)):
    video_path = save_uploaded_video(file)
    audio_path = extract_audio(video_path)

    result = workflow.invoke({
        "audio_path": str(audio_path),
        "video_path": str(video_path)
    })

    return {
        "status": "success",
        "video_path": str(video_path),
        "audio_path": str(audio_path),
        "result": result
    }