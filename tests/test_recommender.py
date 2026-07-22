import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from src.recommender import Song, UserProfile, Recommender, POINT_STRATEGIES

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # The pop, happy, high-energy song should score highest.
    assert results[0].title == "Test Pop Track"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
    assert "genre match" in explanation
    assert "mood match" in explanation
    assert "similar energy" in explanation
    assert "acousticness preference match" in explanation


def test_recommend_handles_edge_case_k_values():
    """Test that recommend returns an empty list for k=0 and all songs for a large k."""
    user = UserProfile("pop", "happy", 0.8, False)
    rec = make_small_recommender()

    # Test with k=0
    zero_results = rec.recommend(user, k=0)
    assert len(zero_results) == 0

    # Test with k > number of songs
    large_k_results = rec.recommend(user, k=10)
    assert len(large_k_results) == 2


def test_recommend_ranking_changes_with_strategy():
    """Test that changing the weighting strategy changes the recommendation order."""
    # A user who likes pop but a chill mood, creating a conflict between the two test songs.
    user = UserProfile(
        favorite_genre="pop", favorite_mood="chill", target_energy=0.6, likes_acoustic=True
    )

    # With 'intent_first', the genre match should win.
    rec_intent = Recommender(make_small_recommender().songs, strategy=POINT_STRATEGIES["intent_first"])
    results_intent = rec_intent.recommend(user, k=2)
    assert results_intent[0].title == "Test Pop Track"

    # With 'balanced' weights, the mood match (and better acousticness) should win.
    rec_balanced = Recommender(make_small_recommender().songs, strategy=POINT_STRATEGIES["balanced"])
    results_balanced = rec_balanced.recommend(user, k=2)
    assert results_balanced[0].title == "Chill Lofi Loop"


def test_explanation_for_partial_match():
    """Test that the explanation only includes reasons that apply."""
    user = UserProfile("rock", "sad", 0.5, True) # This profile matches nothing perfectly
    rec = make_small_recommender()
    song = rec.songs[0] # "Test Pop Track"

    explanation = rec.explain_recommendation(user, song)
    assert "genre match" not in explanation
    assert "mood match" not in explanation
