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
```

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

---

## Sample Recommendation Output

The CLI produces different rankings for each named user preference profile:

### High-Energy Pop

```text
High-Energy Pop — Top recommendations:

Sunrise City - Score: 0.99
Because: genre match (+2); mood match (+1); similar energy; acousticness preference match

Gym Hero - Score: 0.76
Because: genre match (+2); similar energy; acousticness preference match

Rooftop Lights - Score: 0.54
Because: mood match (+1); similar energy; acousticness preference match

Pocket Full of Sunshine - Score: 0.39
Because: similar energy; acousticness preference match

Concrete Poetry - Score: 0.38
Because: similar energy; acousticness preference match
```

### Chill Lofi

```text
Chill Lofi — Top recommendations:

Midnight Coding - Score: 0.99
Because: genre match (+2); mood match (+1); similar energy; acousticness preference match

Library Rain - Score: 0.97
Because: genre match (+2); mood match (+1); similar energy; acousticness preference match

Focus Flow - Score: 0.79
Because: genre match (+2); similar energy; acousticness preference match

Spacewalk Thoughts - Score: 0.54
Because: mood match (+1); similar energy; acousticness preference match

Sunday Vinyl - Score: 0.38
Because: similar energy; acousticness preference match
```

### Deep Intense Rock

```text
Deep Intense Rock — Top recommendations:

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

I compared the `intent_first`, `balanced`, and `discovery` weighting strategies. The default `intent_first` strategy consistently favored exact genre matches because genre is worth twice as much as mood. The `balanced` strategy gave mood matches more influence, while the `discovery` strategy allowed songs with similar energy to compete more strongly even when their genre did not match.

I also tested High-Energy Pop, Chill Lofi, and Deep Intense Rock profiles against the full 25-song catalog. The expected songs ranked first for each profile, but the Deep Intense Rock results showed that a non-rock song could still rank highly when its energy and acousticness were close to the target. This confirmed that the recommender supports discovery, but it also demonstrated why the weights and explanations need to be reviewed carefully.

---

## Limitations and Bias

During the profile experiments, the `Deep Intense Rock` recommendations showed that the system can over-prioritize numeric similarity: non-rock songs such as `Gym Hero` still ranked highly because their energy and acousticness were close to the target. The default recipe also gives genre twice the weight of mood, so a great mood match from another genre can be pushed below a weaker genre match. Because the catalog is small and hand-curated, the results may also reflect uneven genre representation rather than broad musical quality. The recommender does not understand lyrics, cultural context, or subjective meaning, so its labels and scores can oversimplify a listener's preferences.

---

## Biggest Learning Moment

My biggest learning moment was seeing how a short weighted formula can turn a table of song attributes into results that feel like personalized recommendations. The system does not understand music or listen like a person, but comparing genre, mood, energy, and acousticness creates rankings that match the three example profiles often enough to feel meaningful. At the same time, the Deep Intense Rock experiment showed that a recommendation can feel plausible while still missing an important preference, such as genre.

AI tools helped me explore the codebase, identify placeholder logic, suggest a clear scoring strategy, generate documentation drafts, and catch missing docstrings and validation issues. I still needed to double-check the suggestions by reading the implementation, comparing the scoring formula with the actual output, checking the catalog counts, and running the CLI with multiple profiles. This was important because an AI-generated recommendation can sound reasonable while overlooking details such as unused features, score normalization, import behavior, or bias caused by the weights.

If I extended this project, I would add more songs and user feedback, support multiple genres and moods, and use valence, danceability, and tempo with explicit user targets. I would also test diversity-aware ranking so the top results do not overrepresent one genre or artist, and compare the different weighting strategies using real ratings instead of intuition alone.

For additional project reflection, see the completed [model card](model_card.md).
