"""
Generate the inter-chapter chime sound used in Trip Audio Companion episodes.
A gentle two-note bell chime (C6 then A5) with natural decay.

Usage: python scripts/generate_chime.py
Output: outputs/audio/chime.mp3
"""
from pathlib import Path
from pydub import AudioSegment
from pydub.generators import Sine


def generate_chime() -> AudioSegment:
    """Generate a soft two-note bell chime."""
    # First note: C6 (1047 Hz) -- brighter attack note
    note1 = (
        Sine(1047).to_audio_segment(duration=900)
        + Sine(2094).to_audio_segment(duration=600) - 12   # octave harmonic, quieter
    )
    note1 = note1.fade_in(15).fade_out(600) - 8  # soften overall

    # Brief gap between notes
    gap = AudioSegment.silent(duration=120)

    # Second note: A5 (880 Hz) -- warmer resolution note
    note2 = (
        Sine(880).to_audio_segment(duration=1100)
        + Sine(1760).to_audio_segment(duration=800) - 14
    )
    note2 = note2.fade_in(10).fade_out(800) - 6

    # Short silence before and after for breathing room
    pad = AudioSegment.silent(duration=400)

    chime = pad + note1 + gap + note2 + pad
    return chime


if __name__ == "__main__":
    out_dir = Path("outputs/audio")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "chime.mp3"

    chime = generate_chime()
    chime.export(str(out_path), format="mp3", bitrate="128k")
    print(f"Chime generated: {out_path} ({len(chime)}ms, {out_path.stat().st_size // 1024} KB)")
