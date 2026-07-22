# 🎵 Music Recommender Simulation

## Project Summary

This project implements a small content-based music recommender. It compares a user's taste profile with song metadata and audio features, assigns each song a score, and returns the highest-scoring songs with explanations.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

---

## How The System Works

The recommender uses **content-based filtering**: it recommends songs whose attributes are similar to the user's stated preferences. It does not use listening behavior from other users.

### Data flow

The recommendation process follows this path:

**Input (User Preferences) → Process (Score Every Song) → Output (Top K Ranking)**

1. **Input:** The system receives the user's preferred genre and mood, target energy, and acoustic preference.
2. **Process:** It loads the song catalog from `data/songs.csv` and evaluates every individual song. Each song is compared with the user profile, assigned a weighted score, and given an explanation of its strongest matches.
3. **Output:** The system sorts all songs from highest to lowest score and returns only the top `k` recommendations.

### Song features

Each `Song` includes:

- `genre` and `mood` for categorical preference matching
- `energy` for similarity to the user's target energy level
- `acousticness` for the user's acoustic preference
- `valence`, `danceability`, and `tempo_bpm` as additional audio descriptors
- `title`, `artist`, and `id` for identification and display, not for the similarity score

### User profile

Each `UserProfile` stores:

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `likes_acoustic`

### Finalized Algorithm Recipe

Every song receives a score from 0 to 1 using a weighted point system. The default `intent_first` strategy is:

- **+2.0 points** for an exact genre match
- **+1.0 point** for an exact mood match
- **+1.0 point** for energy similarity
- **+1.0 point** for acousticness similarity

The numeric similarities are calculated as:

$$
E = \max(0, 1 - |song.energy - user.target\_energy|)
$$

$$
A = \max(0, 1 - |song.acousticness - user.acousticness|)
$$

Genre and mood matches are soft preferences rather than hard filters, so a song can still be recommended when it matches the user's sound in other ways. The weighted total is divided by the total available weight, keeping the final score in the range $[0, 1]$.

The implementation also supports two alternative recipes for experimentation:

- **`balanced`:** genre and mood are both worth 1.5 points.
- **`discovery`:** energy is worth 1.5 points, while acousticness is worth 0.5 points.

The recommender calculates a score for every song, sorts songs from highest to lowest score, and returns the top `k` results. Explanations identify contributing features such as genre match, mood match, similar energy, or acousticness match. Valence, danceability, and tempo remain available as future signals but are not part of the finalized recipe because the current user profile does not provide corresponding targets.

### Potential biases and risks

This system might over-prioritize genre, causing it to ignore excellent songs that match the user's mood or energy but come from a different genre. Exact genre and mood labels can also oversimplify music and reflect subjective or inconsistent metadata. Because the catalog is small and hand-curated, recommendations may favor genres or moods that are more heavily represented while offering less diversity. The discovery strategy can reduce this effect, but it cannot eliminate catalog or labeling bias.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Top recommendations:

Storm Runner - Score: 0.98
Because: genre match (+2); mood match (+1); similar energy; acousticness preference match

Gym Hero - Score: 0.57
Because: mood match (+1); similar energy; acousticness preference match

Sunrise City - Score: 0.38
Because: similar energy; acousticness preference match

Paper Planes - Score: 0.38
Because: similar energy; acousticness preference match

Pocket Full of Sunshine - Score: 0.38
Because: similar energy; acousticness preference match
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



