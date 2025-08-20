RUBRIC = ["relevance", "novelty", "diversity"]  # 1–5 Likert
LIKERT_MIN, LIKERT_MAX = 1, 5

# Rater behavior (noise) – tweak these
RATER_NOISE_STD = 0.7        # higher = less agreement
BIAS_STD = 0.15              # per-rater bias
NOMINAL_ADVANTAGE = {"relevance": 0.4, "novelty": 0.6, "diversity": 0.3}  # Model B lift vs A (latent)
