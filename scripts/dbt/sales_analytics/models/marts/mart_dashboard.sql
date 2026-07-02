-- Final mart: Dashboard ke liye ready data
SELECT
    -- Order Info
    ORDER_ID,
    ORDER_DATE,
    YEAR,
    MONTH,
    MONTH_NAME,
    QUARTER,

    -- Customer Info
    CUSTOMER_ID,
    CUSTOMER_NAME,
    SEGMENT,

    -- Location Info
    REGION,
    STATE,
    CITY,

    -- Product Info
    CATEGORY,
    SUB_CATEGORY,
    PRODUCT_NAME,

    -- Sales Metrics
    SALES,
    DAYS_TO_SHIP,
    RUNNING_MONTHLY_REVENUE,
    TOTAL_REGION_REVENUE,
    TOTAL_CATEGORY_REVENUE,
    AVG_SEGMENT_SALES,

    -- KPIs
    CASE
        WHEN SALES >= 1000 THEN 'High Value'
        WHEN SALES >= 200  THEN 'Medium Value'
        ELSE 'Low Value'
    END AS ORDER_VALUE_SEGMENT,

    CASE
        WHEN DAYS_TO_SHIP <= 2 THEN 'Fast'
        WHEN DAYS_TO_SHIP <= 5 THEN 'Normal'
        ELSE 'Slow'
    END AS SHIPPING_SPEED

FROM {{ ref('int_revenue') }}