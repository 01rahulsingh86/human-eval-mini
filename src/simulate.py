from dataclasses import dataclass
import numpy as np
import pandas as pd
from .config import RUBRIC, LIKERT_MIN, LIKERT_MAX, RATER_NOISE_STD, BIAS_STD, NOMINAL_ADVANTAGE

class SimData:
    def __init__(self, items: int, raters: int, seed: int = 123):
        self.items = items
        self.raters = raters
        self.seed = seed

def _clip_likert(x):
    import numpy as np
    return int(np.clip(round(x), LIKERT_MIN, LIKERT_MAX))

def generate_model_latents(sd: SimData):
    rng = np.random.default_rng(sd.seed)
    rows = []
    for item_id in range(sd.items):
        for model in ["A", "B"]:
            for metric in RUBRIC:
                base = rng.normal(3.2, 0.6)  # base quality around neutral
                lift = NOMINAL_ADVANTAGE.get(metric, 0.0) if model == "B" else 0.0
                latent = base + lift
                rows.append({"item_id": item_id, "model": model, "metric": metric, "latent": latent})
    import pandas as pd
    return pd.DataFrame(rows)

def simulate_scores(sd: SimData, latents: pd.DataFrame):
    rng = np.random.default_rng(sd.seed + 99)
    # per-rater bias (e.g., some strict, some generous)
    bias = rng.normal(0.0, BIAS_STD, size=sd.raters)
    scores = []
    for _, row in latents.iterrows():
        for rater in range(sd.raters):
            noise = rng.normal(0.0, RATER_NOISE_STD)
            val = row["latent"] + bias[rater] + noise
            scores.append({
                "item_id": row["item_id"],
                "model": row["model"],
                "rater": rater,
                "metric": row["metric"],
                "score": _clip_likert(val)
            })
    import pandas as pd
    return pd.DataFrame(scores)
