"""
Duration guard — ensures episodes are never under 60 minutes.

Pre-TTS: estimate from word count.
Post-TTS: measure actual MP3 duration.
"""
from pathlib import Path
from mutagen.mp3 import MP3
from rich.console import Console

console = Console()

BASE_WORDS_PER_MINUTE = 145
DEFAULT_RATE_MODIFIER = -0.05  # matches voice.yaml default of "-5%"
MINIMUM_MINUTES = 60
TARGET_MINUTES = 65
BONUS_CHAPTER_MIN_WORDS = 1500
BONUS_CHAPTER_MAX_WORDS = 2500

# Keep backward-compat name pointing at effective WPM at default rate
WORDS_PER_MINUTE = int(BASE_WORDS_PER_MINUTE * (1 + DEFAULT_RATE_MODIFIER))


def estimate_duration_minutes(text: str, rate_modifier: float = DEFAULT_RATE_MODIFIER) -> float:
    """Estimate narration duration accounting for TTS rate modifier.

    rate_modifier: negative = slower (e.g. -0.05 for -5%), positive = faster.
    At -5% rate, effective WPM = 145 * (1 - 0.05) = 137.75
    """
    word_count = len(text.split())
    effective_wpm = BASE_WORDS_PER_MINUTE * (1 + rate_modifier)
    return word_count / effective_wpm


def check_pre_tts(text: str, rate_modifier: float = DEFAULT_RATE_MODIFIER) -> dict:
    estimated = estimate_duration_minutes(text, rate_modifier)
    word_count = len(text.split())
    needs_expansion = estimated < TARGET_MINUTES
    effective_wpm = BASE_WORDS_PER_MINUTE * (1 + rate_modifier)

    return {
        "word_count": word_count,
        "effective_wpm": round(effective_wpm, 1),
        "estimated_minutes": round(estimated, 1),
        "target_minutes": TARGET_MINUTES,
        "minimum_minutes": MINIMUM_MINUTES,
        "needs_expansion": needs_expansion,
        "words_needed": max(0, int((TARGET_MINUTES - estimated) * effective_wpm)),
    }


def enforce_minimum_duration(
    mp3_path: Path,
    minimum_minutes: float = MINIMUM_MINUTES,
) -> dict:
    """
    Check final MP3 duration after stitching.
    Returns result dict. Caller is responsible for generating bonus content if needed.
    """
    result = check_post_tts(mp3_path)

    if not result["passes"]:
        console.print(
            f"[bold red]Warning Duration check FAILED:[/bold red] "
            f"{result['duration_minutes']} min — "
            f"{result['deficit_minutes']} min below {minimum_minutes}-min minimum. "
            f"Bonus chapter required."
        )
    else:
        console.print(
            f"[bold green]Duration check PASSED:[/bold green] "
            f"{result['duration_minutes']} min"
        )

    return result


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
