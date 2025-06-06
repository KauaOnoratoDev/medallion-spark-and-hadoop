#!/bin/bash

# Formata o NameNode apenas se ainda não estiver formatado
if [ ! -d "/hadoop/dfs/name/current" ]; then
    echo "Formatando o NameNode..."
    hdfs namenode -format -force
fi

# Inicia o NameNode
hdfs namenode &

# Dá um tempo para o NameNode subir
sleep 5

# Executa o script de criação de diretórios no HDFS
/usr/local/bin/create_hdfs_dir.sh

# Força a saída do Safe Mode
echo "⏳ Forçando saída do Safe Mode..."
hdfs dfsadmin -safemode leave

# Mantém o container ativo
wait
