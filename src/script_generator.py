"""
Script generator for Trip Audio Companion.

Takes the structured outline and expands each chapter into full narration text.
- Warm, intelligent, vivid, story-driven prose (per episode_style in trip.yaml)
- No Wikipedia citations
- Every factual claim tagged with source URL
- Targets 145 wpm read rate for TTS
- duration_guard.check_pre_tts() is called after generation; if short, expands

Routing:
- Chapter drafting: DeepSeek V3.1 via OpenRouter
- Final synthesis / quality pass: claude-opus-4-7 via Anthropic direct
  (because this goes to real human ears on a road trip)
"""


def generate_script(outline: dict, cleaned_sources: list[dict], trip_config) -> str:
    """
    Expand an outline into a full narration script.
    Returns complete script text with inline citation markers.
    """
    pass
