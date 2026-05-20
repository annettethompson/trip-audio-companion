"""
TTS engine for Trip Audio Companion.
Default: edge-tts (free, Microsoft neural voices, no API key needed).
"""
import asyncio
from pathlib import Path
import edge_tts
from rich.console import Console

console = Console()

DEFAULT_VOICE = "en-GB-RyanNeural"
DEFAULT_RATE = "-5%"
DEFAULT_PITCH = "-2Hz"


async def synthesize_segment_async(
    text: str,
    output_path: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> Path:
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(str(output_path))
    return output_path


def synthesize_segment(
    text: str,
    output_path: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> Path:
    asyncio.run(synthesize_segment_async(text, output_path, voice, rate, pitch))
    console.print(f"[green]Synthesized:[/green] {output_path.name}")
    return output_path


def synthesize_chapter(
    chapter_text: str,
    chapter_name: str,
    output_dir: Path,
    voice: str = DEFAULT_VOICE,
) -> Path:
    output_path = output_dir / f"{chapter_name}.mp3"
    output_dir.mkdir(parents=True, exist_ok=True)
    return synthesize_segment(chapter_text, output_path, voice=voice)
