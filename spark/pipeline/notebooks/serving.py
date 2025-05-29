from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os


load_dotenv()
spark_warehouse_dir = '/tmp/spark-warehouse'
hdfs_url = os.getenv('HDFS_URL')
hdfs_silver_path = f"{hdfs_url}/datalake_transformation/allorders"
hdfs_gold_path = f"{hdfs_url}/datalake_serving"

spark: SparkSession = SparkSession.builder.appName("Serving") \
    .config("spark.sql.warehouse.dir", spark_warehouse_dir) \
    .getOrCreate()
     
spark.sparkContext.setLogLevel("ERROR")

all_orders_pivot_query = """
    SELECT
        t1.order_id,
        t1.history_id,
        t1.branch,
        t1.order_time AS start,
        t2.updated_at AS end,
        (unix_timestamp(end) - unix_timestamp(start)) / 86400 AS delivery_time
    FROM (SELECT * FROM allorders WHERE status = 'new') AS t1
    INNER JOIN (SELECT * FROM allorders WHERE status = 'delivered') AS t2
    ON t1.order_id = t2.order_id
"""

deliveries_avg_query = """
    SELECT branch, ROUND(AVG(delivery_time), 2) AS avg_delivery_time
    FROM allorders_pivot
    GROUP BY branch
    ORDER BY 2 ASC
"""

deliveries_count_query = """
    SELECT branch, COUNT(*) AS deliveries_count
    FROM allorders_pivot
    GROUP BY branch
    ORDER BY 2 DESC
"""

try:
    silver_table_df = spark.read.parquet(hdfs_silver_path)
    silver_table_df.createOrReplaceTempView('allorders')

    spark.sql(all_orders_pivot_query).createOrReplaceTempView("allorders_pivot")
    
    deliveries_avg = spark.sql(deliveries_avg_query)
    deliveries_avg.write.mode("overwrite").parquet(f'{hdfs_gold_path}/deliveries_avg')


    deliveries_count = spark.sql(deliveries_count_query)
    deliveries_count.write.mode("overwrite").parquet(f"{hdfs_gold_path}/deliveries_count")
    
    deliveries_avg.show()
    deliveries_count.show()
    print(f"Serving completed successfully!")
    
except Exception as e:
    print(f"Erro na transformação: {str(e)}")

spark.stop()