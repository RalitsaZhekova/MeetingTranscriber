import shutil
import subprocess
from pathlib import Path


def ffmpeg_exists() -> bool:
    return shutil.which("ffmpeg") is not None


def build_normalized_audio_path(input_path: str | Path) -> Path:
    input_path = Path(input_path)
    return input_path.with_suffix(".normalized.wav")


def normalize_audio_to_wav(input_path: str | Path, output_path: str | Path) -> Path:
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not ffmpeg_exists():
        raise RuntimeError("FFmpeg is not installed or not available in PATH.")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(output_path),
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg normalization failed.\n"
            f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
        )

    if not output_path.exists():
        raise RuntimeError("Normalized WAV file was not created.")

    return output_path
