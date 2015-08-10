#!/bin/bash

bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic t1
bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic t2
bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic t3

bin/kafka-server-stop.sh config/server.properties 
bin/kafka-server-stop.sh config/server1.properties 
bin/kafka-server-stop.sh config/server2.properties 
bin/kafka-server-stop.sh config/server3.properties 
rm -rf /var/kafka-logs/t*
