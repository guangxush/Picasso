1. 按照Zookeeper和Kafka
2. 先启动Zookeeper```/usr/local/Cellar/zookeeper/3.4.13/bin/zkServer start```
3. 然后启动Kafka```/usr/local/Cellar/kafka/2.2.1/bin/zookeeper-server-start /usr/local/etc/kafka/server.properties &```
4. 创建Kafka主题，这里我们使用news: ```kafka-console-producer --broker-list localhost:9092 --topic news```
5. 查看主题是否创建成功：```./kafka-topics --list --zookeeper localhost:2181```