import argparse, os
from datetime import datetime
import pandas as pd
from src.simulate import SimData, generate_model_latents, simulate_scores
from src.aggregate import compute_mos, compute_irr, paired_ttest, winner_table
from src.utils import save_csv, ensure_dir

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", type=int, default=40, help="Number of items/users")
    ap.add_argument("--raters", type=int, default=5, help="Number of human raters")
    ap.add_argument("--seed", type=int, default=42, help="Random seed")
    ap.add_argument("--outdir", default="artifacts", help="Output directory")
    args = ap.parse_args()

    ensure_dir(args.outdir)

    sd = SimData(items=args.items, raters=args.raters, seed=args.seed)
    latents = generate_model_latents(sd)
    ratings = simulate_scores(sd, latents)

    outputs = latents.pivot_table(index=["item_id","model"], columns="metric", values="latent").reset_index()
    outputs.to_csv(os.path.join(args.outdir, "outputs.csv"), index=False)

    save_csv(ratings, os.path.join(args.outdir, "ratings.csv"))

    mos = compute_mos(ratings)
    irr = compute_irr(ratings)
    ttests = paired_ttest(ratings)
    winners = winner_table(mos)

    save_csv(mos, os.path.join(args.outdir, "metrics_mos.csv"))
    save_csv(irr, os.path.join(args.outdir, "metrics_irr.csv"))
    save_csv(ttests, os.path.join(args.outdir, "metrics_ttests.csv"))
    save_csv(winners, os.path.join(args.outdir, "metrics_winners.csv"))

    ts = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    lines = [
        f"# Human Evaluation Summary",
        f"_Generated: {ts}_",
        "",
        "## Mean Opinion Scores (MOS) by Model",
        mos.pivot(index="metric", columns="model", values="mos").round(3).to_markdown(),
        "",
        "## Inter-Rater Reliability (avg pairwise Spearman ρ)",
        irr.round(3).to_markdown(index=False),
        "",
        "## Paired t-test (per metric, item-level means A vs B)",
        ttests.round(5).to_markdown(index=False),
        "",
        "## Winners (higher MOS)",
        winners.round(3).to_markdown(index=False),
        "",
        "> Note: This is simulated data with Model B given a small latent advantage in config."
    ]
    with open(os.path.join(args.outdir, "summary.md"), "w") as f:
        f.write("\n".join(lines))

    print(f"Artifacts written to: {args.outdir}")
    print(" - outputs.csv, ratings.csv")
    print(" - metrics_mos.csv, metrics_irr.csv, metrics_ttests.csv, metrics_winners.csv")
    print(" - summary.md (pretty table view)")

if __name__ == "__main__":
    main()
