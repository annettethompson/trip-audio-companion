"""
Synthesize the Pagosa Springs episode from script markdown files.
Usage: python scripts/synthesize_pagosa.py
"""
import asyncio
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import edge_tts
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, ID3NoHeaderError
import json
from rich.console import Console

console = Console()

VOICE = "en-US-ChristopherNeural"
RATE = "-5%"
PITCH = "-2Hz"
MAX_CHUNK_CHARS = 4000
SECTION_PAUSE_MS = 3500
EPISODE_TITLE = "The Deepest Spring in the World: Pagosa Springs, the San Juan High Country, and the Battle for the Pagosa"
EPISODE_SLUG = "pagosa"

SCRIPTS_DIR = Path("outputs/pagosa_scripts")
SEGMENTS_DIR = Path("outputs/audio_segments_pagosa")
FINAL_DIR = Path("outputs/final_mp3s")
CITATIONS_DIR = Path("outputs/citations")

for d in [SEGMENTS_DIR, FINAL_DIR, CITATIONS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

CHAPTERS = [
    ("00_intro.md", "The Smell Arrives First"),
    ("01_deepest_spring.md", "The Deepest Spring in the World"),
    ("02_crossing_wolf_creek.md", "Crossing Wolf Creek"),
    ("03_battle_for_the_springs.md", "The Battle for the Springs"),
    ("04_what_the_water_does.md", "What the Water Does"),
    ("05_the_weminuche.md", "The Weminuche"),
    ("06_engelmann_spruce.md", "Engelmann Spruce and the High Forest"),
    ("07_moose_in_colorado.md", "Moose in Colorado"),
    ("08_merriams_turkey.md", "Merriam's Turkey"),
    ("09_san_juan_river.md", "The River at the Bottom of the World"),
    ("10_wolf_creek_1923.md", "1923 Moment: The Road Over the Mountain"),
    ("11_come_back_for_this.md", "Come Back For This"),
]


def extract_narration(md_text: str) -> str:
    """Strip markdown metadata lines, return only narration text."""
    lines = md_text.split("\n")
    narration_lines = []
    skip_topic_inventory = False
    for line in lines:
        if line.startswith("#"):
            continue
        if line.startswith("*Estimated duration") or line.startswith("*Word count"):
            continue
        if line.startswith("*Sources"):
            continue
        if line.strip() == "---":
            continue
        if "Topic inventory:" in line:
            skip_topic_inventory = True
            continue
        if skip_topic_inventory:
            if line.startswith("-") and ("HOME" in line or "REFERENCE" in line):
                continue
            elif line.strip() == "":
                continue
            else:
                skip_topic_inventory = False
                narration_lines.append(line)
                continue
        narration_lines.append(line)
    return "\n".join(narration_lines).strip()


def split_into_chunks(text: str, max_chars: int = MAX_CHUNK_CHARS) -> list:
    """Split text on sentence boundaries."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current = (current + " " + sentence).strip()
        else:
            if current:
                chunks.append(current)
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


async def synthesize_text(text: str, output_path: Path) -> Path:
    """Synthesize text to MP3, chunking if needed."""
    chunks = split_into_chunks(text)
    console.print(f"  Chunks: {len(chunks)}")

    if len(chunks) == 1:
        communicate = edge_tts.Communicate(chunks[0], VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(str(output_path))
    else:
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_paths = []
            for i, chunk in enumerate(chunks):
                chunk_path = Path(tmpdir) / f"chunk_{i:03d}.mp3"
                communicate = edge_tts.Communicate(chunk, VOICE, rate=RATE, pitch=PITCH)
                await communicate.save(str(chunk_path))
                temp_paths.append(chunk_path)

            combined = AudioSegment.empty()
            for cp in temp_paths:
                combined += AudioSegment.from_mp3(str(cp))
            combined.export(str(output_path), format="mp3", bitrate="128k")

    if not output_path.exists() or output_path.stat().st_size < 1024:
        raise RuntimeError(f"TTS produced empty output for {output_path.name}")

    return output_path


def get_chime() -> AudioSegment:
    """Load the inter-chapter chime, generating it if not present."""
    chime_path = Path("outputs/audio/chime.mp3")
    if chime_path.exists():
        return AudioSegment.from_mp3(str(chime_path))
    # Fallback: generate inline if file missing
    from pydub.generators import Sine
    note1 = (Sine(1047).to_audio_segment(duration=900) + Sine(2094).to_audio_segment(duration=600) - 12).fade_in(15).fade_out(600) - 8
    gap = AudioSegment.silent(duration=120)
    note2 = (Sine(880).to_audio_segment(duration=1100) + Sine(1760).to_audio_segment(duration=800) - 14).fade_in(10).fade_out(800) - 6
    pad = AudioSegment.silent(duration=400)
    return pad + note1 + gap + note2 + pad


def format_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


async def main():
    console.print("[bold cyan]Trip Audio Companion -- TTS Synthesis (Pagosa Episode)[/bold cyan]")
    console.print(f"Voice: {VOICE} | Rate: {RATE} | Pitch: {PITCH}\n")

    segment_paths = []
    chapter_names = []

    for filename, chapter_name in CHAPTERS:
        script_path = SCRIPTS_DIR / filename
        if not script_path.exists():
            console.print(f"[yellow]Warning: Skipping {filename} -- not found[/yellow]")
            continue

        segment_path = SEGMENTS_DIR / filename.replace(".md", ".mp3")

        if segment_path.exists() and segment_path.stat().st_size > 1024:
            console.print(f"[dim]-> {chapter_name}: already synthesized, skipping[/dim]")
            segment_paths.append(segment_path)
            chapter_names.append(chapter_name)
            continue

        console.print(f"[cyan]-> Synthesizing:[/cyan] {chapter_name}")

        try:
            md_text = script_path.read_text(encoding="utf-8")
            narration = extract_narration(md_text)
            word_count = len(narration.split())
            console.print(f"  Words: {word_count}")

            await synthesize_text(narration, segment_path)

            audio_info = MP3(str(segment_path))
            duration = audio_info.info.length
            console.print(f"  [green]Done:[/green] {format_time(duration)} ({segment_path.stat().st_size // 1024} KB)")

            segment_paths.append(segment_path)
            chapter_names.append(chapter_name)
        except Exception as e:
            console.print(f"  [red]ERROR in {filename}: {e}[/red]")
            console.print(f"  [yellow]Skipping chapter and continuing...[/yellow]")
            continue

    if not segment_paths:
        console.print("[red]No segments synthesized. Check outputs/pagosa_scripts/ directory.[/red]")
        return

    console.print(f"\n[cyan]Building chapter timestamps...[/cyan]")
    chime = get_chime()
    chapters_data = []
    current_seconds = 0.0

    for seg_path, name in zip(segment_paths, chapter_names):
        audio = AudioSegment.from_mp3(str(seg_path))
        duration_s = len(audio) / 1000
        chapters_data.append({
            "name": name,
            "start_seconds": round(current_seconds, 1),
            "start_formatted": format_time(current_seconds),
            "duration_seconds": round(duration_s, 1),
        })
        current_seconds += duration_s + (len(chime) / 1000)

    console.print(f"\n[cyan]Stitching {len(segment_paths)} segments...[/cyan]")
    combined = AudioSegment.empty()
    for i, seg_path in enumerate(segment_paths):
        combined += AudioSegment.from_mp3(str(seg_path))
        if i < len(segment_paths) - 1:
            combined += chime

    final_path = FINAL_DIR / f"{EPISODE_SLUG}_episode.mp3"
    console.print(f"[cyan]Exporting final MP3...[/cyan]")
    combined.export(str(final_path), format="mp3", bitrate="128k")

    try:
        tags = ID3(str(final_path))
    except ID3NoHeaderError:
        tags = ID3()
    tags.add(TIT2(encoding=3, text=[EPISODE_TITLE]))
    tags.add(TPE1(encoding=3, text=["Trip Audio Companion"]))
    tags.add(TALB(encoding=3, text=["Colorado Hot Springs Trip 2026"]))
    tags.save(str(final_path))

    final_audio = MP3(str(final_path))
    final_duration = final_audio.info.length
    final_minutes = final_duration / 60

    console.print(f"\n[bold]Final MP3:[/bold] {final_path}")
    console.print(f"[bold]Duration:[/bold] {format_time(final_duration)} ({final_minutes:.1f} minutes)")

    if final_minutes >= 65:
        console.print(f"[bold green]PASSES 65-minute minimum[/bold green]")
    else:
        console.print(f"[bold red]FAILS -- {65 - final_minutes:.1f} minutes short[/bold red]")

    timestamps_path = FINAL_DIR / f"{EPISODE_SLUG}_chapters.json"
    with open(timestamps_path, "w") as f:
        json.dump({
            "episode": EPISODE_TITLE,
            "total_duration": format_time(final_duration),
            "total_minutes": round(final_minutes, 2),
            "chapters": chapters_data
        }, f, indent=2)
    console.print(f"[green]Chapter timestamps:[/green] {timestamps_path}")

    console.print(f"\n[bold green]Episode ready:[/bold green] {final_path}")


if __name__ == "__main__":
    asyncio.run(main())
