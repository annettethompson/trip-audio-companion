"""
Companion Page Generator
Builds a phone-optimized HTML companion page for each audio episode.

Usage:
    from src.companion_page_generator import CompanionPageGenerator
    gen = CompanionPageGenerator()
    gen.build(script_path=Path("scripts/glenwood-springs.md"),
              output_dir=Path("web/episodes"))
"""
from __future__ import annotations

import re
import yaml
from pathlib import Path
from datetime import date
from typing import Any

try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> dict[str, list[dict]]:
    with open(path, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _index_by_name(items: list[dict], key: str = "common_name") -> dict[str, dict]:
    """Build a lookup dict keyed by lowercased name."""
    out: dict[str, dict] = {}
    for item in items:
        name = item.get(key, "").lower()
        out[name] = item
        # also index by scientific name
        sci = item.get("scientific_name", "").lower()
        if sci:
            out[sci] = item
    return out


# ---------------------------------------------------------------------------
# Card builders  (one function per card type)
# ---------------------------------------------------------------------------

def _plant_card(data: dict) -> dict:
    return {
        "type": "plant",
        "common_name": data.get("common_name", ""),
        "scientific_name": data.get("scientific_name", ""),
        "status": data.get("status", "caution").lower(),
        "key_property": data.get("key_property", ""),
        "edible_parts": data.get("edible_parts"),
        "poison_warning": data.get("poison_warning"),
        "identification": data.get("identification", []),
        "lookalikes": data.get("lookalikes", []),
        "photo_url": data.get("photo_url", ""),
        "photo_credit": data.get("photo_credit", ""),
    }


def _animal_card(data: dict) -> dict:
    return {
        "type": "animal",
        "common_name": data.get("common_name", ""),
        "scientific_name": data.get("scientific_name", ""),
        "habitat": data.get("habitat", ""),
        "elevation_range": data.get("elevation_range", ""),
        "active_time": data.get("active_time", ""),
        "interesting_fact": data.get("interesting_fact", ""),
        "where_to_spot": data.get("where_to_spot", ""),
        "photo_url": data.get("photo_url", ""),
        "photo_credit": data.get("photo_credit", ""),
    }


def _geology_card(name: str, age: str, rock_type: str,
                  description: str, significance: str,
                  photo_url: str = "", photo_credit: str = "") -> dict:
    return {
        "type": "geology",
        "name": name,
        "age": age,
        "rock_type": rock_type,
        "description": description,
        "significance": significance,
        "photo_url": photo_url,
        "photo_credit": photo_credit,
    }


def _history_card(title: str, era: str, story: str,
                  photo_url: str = "", photo_credit: str = "") -> dict:
    return {
        "type": "history",
        "title": title,
        "era": era,
        "story": story,
        "photo_url": photo_url,
        "photo_credit": photo_credit,
    }


def _hotspring_card(name: str, temperature: str, minerals: str,
                    geology: str, history: str,
                    photo_url: str = "", photo_credit: str = "") -> dict:
    return {
        "type": "hotspring",
        "name": name,
        "temperature": temperature,
        "minerals": minerals,
        "geology": geology,
        "history": history,
        "photo_url": photo_url,
        "photo_credit": photo_credit,
    }


def _divider(chapter_num: int, title: str, emoji: str = "🎧") -> dict:
    return {
        "type": "divider",
        "text": f"Chapter {chapter_num}: {title}",
        "emoji": emoji,
    }


def _info_card(title: str, content: str, bullets: list[str] | None = None) -> dict:
    return {
        "type": "info",
        "title": title,
        "content": content,
        "bullets": bullets or [],
    }


def _cta_card(title: str, items: list[dict]) -> dict:
    return {
        "type": "cta",
        "title": title,
        "items": items,
    }


# ---------------------------------------------------------------------------
# Script parser  (Markdown-based episode scripts)
# ---------------------------------------------------------------------------

def _parse_script(script_path: Path) -> dict:
    """
    Parse a Markdown episode script into a list of card specs.

    Expected frontmatter format (YAML between --- delimiters):
        title: "Episode Title"
        date: "2026-05-20"
        slug: "glenwood-springs"

    Section headers drive card type detection:
        ## Chapter N: Title
        ### Plant: Common Name
        ### Animal: Common Name
        ### Geology: Formation Name
        ### History: Event Title (Era: ...)
        ### Hot Spring: Name
        ### Info: Title
        ### CTA: Title
    """
    text = script_path.read_text(encoding="utf-8")

    # Extract YAML frontmatter
    meta: dict = {}
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            meta = yaml.safe_load(text[3:end]) or {}
            text = text[end + 3:].strip()

    return {
        "meta": meta,
        "raw_text": text,
    }


# ---------------------------------------------------------------------------
# Main generator class
# ---------------------------------------------------------------------------

class CompanionPageGenerator:
    """
    Generates phone-optimized HTML companion pages for audio episodes.

    Parameters
    ----------
    template_dir : Path
        Directory containing companion.html (Jinja2 template),
        plant_data.yaml, and animal_data.yaml.
    """

    def __init__(self, template_dir: Path | None = None):
        if template_dir is None:
            template_dir = Path(__file__).parent.parent / "web" / "template"
        self.template_dir = template_dir
        self._plant_index: dict[str, dict] | None = None
        self._animal_index: dict[str, dict] | None = None

        if not JINJA2_AVAILABLE:
            raise ImportError(
                "Jinja2 is required for companion page generation. "
                "Install with: pip install jinja2"
            )

        self._jinja_env = Environment(
            loader=FileSystemLoader(str(self.template_dir)),
            autoescape=select_autoescape(["html"]),
        )

    # ---- data loading ---------------------------------------------------

    @property
    def plant_index(self) -> dict[str, dict]:
        if self._plant_index is None:
            plant_file = self.template_dir / "plant_data.yaml"
            data = _load_yaml(plant_file)
            self._plant_index = _index_by_name(data.get("plants", []))
        return self._plant_index

    @property
    def animal_index(self) -> dict[str, dict]:
        if self._animal_index is None:
            animal_file = self.template_dir / "animal_data.yaml"
            data = _load_yaml(animal_file)
            self._animal_index = _index_by_name(data.get("animals", []))
        return self._animal_index

    # ---- lookup helpers -------------------------------------------------

    def lookup_plant(self, name: str) -> dict | None:
        key = name.lower().strip()
        return self.plant_index.get(key)

    def lookup_animal(self, name: str) -> dict | None:
        key = name.lower().strip()
        return self.animal_index.get(key)

    # ---- build from a pre-assembled card list ---------------------------

    def build_from_cards(
        self,
        episode_title: str,
        cards: list[dict],
        output_path: Path,
        episode_date: str | None = None,
    ) -> Path:
        """
        Render the Jinja2 template with the given cards list and write HTML.

        Parameters
        ----------
        episode_title : str
            Title shown in the page header.
        cards : list[dict]
            List of card dicts (use the _plant_card, _animal_card, etc. helpers).
        output_path : Path
            Full path of the output HTML file (created if not exists).
        episode_date : str, optional
            Human-readable date string shown in the header.

        Returns
        -------
        Path
            The output path where the HTML was written.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        template = self._jinja_env.get_template("companion.html")
        html = template.render(
            episode_title=episode_title,
            cards=cards,
            episode_date=episode_date or date.today().strftime("%B %d, %Y"),
        )
        output_path.write_text(html, encoding="utf-8")
        return output_path

    # ---- build from a Markdown script file ------------------------------

    def build(
        self,
        episode_script: Path,
        output_dir: Path = Path("web/episodes"),
    ) -> Path:
        """
        Build a companion page from a Markdown episode script.

        The script file must have YAML frontmatter with at minimum:
            title: "..."
            slug: "..."

        Card definitions in the script body follow the format:
            ### Plant: Willow
            ### Animal: Osprey
            etc.

        Returns the path to the generated HTML file.
        """
        parsed = _parse_script(episode_script)
        meta = parsed["meta"]
        raw = parsed["raw_text"]

        episode_title = meta.get("title", episode_script.stem.replace("-", " ").title())
        slug = meta.get("slug", episode_script.stem)
        episode_date = meta.get("date", date.today().strftime("%B %d, %Y"))

        cards = self._parse_raw_to_cards(raw)

        output_path = output_dir / slug / "index.html"
        return self.build_from_cards(
            episode_title=episode_title,
            cards=cards,
            output_path=output_path,
            episode_date=str(episode_date),
        )

    # ---- private: parse raw markdown into card list ---------------------

    def _parse_raw_to_cards(self, raw: str) -> list[dict]:
        """
        Convert raw markdown body into a list of card dicts.
        Handles chapter dividers and typed card headers.
        """
        cards: list[dict] = []
        chapter_num = 0

        for line in raw.splitlines():
            line = line.strip()

            # Chapter divider: ## Chapter N: Title
            m = re.match(r"^##\s+Chapter\s+(\d+):\s+(.+)$", line, re.IGNORECASE)
            if m:
                chapter_num = int(m.group(1))
                cards.append(_divider(chapter_num, m.group(2).strip()))
                continue

            # Typed card: ### Type: Name
            m2 = re.match(r"^###\s+(\w[\w\s]*):\s+(.+)$", line)
            if m2:
                card_type = m2.group(1).strip().lower()
                name = m2.group(2).strip()
                card = self._resolve_card(card_type, name)
                if card:
                    cards.append(card)
                continue

        return cards

    def _resolve_card(self, card_type: str, name: str) -> dict | None:
        """Look up data for a card type+name and return a card dict."""
        if card_type == "plant":
            data = self.lookup_plant(name)
            if data:
                return _plant_card(data)
        elif card_type == "animal":
            data = self.lookup_animal(name)
            if data:
                return _animal_card(data)
        # Inline geology/history/hotspring/info cards require explicit dict data;
        # they are typically assembled directly via build_from_cards()
        return None


# ---------------------------------------------------------------------------
# Convenience exports (for use in main.py and tests)
# ---------------------------------------------------------------------------

__all__ = [
    "CompanionPageGenerator",
    "_plant_card",
    "_animal_card",
    "_geology_card",
    "_history_card",
    "_hotspring_card",
    "_divider",
    "_info_card",
    "_cta_card",
]
