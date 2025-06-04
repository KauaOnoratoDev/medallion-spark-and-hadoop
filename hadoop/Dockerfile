FROM bde2020/hadoop-namenode:2.0.0-hadoop3.2.1-java8

COPY create_hdfs_dir.sh /usr/local/bin/create_hdfs_dir.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh

COPY config/core-site.xml /etc/hadoop/core-site.xml
COPY config/hdfs-site.xml /etc/hadoop/hdfs-site.xml

RUN chmod +x /usr/local/bin/create_hdfs_dir.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
