from collections import OrderedDict


def segment_overlap(start_a: float, end_a: float, start_b: float, end_b: float) -> float:
    return max(0.0, min(end_a, end_b) - max(start_a, start_b))


def relabel_speakers(diarization_segments: list[dict]) -> dict:
    """
    Convert pyannote labels like SPEAKER_00 into Speaker 1, Speaker 2, ...
    preserving first-seen order.
    """
    mapping = OrderedDict()
    counter = 1

    for seg in diarization_segments:
        raw_label = seg["speaker"]
        if raw_label not in mapping:
            mapping[raw_label] = f"Speaker {counter}"
            counter += 1

    return mapping


def assign_speakers_to_transcript(
    transcript_segments: list[dict],
    diarization_segments: list[dict],
) -> list[dict]:
    speaker_map = relabel_speakers(diarization_segments)

    aligned = []

    for t_seg in transcript_segments:
        best_overlap = 0.0
        best_speaker = "Speaker ?"

        for d_seg in diarization_segments:
            overlap = segment_overlap(
                t_seg["start"],
                t_seg["end"],
                d_seg["start"],
                d_seg["end"],
            )

            if overlap > best_overlap:
                best_overlap = overlap
                best_speaker = speaker_map[d_seg["speaker"]]

        aligned.append(
            {
                "start": t_seg["start"],
                "end": t_seg["end"],
                "speaker": best_speaker,
                "text": t_seg["text"],
            }
        )

    return merge_consecutive_speaker_segments(aligned)


def merge_consecutive_speaker_segments(segments: list[dict]) -> list[dict]:
    if not segments:
        return []

    merged = [segments[0].copy()]

    for seg in segments[1:]:
        last = merged[-1]

        if seg["speaker"] == last["speaker"]:
            last["end"] = seg["end"]
            last["text"] = f'{last["text"]} {seg["text"]}'.strip()
        else:
            merged.append(seg.copy())

    return merged


def format_timestamp(seconds: float) -> str:
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02}:{minutes:02}:{secs:02}"


def build_speaker_labeled_text(segments: list[dict]) -> str:
    lines = []

    for seg in segments:
        lines.append(
            f"[{format_timestamp(seg['start'])} - {format_timestamp(seg['end'])}] "
            f"{seg['speaker']}: {seg['text']}"
        )

    return "\n".join(lines)
