#
#
#	IMPORTS
#
#
#	kazoo client itself
from kazoo.client import KazooClient

#	For creating and manipulating graphs
# import networkx as nx

#	For visualizing graph
# import matplotlib.pyplot as plt
# import graphviz
from graph_tool.all import *

#	logging purposes, required by zookeeper client
import logging


#
#
#	END OF IMPORTS
#
#
#
#	GLOBAL VARIABLES
#
#
#	Controller_epoch
controller_epoch = "/Controller_epoch"

#	Brokers
brokers = "/brokers"
topics = brokers + "/topics"
ids = brokers + "/ids"

#	Zookeeper
zookeeper = "/zookeeper"

#	Kafka-manager
kafka_manager = "/kafka-manager"

#	Admin
admin = "/admin"

#	Consumers
consumer_groups = "/consumers"

#	Config
config = "/config"

#	Producers
producers = "/producers"

#
#	END OF GLOBAL VARIABLES
#
#

#The class
class extended_client:
	"""Python class to extend client functionality when interacting with zk"""
	def __init__(self, url_port):
		#Start zookeeper client
		self.zk = KazooClient(hosts=url_port)
		self.zk.start();
	#
	#	FUNCTIONS
	#
	#

	#	Listen for when the connection is:
	#	dropped, restored, or when the Zookeeper session has expired

	def my_listener(state):
		if state == KazooState.LOST:
			# Register somewhere that the session was lost
			print "Connection lost"
		elif state == KazooState.SUSPENDED:
			# Handle being disconnected from Zookeeper
			print "Connection suspended"
		else:
			# Handle being connected/reconnected to Zookeeper
			print "Oh we are good!"

	#	1.	Get the number of brokers running
	def get_num_brokers(new_zk):
		if new_zk.exists(ids):
			#Brokers exist, find how many
			return len(new_zk.get_children(ids))

	#		Get all the existing brokers
	def get_brokers_ids(new_zk):
		if new_zk.exists(ids):
			#Brokers exist, find how many
			return new_zk.get_children(ids)

	#		Get a given broker given id
	def get_broker(new_zk, new_id):
		if new_zk.exists(ids):
			#Brokers exist, find how many
			return new_zk.get(ids + "/" + str(new_id))

	#		Get the info of a given topic
	def get_topic(new_zk, topic):
		return new_zk.get(topics + "/" + str(topic))

	#	2. 	Get the number of partitions of a given topic
	def get_num_partitions(new_zk, topic):
		partitions = topics + "/" + topic + "/partitions"
		if new_zk.exists(partitions):
			#Topic exists, get number of partitions
			return len(new_zk.get_children(partitions))

	# 		Get the total number of messages being sent through the cluster

	#	3. 	Get number of messages per partition

	#	4. 	Get the number of consumer groups
	def get_num_consumers(new_zk):
		if new_zk.exists(consumer_groups):
			#If directory exists
			return len(new_zk.get_children(consumer_groups))

	#	 	Get all the consumer groups
	def show_all_consumers(new_zk):
		if new_zk.exists(consumer_groups):
			#If directory exists
			return new_zk.get_children(consumer_groups)

	#		Get a particular consumer
	def get_consumer(new_zk, new_consumer):
		path = consumer_groups + "/" + new_consumer
		if new_zk.exists(path):
			return new_zk.get(path)
		return None
	#	5. 	Get the number of producers
	def get_num_producers(new_zk):
		if new_zk.exists(producers):
			#If directory exists
			return len(new_zk.get_children(producers))

	#	 	Get all the producers
	def show_all_producers(new_zk):
		if new_zk.exists(producers):
			#If directory exists
			return new_zk.get_children(producers)

	#		Get a particular producer
	def get_producer(new_zk, new_producer):
		path = producers + "/" + new_producer
		if new_zk.exists(path):
			return new_zk.get(path)
		return None

	#	6. 	Get the number of replicas of a given topic

	# 	7. 	Get the topic listened to by a given consumer group
	def show_consumer_topics(new_zk, new_group):
		path = consumer_groups + "/" + new_group + "/owners"
		if new_zk.exists(path):
			return new_zk.get_children(path)

	# 	8. 	Show the topic(s) posted by a given producer
	def show_producer_topics(new_zk, new_producer):
		path = producers + "/" + new_producer + "/topics" 
		if new_zk.exists(path):
			return new_zk.get_children(path)

	# 		Get number of topics in a given group
	def get_num_topics(new_zk, new_group):
		this_group_topics = consumer_groups + "/" + new_group + "/owners"
		if new_zk.exists(this_group_topics):
			return len(new_zk.get_children(this_group_topics))

	#		Get the total number of topics
	def get_total_num_topics(new_zk):
		if new_zk.exists(topics):
			return len(new_zk.get_children(topics))

	#		Get all the available topics
	def show_all_topics(new_zk):
		if new_zk.exists(topics):
			return new_zk.get_children(topics)

	#		Show topic consumer
	def show_topic_consumers(new_zk, new_topic):
		to_return = []
		if get_topic(new_zk, new_topic) is not None:
			#Topic exists
			#Get all the consumers 
			cons = show_all_consumers(new_zk)
			for con in cons:
				#For each consumer, get all its topics
				topics = show_consumer_topics(new_zk, con)
				for topic in topics:
					#For all the topics in this consumer
					#Check if the given topic is in there
					if topic == new_topic:
						#If it is, append it
						to_return.append(con)
		return to_return

	#		Show topic producer
	def show_topic_producers(new_zk, new_topic):
		to_return = []
		if get_topic(new_zk, new_topic) is not None:
			#Topic exists
			#Get all the producers
			prods = show_all_producers(new_zk)
			for prod in prods:
				#For each producer, get all its topics
				topics = show_producer_topics(new_zk, prod)
				for topic in topics:
					#For all the topics in this producer
					#Check if the given topic is in there
					if topic == new_topic:
						#If it is, append it
						to_return.append(prod)

		return to_return

	#		Get the node with the diven property "name"
	def get_vertex(new_di_graph, vertex_name):
		for i in new_di_graph.vertices():
			v = new_di_graph.vertex(i)
			
			#print "VNam: " + vertex_name
			#print "graph sting: " + new_di_graph.vp.string[v]
			if vertex_name == new_di_graph.vp.string[v]:
				return v
		return None

	#		Show consumer-producers. Producers which are also consumers
	def show_consumer_producers(new_zk):
		producers = show_all_producers(new_zk)
		con_prod = []
		for producer in producers:
			if get_consumer(new_zk, producer) is not None:
				con_prod.append(producer)
		return con_prod

	#		Show unique producers. Producers who are only producers
	def show_unique_producers(new_zk):
		producers = show_all_producers(new_zk)
		con_prods = show_consumer_producers(new_zk)

		for con_prod in con_prods:
			producers.remove(con_prod)

		return producers

	#		Show unique consumers. Consumers who are only consuemrs
	def show_unique_consumers(new_zk):
		consumers = show_all_consumers(new_zk)
		con_prods = show_consumer_producers(new_zk)

		for con_prod in con_prods:
			consumers.remove(con_prod)

		return consumers
	#		Create a graph 
	def get_digraph(new_zk):
		#	Graph
		# DG = nx.DiGraph()
		di_graph = Graph(directed=True)
		v_p = di_graph.new_vertex_property("string")
		topics = show_all_topics(new_zk)

		# Nodes which are both consumers and producers
		# con_prods_index = []
		consumer_producer_names = show_consumer_producers(new_zk)

		#print "Total topics: " + str(len(topics))
		# For each topic
		for topic in topics:
			# Create a node of that topic
			#DG.add_node(topic)
			# Create the node
			t = di_graph.add_vertex()
			# Add topic name to be part of properties of graph
			v_p[t] = topic
			#Get all consumers and producers
			producers = show_topic_producers(new_zk, topic)
			#print topic + "producers are : " + str(len(producers))
			consumers = show_topic_consumers(new_zk, topic)
			#print topic + "consumers are: " + str(len(consumers))

			# Deal with sole producers and sole consumers
			# Create a node for each producer and connect them to the topic
			for producer in producers:
				# If producer is ONLY producer, create the node
				if get_consumer(new_zk, producer) is None:
					p = di_graph.add_vertex()
					v_p[p] = producer
					di_graph.add_edge(p, t)

			#Create a node for each consumer and connect them to the topic
			for consumer in consumers:
				# If ONLY consumer, continue, otherwise, don't create node
				if get_producer(new_zk, consumer) is None:
					c = di_graph.add_vertex()
					v_p[c] = consumer
					di_graph.add_edge(t, c)

		#	Set the vertex properties to enable later retrieval
		di_graph.vp.string = v_p

		#
		#	Handle all the nodes which are both consumers and producers
		#
		for consumer_producer in consumer_producer_names:
			# Get the topics produced and topics consumed
			topics_produced = show_producer_topics(new_zk, consumer_producer)
			topics_consumed = show_consumer_topics(new_zk, consumer_producer)

			# Create the node
			c_p = di_graph.add_vertex()
			# Add properties for naming
			v_p[c_p] = consumer_producer

			# For all the topics produced, make a link from con_prod to topic
			for t_p in topics_produced:
				t = get_vertex(di_graph, t_p)
				di_graph.add_edge(c_p, t)

			# For all the topics consumed, make a link from the topics to con_prod
			for t_p in topics_consumed:
				t = get_vertex(di_graph, t_p)
				di_graph.add_edge(t, c_p)

		# Make the graph vertex properties internal
		di_graph.vp.string = v_p

		# Get the source nodes of the graphs and link them to root node
		unique_producers = show_unique_producers(new_zk)
		root = di_graph.add_vertex()
		v_p[root] = "/"
		for u_p in unique_producers:
			v = get_vertex(di_graph, u_p)
			di_graph.add_edge(root, v)

		# Make the graph vertex properties internal
		di_graph.vp.string = v_p
		
		return di_graph

	#
	#
	#	END OF FUNCTIONS
	#
	#

# #
# #	SCRIPT
# #
# #
# #Start the logging
# logging.basicConfig()

# #Start zookeeper client
# zk = KazooClient(hosts='127.0.0.1:2181')
# zk.start();

# #Register zookeeper listener
# zk.add_listener(my_listener)
# prods = show_all_producers(zk)

# realgraph = get_digraph(zk)
# v_p = realgraph.vp.string

# graph_draw(
# 	realgraph, 
# 	vertex_text=v_p, 
# 	vertex_font_size=12,
# 	output_size=(1000, 1000), 
# 	output="graph.png"
# 	)


# #
# #
# #	END OF SCRIPT
# #
# #
