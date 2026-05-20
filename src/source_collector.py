"""
Source collector for Trip Audio Companion.

Fetches web pages from approved tier-1/2/3 sources (see config/sources.yaml).
Uses trafilatura for clean text extraction.
Respects the no-Wikipedia rule — any wikipedia.org/wikimedia.org URL is rejected at intake.
Stores raw HTML and extracted text to data/raw_sources/.
"""


def collect_sources(urls: list[str], output_dir) -> list[dict]:
    """
    Fetch and extract text from a list of approved URLs.
    Returns list of dicts with keys: url, title, text, date_accessed, tier.
    """
    pass
