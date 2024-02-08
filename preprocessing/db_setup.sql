CREATE DATABASE "ecommerceDB"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

DROP TABLE IF EXISTS customer_data;

CREATE TABLE customer_data(
	customer_id integer,
	purchase_date date,
	product_category characer varying,
	product_price integer,
	quantity integer,
	total_purchased_amount integer,
	payment_method varchar,
	customer_age integer,
	returned numeric,
	customer_name characer varying,
	age integer,
	gender characer varying,
	churn integer
);