"""
Citation exporter for Trip Audio Companion.

After script generation, extracts all inline citation markers and produces:
- outputs/citations/{episode_slug}_citations.md — human-readable citation list
- outputs/citations/{episode_slug}_citations.json — machine-readable for future use

Citation fields (per config/sources.yaml):
- title, url, date_accessed, topic, tier, author, publisher

Validates that no banned sources (wikipedia.org, wikimedia.org) appear in final citations.
"""


def export_citations(script_text: str, source_metadata: list[dict], episode_slug: str, output_dir) -> dict:
    """
    Extract citation markers from script and write citation files.
    Returns dict with paths to md and json outputs.
    """
    pass
