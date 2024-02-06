# Dependencies
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import warnings

# Probs better to set up environmental variables for this
from passwords import db_params
warnings.filterwarnings('ignore')

class CustomerETLPipeline:
    # Initalize with app, jarpath, database url, dbproperties
    def __init__(self, jdbc_jar_path, database_url, properties):
        self.spark = SparkSession.builder \
            .appName('ecommerce_etl_pipeline') \
            .config('spark.jars', jdbc_jar_path) \
            .getOrCreate()
        self.database_url = database_url
        self.properties = properties

    # Extract data from postgres database
    def extract_customers(self, table_name):
        try:
            print('Extracting data from database...')
            df = self.spark.read.jdbc(url=self.database_url,
                                      table=table_name,
                                      properties=self.properties)
            df.createOrReplaceTempView('customer_data')
            print('Data Extracted Successfully!')
            return df
        except Exception as err:
            print('Error extracting data from url. Check credentials or schema.')

    def transform_customers(self):
        try:
            print('Transforming data from view...')
            customer_profile = self.spark.sql("""
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
                    sum(total_purchased_amount) as total_spent_historic
                FROM 
                    customer_data
                GROUP BY 
                    customer_id, customer_name, customer_age, gender
                """)

            customer_shopping_profile = self.spark.sql("""
                SELECT 
                    customer_id, 
                    sum(CASE WHEN payment_method = 'Credit Card' THEN 1 ELSE 0 END) as payment_creditcard,
                    sum(CASE WHEN payment_method = 'Debit' THEN 1 ELSE 0 END) as payment_debit,
                    sum(CASE WHEN payment_method = 'Crypto' THEN 1 ELSE 0 END) as payment_crypto,
                    sum(CASE WHEN payment_method = 'Paypal' THEN 1 ELSE 0 END) as payment_paypal,
                    sum(CASE WHEN payment_method = 'Cash' THEN 1 ELSE 0 END) as payment_cash,
                    sum(CASE WHEN product_category = 'Electronics' THEN 1 ELSE 0 END) as cat_electronics,
                    sum(CASE WHEN product_category = 'Home' THEN 1 ELSE 0 END) as cat_home,
                    sum(CASE WHEN product_category = 'Clothing' THEN 1 ELSE 0 END) as cat_clothing,
                    sum(CASE WHEN product_category = 'Books' THEN 1 ELSE 0 END) as cat_books
                FROM 
                    customer_data
                GROUP BY 
                    customer_id, customer_name, customer_age, gender
                """)
            print('Data transformed successfully!')
            return customer_profile, customer_shopping_profile
        except Exception as err:
            print('Error Encountered during transformation:' + str(err))

    def load_customers(self, customer_profile, customer_shopping_profile):
        try:
            print('Loading transformed data into database...')
            customer_profile.write.jdbc(url=self.database_url,
                                        table='customer_profile',
                                        mode='overwrite',
                                        properties=self.properties)
            customer_shopping_profile.write.jdbc(url=self.database_url,
                                                 table='customer_shopping_profile',
                                                 mode='overwrite',
                                                 properties=self.properties)
            print('Data loaded successfully!')
        except Exception as err:
            print('Error Encountered during loading:' + str(err))

    def stop_spark(self):
        self.spark.stop()
        print('Spark Session successfully terminated.')


# Example usage
if __name__ == "__main__":
    jdbc_jar_path = '../Resources/postgresql-42.7.1.jar'
    database_url = "jdbc:postgresql://localhost:5432/ecommerceDB"
    properties = {
        "user": db_params['user'],
        "password": db_params['password'],
        "driver": "org.postgresql.Driver"
    }

# Execution
    etl_instance = CustomerETLPipeline(jdbc_jar_path, database_url, properties)
    df = etl_instance.extract_customers("customer_data")
    customer_profile, customer_shopping_profile = etl_instance.transform_customers()
    etl_instance.load_customers(customer_profile, customer_shopping_profile)
    etl_instance.stop_spark()

#%%
