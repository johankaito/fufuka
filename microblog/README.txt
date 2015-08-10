This is how the front end works:

Requirements:
	Jolokia: JMX-Mbean REST API
		Running:(Refer to Jolokia)
			- Ask jolokia-jvm to bind to a particular process id (Frome beginning or during run-time,
			  prefereable from the beginning
			- This will start Jolokia and provide you with a port to go listen in for the REST api
			- Responsible for providing real-time metrics of the KafkaInstance. Handles the dynamics
			  of the observed graph

	ExtClient-Microblog:
		- This is the middle portion of the application. It loads data from zookeeper to draw the graph
	
	(Optional)
	Confluent: Kafka Rest API
			- Confluent platform comes along with a Kafka-REST-API.

	
Running notes:
Attaching Jolokia to PID:
	java -jar jolokia-jvm-1.3.1-agent.jar --help
	