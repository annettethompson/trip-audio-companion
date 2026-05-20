"""
Outline generator for Trip Audio Companion.

Takes the trip config (topics, route, hot springs) and cleaned sources,
then uses an LLM to generate a structured episode outline with:
- Chapter titles and target word counts
- Key talking points per chapter
- Estimated duration per chapter
- Source attribution hints

Routing: DeepSeek V3.1 via OpenRouter (default for drafting).
Target: 65-minute episode = ~9,425 words at 145 wpm.
"""


def generate_outline(trip_config, cleaned_sources: list[dict], topic: str) -> dict:
    """
    Generate a structured outline for a 65-minute episode.
    Returns dict with chapters list, each having: title, target_words, key_points, sources.
    """
    pass
