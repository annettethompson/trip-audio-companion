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
    target_words: int = 10000
    minimum_words: int = 9000

    @property
    def target_word_count(self) -> int:
        return self.target_minutes * self.words_per_minute


def load_trip_config(path: Path) -> TripConfig:
    with open(path) as f:
        data = yaml.safe_load(f)
    return TripConfig(**data)
