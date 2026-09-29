"""Load the raw CSVs into a SQLite database so the analysis can be written in SQL."""
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DB = ROOT / "data" / "olist.db"

TABLES = {
    "orders": "olist_orders_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
    "products": "olist_products_dataset.csv",
    "category_translation": "product_category_name_translation.csv",
}

INDEXES = [
    "CREATE INDEX IF NOT EXISTS ix_orders_order ON orders(order_id)",
    "CREATE INDEX IF NOT EXISTS ix_orders_customer ON orders(customer_id)",
    "CREATE INDEX IF NOT EXISTS ix_customers_customer ON customers(customer_id)",
    "CREATE INDEX IF NOT EXISTS ix_items_order ON order_items(order_id)",
    "CREATE INDEX IF NOT EXISTS ix_payments_order ON order_payments(order_id)",
    "CREATE INDEX IF NOT EXISTS ix_reviews_order ON order_reviews(order_id)",
    "CREATE INDEX IF NOT EXISTS ix_products_product ON products(product_id)",
]


def build() -> Path:
    with sqlite3.connect(DB) as con:
        for table, file in TABLES.items():
            pd.read_csv(RAW / file).to_sql(table, con, index=False, if_exists="replace")
        for statement in INDEXES:
            con.execute(statement)
    return DB


if __name__ == "__main__":
    print(f"Built {build()}")
