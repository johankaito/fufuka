#!/bin/bash

bin/kafka-server-stop.sh config/server.properties 
#sleep 2
bin/kafka-server-stop.sh config/server1.properties 
#sleep 2
bin/kafka-server-stop.sh config/server2.properties 
#sleep 2
bin/kafka-server-stop.sh config/server3.properties 
#sleep 2
bin/zookeeper-server-stop.sh 
pkill -9 -f kafka
pkill -9 -f zookeeper
