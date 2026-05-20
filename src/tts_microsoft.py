"""
TTS engine for Trip Audio Companion.
Default: edge-tts (free, Microsoft neural voices, no API key needed).
"""
import asyncio
import re
import tempfile
from pathlib import Path
import edge_tts
from pydub import AudioSegment
from rich.console import Console

console = Console()

DEFAULT_VOICE = "en-GB-RyanNeural"
DEFAULT_RATE = "-5%"
DEFAULT_PITCH = "-2Hz"

MAX_CHUNK_CHARS = 4500  # safe margin below edge-tts limit


def _split_into_chunks(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list[str]:
    """Split text on sentence boundaries to stay under edge-tts char limit."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = (current + " " + sentence).strip()
        else:
            if current:
                chunks.append(current)
            # If a single sentence exceeds max_chars, split on comma/clause
            if len(sentence) > max_chars:
                parts = re.split(r'(?<=[,;])\s+', sentence)
                for part in parts:
                    if len(current) + len(part) + 1 <= max_chars:
                        current = (current + " " + part).strip()
                    else:
                        if current:
                            chunks.append(current)
                        current = part
            else:
                current = sentence
    if current:
        chunks.append(current)
    return chunks


async def synthesize_segment_async(
    text: str,
    output_path: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> Path:
    """Synthesize text to MP3, chunking if text exceeds edge-tts limits."""
    chunks = _split_into_chunks(text)

    if len(chunks) == 1:
        # Single chunk — direct synthesis
        communicate = edge_tts.Communicate(chunks[0], voice, rate=rate, pitch=pitch)
        await communicate.save(str(output_path))
    else:
        # Multiple chunks — synthesize each to a temp file, then concatenate
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = Path(tmpdir) / f"chunk_{i:03d}.mp3"
                communicate = edge_tts.Communicate(chunk, voice, rate=rate, pitch=pitch)
                await communicate.save(str(chunk_path))
                temp_paths.append(chunk_path)

            # Concatenate all chunks
            combined = AudioSegment.empty()
            for cp in temp_paths:
                combined += AudioSegment.from_mp3(str(cp))
            combined.export(str(output_path), format="mp3", bitrate="128k")

    # Guard: verify output file is non-empty
    if not output_path.exists() or output_path.stat().st_size < 1024:
        raise RuntimeError(
            f"TTS synthesis produced empty or missing output: {output_path}. "
            "This usually means edge-tts timed out or the text was empty."
        )
    return output_path


def synthesize_segment(
    text: str,
    output_path: Path,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    pitch: str = DEFAULT_PITCH,
) -> Path:
    try:
        asyncio.run(synthesize_segment_async(text, output_path, voice, rate, pitch))
    except RuntimeError as e:
        console.print(f"[bold red]TTS error:[/bold red] {e}")
        raise
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
