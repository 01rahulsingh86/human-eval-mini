# Human Eval Mini 🧪🤖

A tiny demo repository that shows how to **evaluate model outputs with human ratings at scale**.  
It builds a mini evaluation engine, runs mock raters, and generates metrics + reports.

---

## 🚀 Features
- Generates model outputs for evaluation
- Simulates human raters to assign scores
- Aggregates ratings into metrics (MOS, IRR, T-tests, winners)
- Produces artifacts:
  - `outputs.csv`, `ratings.csv`
  - `metrics_mos.csv`, `metrics_irr.csv`, `metrics_ttests.csv`, `metrics_winners.csv`
  - `summary.md` → pretty Markdown table view of results

---

## 📦 Setup

Clone the repo:
```bash
git clone https://github.com/<USERNAME>/human-eval-mini.git
cd human-eval-mini

Create a virtual environment:
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run the Demo

Run with 40 items, 5 raters, and a fixed seed:
python -m scripts.run_demo --items 40 --raters 5 --seed 42


Open summary.md for a clean results table. Example:

metric	modelA	modelB	winner
MOS	4.23	3.87	modelA
🛠️ Tech Stack

Python 3.9+

pandas for metrics aggregation

tabulate for pretty Markdown output

🌟 Why?

This repo is meant as a learning tool:

How to simulate human evaluation in ML pipelines

How to generate reproducible metrics

How to package results for analysis


License

MIT License © 2025

