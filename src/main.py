"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile used by the content-based recommender. The categorical
    # preferences separate broad musical styles, while the numeric values let
    # the scorer find songs with a similar sound within or across genres.
    user_prefs = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.88,
        "acousticness": 0.15,
        "valence": 0.50,
        "danceability": 0.65,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
