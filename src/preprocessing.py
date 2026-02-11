import pandas as pd
import numpy as np
from pathlib import Path

# 0.パス定義

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

# RAW_FILE = RAW_DIR / "amazon.csv"
RAW_FILE = RAW_DIR / "sample_amazon.csv"  # サンプルCSVに切り替え
OUTPUT_FILE = PROCESSED_DIR / "product_summary.csv"

PROCESSED_DIR.mkdir(exist_ok=True)

# 1.データ読み込み

df = pd.read_csv(RAW_FILE)

print("raw shape:", df.shape)

# 2.今回の分析で使う「最小列」
# 今回の分析に必要な最小限のカラムのみを使用

use_cols = [
    "product_id",
    "category",
    "discounted_price",
    "rating",
    "rating_count"
]

df = df[use_cols]

print("selected cols shape:", df.shape)
print(df.head())

# 3.型変換（文字 → 数値）

price_cols = ["discounted_price"]
num_cols = ["rating", "rating_count"]

for col in price_cols + num_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("after type conversion")
print(df.dtypes)

# 4.商品単位に集計（1行 = 1商品）

product_summary = (
    df
    .groupby(["product_id", "category"], as_index=False)
    .agg(
        avg_price=("discounted_price", "mean"),
        avg_rating=("rating", "mean"),
        review_count=("rating_count", "sum")
    )
)

print("summary shape:", product_summary.shape)
print(product_summary.head())

# 5.人気度ランク付け（SQLの CASE WHEN 相当）

product_summary["popularity_rank"] = np.where(
    product_summary["review_count"] >= 1000, "A",
    np.where(product_summary["review_count"] >= 300, "B", "C")
)

# 6.ランク分布確認

rank_counts = (
    product_summary["popularity_rank"]
    .value_counts()
    .reindex(["A", "B", "C"], fill_value=0)
)

print("rank distribution")
print(rank_counts)

# 7.CSV出力

product_summary.to_csv(OUTPUT_FILE, index=False)
print("saved to:", OUTPUT_FILE)