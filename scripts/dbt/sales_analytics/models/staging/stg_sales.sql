-- Staging model: Raw data ko clean karke laata hai
SELECT
    ORDER_ID,
    ORDER_DATE,
    SHIP_DATE,
    SHIP_MODE,
    CUSTOMER_ID,
    CUSTOMER_NAME,
    SEGMENT,
    COUNTRY,
    CITY,
    STATE,
    POSTAL_CODE,
    REGION,
    PRODUCT_ID,
    CATEGORY,
    SUB_CATEGORY,
    PRODUCT_NAME,
    SALES,
    YEAR,
    MONTH,
    MONTH_NAME,
    QUARTER,
    DAYS_TO_SHIP
FROM {{ source('sales', 'RAW_SALES') }}
WHERE SALES > 0