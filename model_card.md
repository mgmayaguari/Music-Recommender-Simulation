# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder: CLI-First Content Recommender**

---

## 2. Intended Use

VibeFinder demonstrates how a content-based music recommender turns a user's stated preferences into a ranked list of songs. It recommends songs from a small local catalog using genre, mood, energy, and acousticness. It assumes that one favorite genre, one favorite mood, a target energy level, and an acoustic preference are reasonable summaries of the user's taste. This is intended for classroom exploration and experimentation, not production use or high-stakes decisions about a listener's identity or taste.



---

## 3. How the Model Works

The model compares each song with the user's profile. An exact genre match contributes **2 points**, while an exact mood match contributes **1 point**. Energy and acousticness contribute up to **1 point each**, based on how close the song is to the user's target values. The total is normalized to a score between 0 and 1, every song is scored, and the highest-scoring songs are returned as the top recommendations.

Genre and mood are soft preferences rather than filters, so songs from other genres can still be discovered when their audio characteristics are similar. The implementation adds CSV loading, configurable weighting strategies, ranking, and explanations of the features that contributed to each recommendation. The default recipe prioritizes genre intent, while balanced and discovery recipes support comparison experiments.



---

## 4. Data

The model uses the 25-song catalog in `data/songs.csv`. Each song includes an ID, title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. The catalog contains 22 genres: most occur once, while lofi occurs three times and pop occurs twice. It contains 21 moods: most occur once, while chill occurs three times and happy and intense occur twice each.

The data is a small, hand-curated simulation rather than a representative sample of real-world music. It does not include listening history, user ratings, lyrics, language, release date, popularity, cultural context, or collaborative behavior. Valence, danceability, and tempo are stored as additional descriptors, but the finalized scoring recipe does not use them because current profiles do not define matching targets.



---

## 5. Strengths

The model works well when a user has clear preferences represented in the catalog. High-Energy Pop ranks a happy pop song first, Chill Lofi ranks chill lofi songs first, and Deep Intense Rock ranks the intense rock song first. Energy similarity helps distinguish songs within or across genres, while soft categorical matching allows some discovery instead of eliminating every song that misses one label.

The explanations are simple and understandable: they identify genre, mood, energy, and acousticness matches. The CLI-first design also makes it easy to compare several profiles and observe how changing preferences changes the ranking.



---

## 6. Limitations and Bias

The strongest weakness discovered during profile experiments is that numeric features can make a non-matching-genre song rank highly. For the Deep Intense Rock profile, Gym Hero appears near the top because its energy and acousticness are similar, even though it is pop rather than rock. The default recipe gives genre twice the weight of mood, which may push down a song with an excellent mood match from another genre. The small catalog is unevenly represented, so genres with more entries have more opportunities to appear.

The model does not understand lyrics, language, cultural context, artist identity, or the personal meaning of a song. Genre and mood labels can be subjective, and one favorite genre and mood cannot represent complex or changing taste. The system may therefore overfit to the provided labels and audio values while missing songs a real listener would consider a good match.



---

## 7. Evaluation

The recommender was evaluated with three named profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock. For each profile, the CLI scored the full catalog, sorted the results, and displayed the top five songs with explanations. I checked whether the highest-ranked songs matched each profile's genre, mood, and target energy, and whether scores stayed in the expected 0-to-1 range.

The results matched the main expectations: Sunrise City ranked first for High-Energy Pop, Midnight Coding ranked first for Chill Lofi, and Storm Runner ranked first for Deep Intense Rock. I also ran the starter object-oriented tests and a direct CLI smoke test. The most informative surprise was that a different-genre song could rank highly when its energy and acousticness were close to the target.



---

## 8. Future Work

 - Add user targets for valence, danceability, and tempo.
 - Add more songs and measure genre and mood coverage.
 - Support multiple favorite genres, moods, and energy ranges.
 - Add diversity rules so results do not overrepresent one genre, artist, or mood.
 - Show component scores and weighted contributions in explanations.
 - Compare recipes with user feedback or ratings.



---

## 9. Personal Reflection

This project showed me that a recommender is not simply finding songs that look similar; it applies assumptions about which similarities matter most. Changing the genre and mood weights can change the ranking even when the catalog and profile stay the same. I learned that a transparent scoring rule is easy to inspect, but it can still produce biased results because of the catalog and labels it receives. This made the tradeoff between precise recommendations and useful discovery more visible than I expected.


