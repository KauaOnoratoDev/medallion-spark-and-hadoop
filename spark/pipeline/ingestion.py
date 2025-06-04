import os
from pyspark.sql import SparkSession
from dotenv import load_dotenv

load_dotenv()

hdfs_url = os.getenv('HDFS_URL')
spark_warehouse_dir = f'{hdfs_url}/tmp/spark-warehouse'

spark: SparkSession = SparkSession.builder.appName("Ingestion").config("spark.sql.warehouse.dir", spark_warehouse_dir).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

database = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
jdbc_url = f"jdbc:postgresql://{os.getenv('DB_HOST')}:5432/{database}"
hdfs_base_path = f"{hdfs_url}/user/hadoop/datalake_ingestion"

tables = [
    'orders',
    'ordershistory',
]

for table in tables:
    print(f"Ingesting {table}...")
    print(f"{'-'*50}")
    
    try:
        df = spark.read.format('jdbc').options(
            url=jdbc_url,
            driver='org.postgresql.Driver',
            dbtable=table,
            user=user,
            password=password
        ).load()
        
        hdfs_output_path = f"{hdfs_base_path}/{table}"
        
        df.write.mode('overwrite').parquet(hdfs_output_path)
        
        df.show()
        print(f"Ingestion completed successfully!")

    except Exception as e:
        print(f"Error ingesting {table}: {str(e)}")

spark.stop()