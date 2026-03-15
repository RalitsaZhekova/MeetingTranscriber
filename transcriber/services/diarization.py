import os
from pathlib import Path

import torch
import soundfile as sf
from pyannote.audio import Pipeline



def get_diarization_pipeline():
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise RuntimeError("HF_TOKEN is missing. Set it in your .env file.")

    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-community-1",
        token=hf_token,
    )
    return pipeline


def load_audio_for_pyannote(audio_path: str | Path) -> dict:
    audio_path = Path(audio_path)

    waveform, sample_rate = sf.read(str(audio_path), always_2d=True)
    waveform = waveform.T
    waveform_tensor = torch.from_numpy(waveform).float()

    return {
        "waveform": waveform_tensor,
        "sample_rate": sample_rate,
    }


def diarize_audio(
    audio_path: str | Path,
    num_speakers: int | None = None,
):
    pipeline = get_diarization_pipeline()
    audio_input = load_audio_for_pyannote(audio_path)

    output = pipeline(
        audio_input,
        num_speakers=num_speakers,
    )

    segments = []

    for turn, speaker in output.speaker_diarization:
        segments.append(
            {
                "start": round(turn.start, 2),
                "end": round(turn.end, 2),
                "speaker": speaker,
            }
        )

    return segments
