-- 商品単位に集計
-- 1行 = 1商品
CREATE TEMP TABLE product_summary AS
SELECT
    product_id,
    category,
    AVG(discounted_price) AS avg_price,
    AVG(rating) AS avg_rating,
    SUM(rating_count) AS review_count
FROM amazon_preprocessed
GROUP BY
    product_id,
    category;
    
-- 集計結果確認
SELECT
    *
FROM product_summary
LIMIT 5;

-- 人気度ランク付け
-- レビュー数を基準に3段階評価
CREATE TEMP TABLE product_ranked AS
SELECT
    product_id,
    category,
    avg_price,
    avg_rating,
    review_count,
    CASE
        WHEN review_count >= 1000 THEN 'A'
        WHEN review_count >= 300 THEN 'B'
        ELSE 'C'
    END AS popularity_rank
FROM product_summary;

-- ランク分布確認
SELECT
    popularity_rank,
    COUNT(*) AS product_count
FROM product_ranked
GROUP BY popularity_rank
ORDER BY popularity_rank;

-- ランク別の傾向確認
SELECT
    popularity_rank,
    ROUND(AVG(avg_price), 2) AS avg_price,
    ROUND(AVG(avg_rating), 2) AS avg_rating,
    AVG(review_count) AS avg_review_count
FROM product_ranked
GROUP BY popularity_rank
ORDER BY popularity_rank;