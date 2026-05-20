"""
Trip Audio Companion CLI
python -m src.main create-episode --trip config/trip.yaml --topic "Colorado Hot Springs Geology"
"""
import typer
from pathlib import Path
from rich.console import Console
from rich import print as rprint

app = typer.Typer(help="Trip Audio Companion — 60+ minute educational MP3 episodes for road trips")
console = Console()


def _check_ffmpeg():
    """Verify ffmpeg is on PATH. Fail fast with a clear message if not."""
    import shutil
    if shutil.which("ffmpeg") is None:
        console.print(
            "[bold red]ERROR:[/bold red] ffmpeg not found on PATH.\n"
            "Install ffmpeg: https://ffmpeg.org/download.html\n"
            "  Windows: winget install ffmpeg\n"
            "  Or: choco install ffmpeg"
        )
        raise typer.Exit(code=1)


def _ensure_dirs():
    """Create output directories if they don't exist."""
    _check_ffmpeg()
    dirs = [
        Path("outputs/scripts"),
        Path("outputs/audio_segments"),
        Path("outputs/final_mp3s"),
        Path("outputs/citations"),
        Path("data/raw_sources"),
        Path("data/cleaned_sources"),
        Path("data/notes"),
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


@app.command()
def create_episode(
    trip: Path = typer.Option("config/trip.yaml", help="Path to trip.yaml"),
    topic: str = typer.Option(..., help="Episode topic"),
    output_dir: Path = typer.Option(Path("outputs"), help="Output directory"),
):
    """Create a single 60+ minute episode for a topic."""
    _ensure_dirs()
    console.print(f"[bold cyan]Creating episode:[/bold cyan] {topic}")
    console.print(f"Trip config: {trip}")
    console.print("[yellow]Full pipeline not yet implemented — scaffold in place.[/yellow]")


@app.command()
def verify_duration(
    mp3: Path = typer.Argument(..., help="Path to MP3 file"),
):
    """Check if an MP3 meets the 60-minute minimum. Prints PASS or FAIL with next steps."""
    _ensure_dirs()
    from src.duration_guard import enforce_minimum_duration
    result = enforce_minimum_duration(mp3)
    if not result["passes"]:
        rprint(
            f"[red]Run: python -m src.main add-bonus-if-short {mp3}[/red]"
        )
        raise typer.Exit(code=1)


@app.command()
def add_bonus_if_short(
    mp3: Path = typer.Argument(..., help="Path to MP3 that failed duration check"),
):
    """Generate and append a bonus chapter if episode is under 60 minutes."""
    _ensure_dirs()
    from src.duration_guard import check_post_tts
    result = check_post_tts(mp3)
    if result["passes"]:
        rprint(f"[green]Episode already meets minimum: {result['duration_minutes']} min. No bonus needed.[/green]")
        return
    console.print(f"[yellow]Bonus chapter generation not yet implemented. Deficit: {result['deficit_minutes']} min[/yellow]")


@app.command()
def create_trip_series(
    trip: Path = typer.Option("config/trip.yaml", help="Path to trip.yaml"),
):
    """Create all episodes for a trip."""
    _ensure_dirs()
    console.print("[yellow]Full series generation not yet implemented.[/yellow]")


@app.command()
def build_companion_page(
    episode_script: Path = typer.Argument(..., help="Path to episode .md script"),
    output_dir: Path = typer.Option(Path("web/episodes"), help="Output directory"),
):
    """Build a phone-optimized companion webpage for an episode."""
    _ensure_dirs()
    from src.companion_page_generator import CompanionPageGenerator

    console.print(f"[bold cyan]Building companion page for:[/bold cyan] {episode_script}")

    gen = CompanionPageGenerator()
    out = gen.build(episode_script=episode_script, output_dir=output_dir)

    console.print(f"[green]Companion page written to:[/green] {out}")
    console.print(f"[dim]Deploy web/ to Cloudflare Pages — page will be at //{out.parent.name}/[/dim]")


def main():
    app()


if __name__ == "__main__":
    main()
