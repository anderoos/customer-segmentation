# Dependencies
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import warnings

# Transformations file
from transformations import queries

# Probs better to set up environmental variables for this
from passwords import db_params

# Filter warnings
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

    def transform_customers(self, transformations_dict):
        try:
            print('Transforming data from view...')
            transformed_dfs = dict()
            for xfm_key, xfm_values in transformations_dict.items():
                for xfm in xfm_values:
                    table_name = xfm['name']
                    query = xfm['query']
                    print(f'Transforming {table_name}')
                    temp_df = self.spark.sql(query)
                    transformed_dfs[table_name] = temp_df
            print('Data transformed successfully!')
            print(f'DFs Mounted: {transformed_dfs.keys()}')
            return transformed_dfs
        except Exception as err:
            print('Error Encountered during transformation:' + str(err))

    def load_customers(self, df_dict):
        try:
            print('Loading transformed data into database...')
            for k, v in df_dict.items():
                print(f'Wrting {k}...')
                df_dict[k].write.jdbc(url=self.database_url,
                                      table=f'{k}',
                                      mode='overwrite',
                                      properties=self.properties)
            print('Data loaded successfully!')
        except Exception as err:
            print('Error Encountered during loading:' + str(err))

    def stop_spark(self):
        self.spark.stop()
        print('Spark Session successfully terminated.')


# Declarations
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
    dataframes_dict = etl_instance.transform_customers(queries)
    etl_instance.load_customers(dataframes_dict)
    etl_instance.stop_spark()
