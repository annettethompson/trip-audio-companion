"""
Duration guard — ensures episodes are never under 60 minutes.

Pre-TTS: estimate from word count.
Post-TTS: measure actual MP3 duration.
"""
from pathlib import Path
from mutagen.mp3 import MP3


WORDS_PER_MINUTE = 145
MINIMUM_MINUTES = 60
TARGET_MINUTES = 65
BONUS_CHAPTER_MIN_WORDS = 1500
BONUS_CHAPTER_MAX_WORDS = 2500


def estimate_duration_minutes(text: str) -> float:
    word_count = len(text.split())
    return word_count / WORDS_PER_MINUTE


def check_pre_tts(text: str) -> dict:
    estimated = estimate_duration_minutes(text)
    word_count = len(text.split())
    needs_expansion = estimated < TARGET_MINUTES

    return {
        "word_count": word_count,
        "estimated_minutes": round(estimated, 1),
        "target_minutes": TARGET_MINUTES,
        "minimum_minutes": MINIMUM_MINUTES,
        "needs_expansion": needs_expansion,
        "words_needed": max(0, int((TARGET_MINUTES - estimated) * WORDS_PER_MINUTE)),
    }


def check_post_tts(mp3_path: Path) -> dict:
    audio = MP3(str(mp3_path))
    duration_seconds = audio.info.length
    duration_minutes = duration_seconds / 60

    return {
        "path": str(mp3_path),
        "duration_seconds": round(duration_seconds, 1),
        "duration_minutes": round(duration_minutes, 2),
        "passes": duration_minutes >= MINIMUM_MINUTES,
        "minimum_minutes": MINIMUM_MINUTES,
        "deficit_minutes": max(0, round(MINIMUM_MINUTES - duration_minutes, 2)),
    }
