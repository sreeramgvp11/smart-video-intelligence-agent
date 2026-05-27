from typing import TypedDict
from langgraph.graph import StateGraph
from pathlib import Path
from app.services.transcription_service import transcribe_audio
from app.services.summary_service import summarize_transcript
from app.services.video_service import generate_thumbnail, detect_scenes


class VideoState(TypedDict, total=False):
    video_path: str
    audio_path: str
    transcript: dict
    intelligence: dict
    visual_analysis: dict


def transcription_agent(state: VideoState):
    audio_path = Path(state["audio_path"])

    transcript = transcribe_audio(audio_path)
    return {"transcript": transcript}

def summarization_agent(state: VideoState):
    transcript = Path(state["transcript"])
    intelligence = summarize_transcript(transcript)
    return {"intelligence": intelligence}


def visual_analysis_agent(state: VideoState):
    video_path = Path(state["video_path"])

    thumbnail_path = generate_thumbnail(video_path)
    scenes = detect_scenes(video_path)

    return {
        "visual_analysis": {
            "thumbnail_path": str(thumbnail_path),
            "scene_changes": scenes,
            "scene_count": len(scenes)
        }
    }


def build_workflow():
    graph = StateGraph(VideoState)

    graph.add_node("transcribe", transcription_agent)
    graph.add_node("summarize", summarization_agent)
    graph.add_node("visual_analysis", visual_analysis_agent)

    graph.set_entry_point("transcribe")
    graph.add_edge("transcribe", "summarize")
    graph.add_edge("summarize", "visual_analysis")
    graph.set_finish_point("visual_analysis")

    return graph.compile()