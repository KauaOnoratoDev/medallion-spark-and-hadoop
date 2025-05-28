#!/bin/bash

HDFS_BASE_PATH="hdfs://localhost:9000/sparkuser/hadoop"

DIRECTORIES=(
    "datalake_ingestion"
    "datalake_transformation"
    "datalake_serving"
)

for dir in "${DIRECTORIES[@]}"; do
    FULL_PATH="${HDFS_BASE_PATH}/${dir}"

    hdfs dfs -mkdir -p "$FULL_PATH"
    
    if [ $? -eq 0 ]; then
        echo "Diretório $FULL_PATH criado com sucesso ou já existente."
    else
        echo "ERRO: Falha ao criar o diretório $FULL_PATH. Verifique sua conexão HDFS e permissões."
        exit 1 
    fi
done
