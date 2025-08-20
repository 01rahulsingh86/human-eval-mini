import pandas as pd
import numpy as np
from scipy.stats import spearmanr, ttest_rel

def compute_mos(ratings: pd.DataFrame) -> pd.DataFrame:
    mos = ratings.groupby(["model", "metric"])["score"].mean().reset_index()
    mos = mos.rename(columns={"score": "mos"})
    return mos

def compute_irr(ratings: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric, dfm in ratings.groupby("metric"):
        pivot = dfm.pivot_table(index=["item_id","model"], columns="rater", values="score")
        raters = list(pivot.columns)
        rhos = []
        for i in range(len(raters)):
            for j in range(i+1, len(raters)):
                a = pivot[raters[i]].values
                b = pivot[raters[j]].values
                m = ~np.isnan(a) & ~np.isnan(b)
                if m.sum() > 2:
                    rho, _ = spearmanr(a[m], b[m])
                    if np.isfinite(rho):
                        rhos.append(rho)
        irr = float(np.mean(rhos)) if rhos else np.nan
        rows.append({"metric": metric, "irr_spearman": irr, "pairs": len(rhos)})
    return pd.DataFrame(rows)

def paired_ttest(ratings: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for metric, dfm in ratings.groupby("metric"):
        per_item = dfm.groupby(["item_id","model"])["score"].mean().unstack("model")
        if {"A","B"}.issubset(per_item.columns):
            a = per_item["A"].values
            b = per_item["B"].values
            t, p = ttest_rel(a, b, nan_policy="omit")
            rows.append({"metric": metric, "t_stat": float(t), "p_value": float(p)})
    return pd.DataFrame(rows)

def winner_table(mos: pd.DataFrame) -> pd.DataFrame:
    winners = mos.loc[mos.groupby("metric")["mos"].idxmax()].copy()
    winners = winners.rename(columns={"model":"winner"})
    return winners[["metric","winner","mos"]]
