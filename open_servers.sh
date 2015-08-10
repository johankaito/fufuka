#!/bin/bash

bin/zookeeper-server-start.sh config/zookeeper.properties&
bin/kafka-server-start.sh config/server1.properties&
bin/kafka-server-start.sh config/server2.properties&
bin/kafka-server-start.sh config/server3.properties&

