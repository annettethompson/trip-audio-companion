"""
Stitch audio segments into a single MP3 with chapter markers.
"""
from pathlib import Path
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, COMM
import json


SECTION_PAUSE_MS = 2000   # 2 second pause between major sections
SEGMENT_PAUSE_MS = 1500   # 1.5 second pause between subsections


def stitch_segments(
    segment_paths: list[Path],
    output_path: Path,
    pause_between: int = SECTION_PAUSE_MS,
    episode_title: str = "Trip Audio Companion",
) -> Path:
    silence = AudioSegment.silent(duration=pause_between)
    combined = AudioSegment.empty()

    for i, seg_path in enumerate(segment_paths):
        segment = AudioSegment.from_mp3(str(seg_path))
        combined += segment
        if i < len(segment_paths) - 1:
            combined += silence

    combined.export(str(output_path), format="mp3", bitrate="128k")

    # Tag the MP3 — handle fresh files with no existing ID3 header
    from mutagen.id3 import ID3NoHeaderError
    try:
        tags = ID3(str(output_path))
    except ID3NoHeaderError:
        tags = ID3()

    tags[TIT2.__name__] = TIT2(encoding=3, text=episode_title)
    tags[TPE1.__name__] = TPE1(encoding=3, text="Trip Audio Companion")
    tags.save(str(output_path))

    return output_path


def get_duration_minutes(mp3_path: Path) -> float:
    audio = MP3(str(mp3_path))
    return audio.info.length / 60


def build_chapter_timestamps(
    segment_paths: list[Path],
    chapter_names: list[str],
    pause_ms: int = SECTION_PAUSE_MS,
) -> list[dict]:
    chapters = []
    current_seconds = 0.0

    for i, (seg_path, name) in enumerate(zip(segment_paths, chapter_names)):
        audio = AudioSegment.from_mp3(str(seg_path))
        duration_s = len(audio) / 1000

        chapters.append({
            "index": i,
            "name": name,
            "start_seconds": round(current_seconds, 1),
            "start_formatted": _format_time(current_seconds),
            "duration_seconds": round(duration_s, 1),
        })

        current_seconds += duration_s + (pause_ms / 1000)

    return chapters


def _format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"
