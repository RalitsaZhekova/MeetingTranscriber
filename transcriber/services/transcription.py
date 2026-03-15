import json
from pathlib import Path

from faster_whisper import WhisperModel


def get_whisper_model(model_size: str = "medium") -> WhisperModel:
    """
    Create a Whisper model instance.

    model_size options commonly include:
    tiny, base, small, medium, large-v3, large-v3-turbo
    """
    return WhisperModel(
        model_size,
        device="cpu",
        compute_type="int8",
    )


def transcribe_audio(
    audio_path: str | Path,
    model_size: str = "medium",
    language: str | None = None,
):
    """
    language:
    - None => auto-detect
    - "en" => force English
    - "bg" => force Bulgarian
    """
    audio_path = Path(audio_path)

    model = get_whisper_model(model_size=model_size)

    transcribe_kwargs = {
        "audio": str(audio_path),
        "task": "transcribe",
        "vad_filter": True,
        "word_timestamps": False,
    }

    if language:
        transcribe_kwargs["language"] = language

    segments, info = model.transcribe(**transcribe_kwargs)

    raw_segments = []

    for segment in segments:
        raw_segments.append(
            {
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "text": segment.text.strip(),
            }
        )

    info_data = {
        "language": getattr(info, "language", None),
        "language_probability": getattr(info, "language_probability", None),
        "duration": getattr(info, "duration", None),
        "requested_language": language if language else "auto",
    }

    return {
        "info": info_data,
        "segments": raw_segments,
    }


def save_transcript_json(output_path: str | Path, payload: dict) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    return output_path
