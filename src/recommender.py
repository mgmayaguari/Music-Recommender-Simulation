"""Content-based music recommendation models and scoring utilities."""

import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

@dataclass(frozen=True)
class WeightingStrategy:
    """Point weights for recommendation features.

    Scores are normalized by the total weight, so they remain in the range
    0..1. The default gives a genre match twice the value of a mood match.
    """

    genre: float = 2.0
    mood: float = 1.0
    energy: float = 1.0
    acousticness: float = 1.0

    def __post_init__(self) -> None:
        """Validate that the strategy contains usable non-negative weights."""
        weights = (self.genre, self.mood, self.energy, self.acousticness)
        if any(weight < 0 for weight in weights):
            raise ValueError("Strategy weights must be non-negative")
        if sum(weights) == 0:
            raise ValueError("At least one strategy weight must be positive")


# Named recipes make experimentation possible without changing scoring logic.
POINT_STRATEGIES = {
    "intent_first": WeightingStrategy(genre=2.0, mood=1.0, energy=1.0, acousticness=1.0),
    "balanced": WeightingStrategy(genre=1.5, mood=1.5, energy=1.0, acousticness=1.0),
    "discovery": WeightingStrategy(genre=1.0, mood=1.0, energy=1.5, acousticness=0.5),
}


class Recommender:
    """Rank songs and explain recommendations for a typed user profile."""

    def __init__(
        self,
        songs: List[Song],
        strategy: WeightingStrategy = POINT_STRATEGIES["intent_first"],
    ):
        """Create a recommender with a configurable scoring strategy."""
        self.songs = songs
        self.strategy = strategy

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top ``k`` songs ranked by their recommendation scores."""
        ranked = sorted(
            self.songs,
            key=lambda song: _score_song_values(user, song, self.strategy)[0],
            reverse=True,
        )
        return ranked[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain which user preferences contributed to a song's score."""
        _, reasons = _score_song_values(user, song, self.strategy)
        return "; ".join(reasons) or "This song received partial similarity points."


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from the project CSV file with numeric fields converted."""
    with open(csv_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        songs = []
        numeric_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
        for row in reader:
            songs.append({
                **row,
                "id": int(row["id"]),
                **{field: float(row[field]) for field in numeric_fields},
            })
        return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
    strategy: WeightingStrategy = POINT_STRATEGIES["intent_first"],
) -> Tuple[float, List[str]]:
    """Return a normalized score and reasons using the selected point recipe."""
    components = {
        "genre": float(song.get("genre") == user_prefs.get("genre")),
        "mood": float(song.get("mood") == user_prefs.get("mood")),
        "energy": _similarity(song.get("energy"), user_prefs.get("energy")),
        "acousticness": _acoustic_similarity(song, user_prefs),
    }
    weighted_total = sum(getattr(strategy, name) * value for name, value in components.items())
    total_weight = sum(getattr(strategy, name) for name in components)

    reasons = []
    if components["genre"]:
        reasons.append(f"genre match (+{strategy.genre:g})")
    if components["mood"]:
        reasons.append(f"mood match (+{strategy.mood:g})")
    if components["energy"] >= 0.8:
        reasons.append("similar energy")
    if components["acousticness"] >= 0.8:
        reasons.append("acousticness preference match")
    return weighted_total / total_weight, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: WeightingStrategy = POINT_STRATEGIES["intent_first"],
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest-first, and return the top ``k``."""
    ranked = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, strategy)
        explanation = "; ".join(reasons) or "This song received partial similarity points."
        ranked.append((song, score, explanation))
    ranked.sort(key=lambda result: result[1], reverse=True)
    return ranked[:k]


def _similarity(value: Optional[float], target: Optional[float]) -> float:
    """Return a clamped similarity score for two numeric values."""
    if value is None or target is None:
        return 0.0
    return max(0.0, min(1.0, 1.0 - abs(float(value) - float(target))))


def _acoustic_similarity(song: Dict, user_prefs: Dict) -> float:
    """Return how closely a song's acousticness matches the user's preference."""
    target = user_prefs.get("acousticness")
    if target is None and "likes_acoustic" in user_prefs:
        target = 1.0 if user_prefs["likes_acoustic"] else 0.0
    return _similarity(song.get("acousticness"), target)


def _score_song_values(
    user: UserProfile, song: Song, strategy: WeightingStrategy
) -> Tuple[float, List[str]]:
    """Score a typed song by adapting its profile to the functional scorer."""
    return score_song(
        {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        },
        song.__dict__,
        strategy,
    )
