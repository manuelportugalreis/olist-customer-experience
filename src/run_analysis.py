"""Run every SQL query, save the results and draw the charts used in the README and memo."""
import sqlite3
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from build_database import DB, build

ROOT = Path(__file__).resolve().parents[1]
SQL = ROOT / "sql"
RESULTS = ROOT / "results"
ASSETS = ROOT / "assets"

BLUE, GREY, RED = "#2a5bd7", "#9aa0a6", "#d93025"


def run_queries(con: sqlite3.Connection) -> dict[str, pd.DataFrame]:
    con.executescript((SQL / "00_delivered_orders.sql").read_text())
    results = {}
    for path in sorted(SQL.glob("0[1-9]_*.sql")):
        df = pd.read_sql(path.read_text(), con)
        df.to_csv(RESULTS / f"{path.stem}.csv", index=False)
        results[path.stem] = df
        print(f"\n== {path.stem} ==\n{df.to_string(index=False)}")
    return results


def style(ax, title: str) -> None:
    ax.set_title(title, loc="left", fontsize=12, fontweight="bold")
    ax.spines[["top", "right"]].set_visible(False)


def chart_delivery(df: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(7, 3.6))
    labels = df["delivery_bucket"].str[3:]
    colors = [BLUE, BLUE, RED, RED]
    bars = ax.bar(labels, df["pct_bad_reviews"], color=colors)
    ax.bar_label(bars, fmt="%.0f%%", padding=3)
    ax.set_ylabel("% of orders with a 1-2 star review")
    style(ax, "Late deliveries turn into bad reviews")
    fig.tight_layout()
    fig.savefig(ASSETS / "late_delivery_vs_bad_reviews.png", dpi=160)


def chart_repurchase(df: pd.DataFrame) -> None:
    bad = df[(df["first_delivery"] == "late") & df["first_review"].str.startswith("1")].iloc[0]
    good = df[(df["first_delivery"] == "on time") & df["first_review"].str.startswith("3")].iloc[0]
    drop = 1 - bad["pct_repurchased"] / good["pct_repurchased"]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    bars = ax.bar(
        ["First order late and rated 1-2", "First order on time and rated 4-5"],
        [bad["pct_repurchased"], good["pct_repurchased"]],
        color=[RED, BLUE],
    )
    ax.bar_label(bars, fmt="%.1f%%", padding=3)
    ax.set_ylabel("% of customers who bought again")
    style(ax, f"After a late, badly rated first order, {drop:.0%} fewer customers return")
    fig.tight_layout()
    fig.savefig(ASSETS / "first_experience_vs_repurchase.png", dpi=160)


def main() -> None:
    RESULTS.mkdir(exist_ok=True)
    ASSETS.mkdir(exist_ok=True)
    if not DB.exists():
        build()
    with sqlite3.connect(DB) as con:
        results = run_queries(con)
    chart_delivery(results["02_late_delivery_vs_reviews"])
    chart_repurchase(results["03_first_experience_vs_repurchase"])


if __name__ == "__main__":
    main()
