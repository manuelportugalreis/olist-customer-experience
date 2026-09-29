"""Early-warning model: which orders are likely to get a 1-2 star review?

Two versions, to separate what the company can predict from what it can only react to:
- "at purchase": only information known when the order is placed.
- "at delivery": adds how late the order arrived.
The test set is the most recent months (time-based split), as it would be in production.
"""
import json
import sqlite3
from math import sqrt
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from build_database import DB

ROOT = Path(__file__).resolve().parents[1]
SPLIT_DATE = "2018-04-01"

QUERY = """
SELECT d.*,
       COALESCE(t.product_category_name_english, 'unknown') AS category
FROM delivered_orders d
JOIN (SELECT order_id, MIN(product_id) AS product_id FROM order_items GROUP BY order_id) first_item
     ON first_item.order_id = d.order_id
JOIN products p ON p.product_id = first_item.product_id
LEFT JOIN category_translation t ON t.product_category_name = p.product_category_name
WHERE d.review_score IS NOT NULL
"""

AT_PURCHASE_NUMERIC = ["promised_days", "n_items", "n_sellers", "items_value", "freight_share"]
CATEGORICAL = ["customer_state", "category"]
AT_DELIVERY_NUMERIC = AT_PURCHASE_NUMERIC + ["days_late", "actual_days"]


def load() -> pd.DataFrame:
    with sqlite3.connect(DB) as con:
        con.executescript((ROOT / "sql" / "00_delivered_orders.sql").read_text())
        df = pd.read_sql(QUERY, con)
    df["freight_share"] = df["freight_value"] / (df["items_value"] + df["freight_value"])
    df["bad_review"] = (df["review_score"] <= 2).astype(int)
    return df


def evaluate(df: pd.DataFrame, numeric: list[str]) -> dict[str, float]:
    train = df[df["order_purchase_timestamp"] < SPLIT_DATE]
    test = df[df["order_purchase_timestamp"] >= SPLIT_DATE]
    features = numeric + CATEGORICAL
    encode = ColumnTransformer([
        ("num", StandardScaler(), numeric),
        ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=100), CATEGORICAL),
    ])
    models = {
        "logistic_regression": make_pipeline(encode, LogisticRegression(max_iter=1000)),
        "gradient_boosting": make_pipeline(
            ColumnTransformer([
                ("num", "passthrough", numeric),
                ("cat", OneHotEncoder(handle_unknown="ignore", min_frequency=100, sparse_output=False), CATEGORICAL),
            ]),
            HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=0),
        ),
    }
    scores = {}
    for name, model in models.items():
        model.fit(train[features], train["bad_review"])
        scores[name] = round(roc_auc_score(test["bad_review"], model.predict_proba(test[features])[:, 1]), 3)
    return scores


def repurchase_gap_z() -> dict[str, float]:
    """Two-proportion z-test: repurchase after a late + bad first order vs an on-time + good one."""
    r = pd.read_csv(ROOT / "results" / "03_first_experience_vs_repurchase.csv")
    bad = r[(r.first_delivery == "late") & (r.first_review.str.startswith("1"))].iloc[0]
    good = r[(r.first_delivery == "on time") & (r.first_review.str.startswith("3"))].iloc[0]
    p1, n1 = bad.pct_repurchased / 100, bad.customers
    p2, n2 = good.pct_repurchased / 100, good.customers
    z = (p2 - p1) / sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    return {"repurchase_late_bad_pct": round(p1 * 100, 2), "repurchase_on_time_good_pct": round(p2 * 100, 2), "z": round(z, 2)}


def main() -> None:
    df = load()
    results = {
        "orders": len(df),
        "bad_review_rate": round(df["bad_review"].mean(), 3),
        "auc_at_purchase": evaluate(df, AT_PURCHASE_NUMERIC),
        "auc_at_delivery": evaluate(df, AT_DELIVERY_NUMERIC),
        "repurchase_gap": repurchase_gap_z(),
    }
    (ROOT / "results" / "model_results.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
