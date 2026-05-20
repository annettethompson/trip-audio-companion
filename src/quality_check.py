"""
Quality checks before and after episode generation.
"""
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


def check_no_wikipedia(citations_text: str) -> bool:
    banned = ["wikipedia.org", "wikimedia.org"]
    for b in banned:
        if b in citations_text.lower():
            return False
    return True


def run_pre_flight(script_text: str, citations_text: str) -> dict:
    word_count = len(script_text.split())
    estimated_minutes = round(word_count / 137.75, 1)  # rate-adjusted WPM at -5%
    has_citations = len(citations_text.strip()) > 0
    no_wiki = check_no_wikipedia(citations_text)
    duration_passes = estimated_minutes >= 60

    results = {
        "word_count": word_count,
        "estimated_minutes": estimated_minutes,
        "has_citations": has_citations,
        "no_wikipedia": no_wiki,
        "passes": duration_passes and has_citations and no_wiki,
    }

    table = Table(title="Pre-Flight Quality Check")
    table.add_column("Check", style="cyan")
    table.add_column("Result", style="green")
    table.add_column("Value")

    table.add_row("Estimated >= 60 min", "✅" if duration_passes else "❌", f"{estimated_minutes} min")
    table.add_row("Citations present", "✅" if has_citations else "❌", "")
    table.add_row("No Wikipedia", "✅" if no_wiki else "❌", "")

    console.print(table)
    return results
