# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## User Profile Critique

**Prompt used:**

> Critique this proposed content-based music recommender profile: `genre=rock`, `mood=intense`, `energy=0.88`, `acousticness=0.15`, `valence=0.50`, and `danceability=0.65`. Will these preferences allow the system to differentiate between intense rock and chill lofi, or is the profile too narrow? Consider which features are most informative, whether any preferences overlap, and how the profile could support discovery of related songs.

**Critique:**

The profile should clearly distinguish intense rock from chill lofi. `genre` separates rock from lofi, `mood` separates intense from chill, and the high `energy` target reinforces the difference: `Storm Runner` has energy `0.91`, while the lofi songs range from `0.35` to `0.42`. The low acousticness target also supports the distinction because the intense rock track has acousticness `0.10`, while the lofi tracks have acousticness between `0.71` and `0.86`.

The profile is specific, but it is not unusably narrow because the numeric preferences allow related songs to receive partial credit. `Gym Hero`, `Night Drive Loop`, and `Neon Heartbeat` can still be discovered because they are energetic and relatively non-acoustic, even though they are not rock. However, `genre` and `mood` should be treated as weighted preferences rather than hard filters; otherwise the recommender may return too few results from a small catalog. `valence` and `danceability` are useful secondary features, but they should have lower weights because the profile does not express them as strongly as genre, mood, energy, and acousticness.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
