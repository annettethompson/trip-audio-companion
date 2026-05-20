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


@app.command()
def create_episode(
    trip: Path = typer.Option("config/trip.yaml", help="Path to trip.yaml"),
    topic: str = typer.Option(..., help="Episode topic"),
    output_dir: Path = typer.Option(Path("outputs"), help="Output directory"),
):
    """Create a single 60+ minute episode for a topic."""
    console.print(f"[bold cyan]Creating episode:[/bold cyan] {topic}")
    console.print(f"Trip config: {trip}")
    console.print("[yellow]Full pipeline not yet implemented — scaffold in place.[/yellow]")


@app.command()
def verify_duration(
    mp3: Path = typer.Argument(..., help="Path to MP3 file"),
):
    """Check if an MP3 meets the 60-minute minimum."""
    from src.duration_guard import check_post_tts
    result = check_post_tts(mp3)
    if result["passes"]:
        rprint(f"[green]✅ {result['duration_minutes']} minutes — passes 60-min minimum[/green]")
    else:
        rprint(f"[red]❌ {result['duration_minutes']} minutes — {result['deficit_minutes']} min short of minimum[/red]")


@app.command()
def create_trip_series(
    trip: Path = typer.Option("config/trip.yaml", help="Path to trip.yaml"),
):
    """Create all episodes for a trip."""
    console.print("[yellow]Full series generation not yet implemented.[/yellow]")


if __name__ == "__main__":
    app()
