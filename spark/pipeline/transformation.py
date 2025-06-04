import os
from pyspark.sql import SparkSession
from  pyspark.sql.functions import col, to_date
from dotenv import load_dotenv

load_dotenv()

hdfs_url = os.getenv('HDFS_URL')
spark_warehouse_dir = f'{hdfs_url}/tmp/spark-warehouse'

spark: SparkSession = SparkSession.builder.appName("Transformation").config("spark.sql.warehouse.dir", spark_warehouse_dir).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

hdfs_bronze_orders_path = f"{hdfs_url}/user/hadoop/datalake_ingestion/orders"
hdfs_bronze_ordershistory_path = f"{hdfs_url}/user/hadoop/datalake_ingestion/ordershistory"
hdfs_silver_path = f"{hdfs_url}/user/hadoop/datalake_transformation/allorders"

joined_dataframe_query = """
    SELECT
        o.order_id,
        order_time,
        branch,
        history_id,
        status,
        updated_at
    FROM global_temp.orders_view AS o
    INNER JOIN global_temp.ordershistory_view AS oh
        ON o.order_id = oh.order_id
    WHERE
        status != "intransit"
"""

try:
    # Load data from HDFS
    orders_df = spark.read.parquet(hdfs_bronze_orders_path)
    orders_history_df = spark.read.parquet(hdfs_bronze_ordershistory_path)
    
    # Create temporary views
    orders_df.createOrReplaceGlobalTempView('orders_view')
    orders_history_df.createOrReplaceGlobalTempView('ordershistory_view')
    
    joined_df = spark.sql(joined_dataframe_query)  
    joined_df = joined_df.withColumn("updated_day", to_date(col("updated_at")))
    
    # Save the result to HDFS
    joined_df.write.mode('overwrite').partitionBy('updated_day').parquet(hdfs_silver_path)
    
    joined_df.show()
    print("Transformation completed successfully!")
    
except Exception as e:
    print(f"Erro na transformação: {str(e)}")
    
spark.stop()