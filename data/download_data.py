"""Download the Olist Brazilian e-commerce dataset from Olist's official public repository.

The same data is published on Kaggle as "Brazilian E-Commerce Public Dataset by Olist"
(license: CC BY-NC-SA 4.0).
"""
from pathlib import Path
from urllib.request import urlretrieve

BASE = "https://raw.githubusercontent.com/olist/work-at-olist-data/master/datasets/"
FILES = [
    "olist_orders_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "product_category_name_translation.csv",
]

raw = Path(__file__).parent / "raw"
raw.mkdir(exist_ok=True)
for name in FILES:
    target = raw / name
    if not target.exists():
        print(f"Downloading {name}...")
        urlretrieve(BASE + name, target)
print(f"Data ready in {raw}")
