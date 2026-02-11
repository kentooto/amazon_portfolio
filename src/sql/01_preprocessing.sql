-- 元データ確認
SELECT
    product_id,
    category,
    discounted_price,
    rating,
    rating_count
FROM amazon_raw
LIMIT 5;

-- 前処理用テーブル作成
-- 分析で使用する最小限の列に絞る
-- 文字列として入っている数値を数値型に変換
CREATE TEMP TABLE amazon_preprocessed AS
SELECT
    product_id,
    category,
    CAST(
        REPLACE(
            REPLACE(discounted_price, '₹', ''),
            ',', ''
        ) AS DECIMAL(10,2)
    ) AS discounted_price,
    CAST(rating AS DECIMAL(3,2)) AS rating,
    CAST(
        REPLACE(rating_count, ',', '')
        AS INTEGER
    ) AS rating_count
FROM amazon_raw
WHERE
    discounted_price IS NOT NULL
    AND rating IS NOT NULL
    AND rating_count IS NOT NULL;
    
-- 前処理後データ確認
SELECT
    *
FROM amazon_preprocessed
LIMIT 5;