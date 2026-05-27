from typing import Dict, List


def summarize_transcript(transcript: Dict) -> Dict:
    text = transcript.get("text", "")
    segments = transcript.get("segments", [])

    return {
        "summary": generate_simple_summary(text),
        "key_moments": extract_key_moments(segments),
        "chapters": generate_chapters(segments)
    }


def generate_simple_summary(text: str, max_sentences: int = 5) -> str:
    if not text:
        return "No transcript available."

    sentences = split_sentences(text)

    if len(sentences) <= max_sentences:
        return text

    selected = sentences[:2]
    selected.append(sentences[len(sentences) // 2])
    selected.extend(sentences[-2:])

    return " ".join(selected)


def split_sentences(text: str) -> List[str]:
    text = text.replace("?", ".").replace("!", ".")
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    return [s + "." for s in sentences]


def extract_key_moments(segments: List[Dict], max_moments: int = 5) -> List[Dict]:
    keywords = [
        "important", "key", "main", "summary", "conclusion",
        "problem", "solution", "result", "because", "therefore",
        "first", "second", "finally"
    ]

    scored = []

    for segment in segments:
        text = segment.get("text", "")
        score = len(text.split())

        for keyword in keywords:
            if keyword in text.lower():
                score += 10

        scored.append({
            "start": segment.get("start"),
            "end": segment.get("end"),
            "text": text,
            "score": score
        })

    scored.sort(key=lambda x: x["score"], reverse=True)

    return [
        {
            "start": item["start"],
            "end": item["end"],
            "text": item["text"]
        }
        for item in scored[:max_moments]
    ]


def generate_chapters(segments: List[Dict], chapter_size: int = 5) -> List[Dict]:
    chapters = []

    for i in range(0, len(segments), chapter_size):
        chunk = segments[i:i + chapter_size]

        if not chunk:
            continue

        chapter_text = " ".join(segment.get("text", "") for segment in chunk)

        chapters.append({
            "title": f"Chapter {len(chapters) + 1}",
            "start": chunk[0].get("start"),
            "end": chunk[-1].get("end"),
            "summary": generate_simple_summary(chapter_text, max_sentences=2)
        })

    return chapters