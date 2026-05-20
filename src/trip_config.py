from pathlib import Path
import yaml
from pydantic import BaseModel, Field
from typing import Optional


class Traveler(BaseModel):
    name: str
    background: Optional[str] = None
    voice_level: Optional[str] = None


class HotSpring(BaseModel):
    name: str
    location: str
    notes: Optional[str] = None


class TripConfig(BaseModel):
    trip_name: str
    trip_slug: str
    start_date: str
    end_date: str
    travelers: list[Traveler]
    hot_springs: list[HotSpring] = Field(default_factory=list)
    topics_of_interest: list[str] = Field(default_factory=list)
    avoid_topics: list[str] = Field(default_factory=list)
    episode_style: str = "warm, intelligent, vivid, story-driven"
    target_minutes: int = 65
    minimum_minutes: int = 60
    words_per_minute: int = 145

    @property
    def target_word_count(self) -> int:
        """Target word count derived from target_minutes and words_per_minute."""
        return self.target_minutes * self.words_per_minute

    @property
    def minimum_word_count(self) -> int:
        """Minimum word count derived from minimum_minutes and words_per_minute."""
        return self.minimum_minutes * self.words_per_minute


def load_trip_config(path: Path) -> TripConfig:
    if not path.exists():
        raise FileNotFoundError(f"Trip config not found: {path}")
    try:
        with open(path) as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in {path}: {e}") from e
    try:
        return TripConfig(**data)
    except Exception as e:
        raise ValueError(f"Trip config validation failed in {path}: {e}") from e
