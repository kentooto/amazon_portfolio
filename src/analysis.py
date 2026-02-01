import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# データ読み込み

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_FILE = BASE_DIR / "data" / "processed" / "product_summary.csv"

df = pd.read_csv(DATA_FILE)

print("analysis shape:", df.shape)
print(df.head())

# 1.ランク別 基本統計

summary_by_rank = (
    df
    .groupby("popularity_rank")
    .agg(
        avg_price_mean=("avg_price", "mean"),
        avg_rating_mean=("avg_rating", "mean"),
        review_count_mean=("review_count", "mean"),
        product_count=("product_id", "count")
    )
)

rank_order = ["A", "B", "C"]
summary_by_rank = summary_by_rank.reindex(rank_order)

print("\n=== ランク別集計 ===")
print(summary_by_rank)

# 2.可視化（レビュー数）

summary_by_rank["review_count_mean"].plot(kind="bar")
plt.title("人気ランク別平均レビュー数")
plt.xlabel("Popularity Rank")
plt.ylabel("Average Review Count")
plt.tight_layout()
plt.show()