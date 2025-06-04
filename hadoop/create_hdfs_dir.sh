#!/bin/bash

# Configurações de diretórios e usuários
HDFS_BASE_PATH="/user/hadoop"
DIRECTORIES=(
    "datalake_ingestion"
    "datalake_transformation"
    "datalake_serving"
)

CREATOR_USER="root"
OWNER_USER="spark"

# Criar e configurar diretórios de datalake
for dir in "${DIRECTORIES[@]}"; do
    FULL_PATH="${HDFS_BASE_PATH}/${dir}"
    echo "Configurando $FULL_PATH..."

    HADOOP_USER_NAME=$CREATOR_USER hdfs dfs -mkdir -p "$FULL_PATH"
    HADOOP_USER_NAME=$CREATOR_USER hdfs dfs -chown -R "$OWNER_USER":supergroup "$FULL_PATH"
    HADOOP_USER_NAME=$OWNER_USER hdfs dfs -chmod -R 775 "$FULL_PATH"
done

# Criar e configurar o diretório Spark SQL warehouse
SPARK_WAREHOUSE_PATH="/tmp/spark-warehouse"
echo "Configurando $SPARK_WAREHOUSE_PATH..."

HADOOP_USER_NAME=$CREATOR_USER hdfs dfs -mkdir -p "$SPARK_WAREHOUSE_PATH"
HADOOP_USER_NAME=$CREATOR_USER hdfs dfs -chown "$OWNER_USER":supergroup "$SPARK_WAREHOUSE_PATH"
HADOOP_USER_NAME=$OWNER_USER hdfs dfs -chmod 777 "$SPARK_WAREHOUSE_PATH" # Permissões mais abertas para o warehouse em dev

echo "Configuração HDFS concluída."