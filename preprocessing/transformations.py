# This document serves to store all SQL queries relating to the customer segmentation project

queries = {
    # Aggregates by customerID and returns customer profile and engagement with store
    'customer_profile_query':[
        {
            'name': 'customer_profile',
            'query': """
                SELECT 
                    customer_id, 
                    customer_name,
                    customer_age,
                    gender,
                    count(*) as order_count,
                    round(sum(returned), 1) as orders_returned,
                    sum(churn) as total_churn,
                    datediff(max(purchase_date), min(purchase_date)) as tenure_days,
                    avg(product_price) as average_total_per_cart,
                    sum(quantity) as total_qty_purchased,
                    sum(total_purchased_amount) as total_spent_historic,
                    sum(CASE WHEN payment_method = 'Credit Card' THEN 1 ELSE 0 END) as payment_creditcard,
                    sum(CASE WHEN payment_method = 'Debit' THEN 1 ELSE 0 END) as payment_debit,
                    sum(CASE WHEN payment_method = 'Crypto' THEN 1 ELSE 0 END) as payment_crypto,
                    sum(CASE WHEN payment_method = 'PayPal' THEN 1 ELSE 0 END) as payment_paypal,
                    sum(CASE WHEN payment_method = 'Cash' THEN 1 ELSE 0 END) as payment_cash,
                    sum(CASE WHEN product_category = 'Electronics' THEN 1 ELSE 0 END) as cat_electronics,
                    sum(CASE WHEN product_category = 'Home' THEN 1 ELSE 0 END) as cat_home,
                    sum(CASE WHEN product_category = 'Clothing' THEN 1 ELSE 0 END) as cat_clothing,
                    sum(CASE WHEN product_category = 'Books' THEN 1 ELSE 0 END) as cat_books
                FROM 
                    customer_data
                GROUP BY 
                    customer_id, customer_name, customer_age, gender
                """
        }
    ],

    # Aggregates by customer ID and returns shopping instances and payment instances
    # 'customer_shopping_profile_query': [
    #     {
    #         'name': 'customer_shopping_profile',
    #         'query': """
    #             SELECT
    #                 customer_id,
    #                 sum(CASE WHEN payment_method = 'Credit Card' THEN 1 ELSE 0 END) as payment_creditcard,
    #                 sum(CASE WHEN payment_method = 'Crypto' THEN 1 ELSE 0 END) as payment_crypto,
    #                 sum(CASE WHEN payment_method = 'Paypal' THEN 1 ELSE 0 END) as payment_paypal,
    #                 sum(CASE WHEN payment_method = 'Cash' THEN 1 ELSE 0 END) as payment_cash,
    #                 sum(CASE WHEN product_category = 'Electronics' THEN 1 ELSE 0 END) as cat_electronics,
    #                 sum(CASE WHEN product_category = 'Home' THEN 1 ELSE 0 END) as cat_home,
    #                 sum(CASE WHEN product_category = 'Clothing' THEN 1 ELSE 0 END) as cat_clothing,
    #                 sum(CASE WHEN product_category = 'Books' THEN 1 ELSE 0 END) as cat_books
    #             FROM
    #                 customer_data
    #             GROUP BY
    #                 customer_id, customer_name, customer_age, gender
    #             """
    #     }
    # ],

    # Post-process all orders (OHE)
    'ecommerce_orders_OHE_query': [
        {
            'name': 'ecommerce_orders_OHE',
            'query': """ 
                SELECT 
                    customer_id,
                    purchase_date,
                    CASE WHEN product_category = 'Electronics' THEN 1 ELSE 0 END as is_electronics,
                    CASE WHEN product_category = 'Home' THEN 1 ELSE 0 END as is_home,
                    CASE WHEN product_category = 'Clothing' THEN 1 ELSE 0 END as is_clothing,
                    CASE WHEN product_category = 'Books' THEN 1 ELSE 0 END as is_books,
                    product_price,
                    quantity,
                    total_purchased_amount,
                    CASE WHEN payment_method = 'Credit Card' THEN 1 ELSE 0 END as is_credit,
                    CASE WHEN payment_method = 'Crypto' THEN 1 ELSE 0 END as is_crypto,
                    CASE WHEN payment_method = 'Paypal' THEN 1 ELSE 0 END as is_paypal,
                    CASE WHEN payment_method = 'Cash' THEN 1 ELSE 0 END as is_cash,
                    customer_age,
                    returned,
                    CASE WHEN gender = 'Male' THEN 1 ELSE 0 END as gender_1m_0f,
                    churn
                FROM
                    customer_data
                """
        }
    ],

    # Aggregate by date
    'sales_by_day': [
        {
            'name': 'total_sales_by_date',
            'query': """ 
                SELECT 
                    purchase_date,
                    count(*) AS checkout_instances,
                    sum(CASE WHEN product_category = 'Electronics' THEN 1 ELSE 0 END) as cat_electronics,
                    sum(CASE WHEN product_category = 'Home' THEN 1 ELSE 0 END) as cat_home,
                    sum(CASE WHEN product_category = 'Clothing' THEN 1 ELSE 0 END) as cat_clothing,
                    sum(CASE WHEN product_category = 'Books' THEN 1 ELSE 0 END) as cat_books,
                    avg(product_price) AS avg_revenue_per_unit,
                    sum(quantity) AS units_sold,
                    sum(total_purchased_amount) AS revenue,
                    sum(CASE WHEN payment_method = 'Credit Card' THEN 1 ELSE 0 END) as credit_instances,
                    sum(CASE WHEN payment_method = 'Crypto' THEN 1 ELSE 0 END) as crypto_instances,
                    sum(CASE WHEN payment_method = 'PayPal' THEN 1 ELSE 0 END) as paypal_instances,
                    sum(CASE WHEN payment_method = 'Cash' THEN 1 ELSE 0 END) as cash_instances,
                    sum(returned) AS total_returns,
                    sum(CASE WHEN churn = 1 THEN 1 ELSE 0 END) as churned,
                    sum(CASE WHEN churn = 0 THEN 1 ELSE 0 END) as retained
                FROM
                    customer_data
                GROUP BY 
                    purchase_date
            """
        }
    ]
}