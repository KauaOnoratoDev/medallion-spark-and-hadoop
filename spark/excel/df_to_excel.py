from pyspark.sql import SparkSession
from dotenv import load_dotenv
import os


load_dotenv()

spark: SparkSession = SparkSession.builder.appName("df_to_excel").getOrCreate()
hdfs_url = os.getenv("HDFS_URL")
hdfs_gold_path = f"{hdfs_url}/user/hadoop/datalake_serving"

try:
    df_deliveries_avg = spark.read.parquet(f"{hdfs_gold_path}/deliveries_avg")
    df_deliveries_count = spark.read.parquet(f"{hdfs_gold_path}/deliveries_count")

    if not os.path.exists('./excel/files/'):
        os.makedirs('./excel/files/')
        print('Pasta files/ criada.')

    df_deliveries_avg.toPandas().to_excel("./excel/files/deliveries_avg.xlsx")
    df_deliveries_count.toPandas().to_excel("./excel/files/deliveries_count.xlsx")
    print('Arquivos excel gerados com sucesso.')
    
except Exception as e:
    print(f"Erro ao gerar arquivos excel: {e}")