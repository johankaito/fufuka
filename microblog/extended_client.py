#!flask/bin/python

#
#	CJMX Client information
#
# Get all messagesinpersec in brokertopic
#	<< mbeans 'kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,*' select * >>
#
#

#
#
#
#	IMPORTS
#
#
#kazoo client itself
from kazoo.client import KazooClient

#	For visualizing graph
#from graph_tool.all import *

#	logging purposes, required by zookeeper client
import logging

#	for exporting json when needed
import json
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
consumers = "/consumers"

#	Config
config = "/config"

#	Producers
producers = "/producers"

#
#	END OF GLOBAL VARIABLES
#
#
#

zk = None
#The class
class extended_client:
	"""Python class to extend client functionality when interacting with zk"""
	#
	#	FUNCTIONS
	#
	#
	def __init__(self, host, port):
		#self.name = in_name
		#Start zookeeper client
		self.port = port
		self.host=host
		self.url_port=host + ":" +str(port)
		self.zk = KazooClient(hosts=self.url_port)

		#Check if "/producers" is in zk.
		# if self.show_all_producers(zk) is None:
		# 	self.has_producers_in_zk = False
		# else:
		# 	self.has_producers_in_zk = True

	#	Listen for when the connection is:
	#	dropped, restored, or when the Zookeeper session has expired

	def get_port(self, new_zk):
		return new_zk.port

	def get_host(self, new_zk):
		return new_zk.host

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
	def get_num_brokers(self, new_zk):
		if new_zk.exists(ids):
			#Brokers exist, find how many
			return len(new_zk.get_children(ids))

	#		Get all the existing brokers
	def show_brokers_ids(self, new_zk):
		if new_zk.exists(ids):
			#Brokers exist, find how many
			return new_zk.get_children(ids)

	#		Get a given broker given id
	def get_broker(self, new_zk, new_id):
		if new_zk.exists(ids):
			#Brokers exist, find how many
			return new_zk.get(ids + "/" + str(new_id))

	#		Get the info of a given topic
	def get_topic(self, new_zk, topic):
		t = topics + "/" + str(topic)
		if new_zk.exists(t):
			return new_zk.get(t)

	#	2. 	Get the number of partitions of a given topic
	def get_num_partitions(new_zk, topic):
		partitions = topics + "/" + topic + "/partitions"
		if new_zk.exists(partitions):
			#Topic exists, get number of partitions
			return len(new_zk.get_children(partitions))

	#		Get consumers given a producer
	def show_consumers_given_producer(self, new_zk, new_producer):
		topics = self.show_topics_produced(new_zk, new_producer)
		ret = []
		for t in topics:
			con = self.show_topic_consumers(new_zk, t)
			for c in con:
				ret.append(c)
		return ret

	#		Get producers given a consumer
	def show_producers_given_consumer(self, new_zk, new_consumer):
		topics = self.show_topics_consumed(new_zk, new_consumer)
		ret = []
		for t in topics:
			prod = self.show_topic_producers(new_zk, t)
			for p in prod:
				ret.append(p)
		return ret

	#		Show topics produced
	def show_topics_produced(self, new_zk, new_producer):
		path = producers + "/" + new_producer + "/topics"
		if new_zk.exists(path):
			return new_zk.get_children(path)

	#		Show topics consumed
	def show_topics_consumed(self, new_zk, new_consumer):
		path = consumers + "/" + new_consumer + "/owners"
		if new_zk.exists(path):
			return new_zk.get_children(path)
		return None
	# 		Get the total number of messages being sent through the cluster

	#	3. 	Get number of messages per partition

	#	4. 	Get the number of consumer groups
	def get_num_all_consumers(self, new_zk):
		if new_zk.exists(consumers):
			#If directory exists
			return len(new_zk.get_children(consumers))

	#	 	Get all the consumer groups
	def show_all_consumers(self, new_zk):
		if new_zk.exists(consumers):
			#If directory exists
			#Get the consumer and make sure it has topics
			cons = new_zk.get_children(consumers)
			to_return = []
			for c in cons:
				if self.show_topics_consumed(new_zk, c) is not None:
					to_return.append(c)

			return to_return


	#		Get a particular consumer
	def get_consumer(self, new_zk, new_consumer):
		path = consumers + "/" + new_consumer
		if new_zk.exists(path):
			return new_zk.get(path)
		return None
	#	5. 	Get the number of producers
	def get_num_producers(self, new_zk):
		if new_zk.exists(producers):
			#If directory exists
			return len(new_zk.get_children(producers))

	#	 	Get all the producers
	def show_all_producers(self, new_zk):
		#print "In show all producers"
		if new_zk.exists(producers):
			#print "Inside the if statement"
			#If directory exists
			return new_zk.get_children(producers)
		return None

	#		Get a particular producer
	def get_producer(new_zk, new_producer):
		path = producers + "/" + new_producer
		if new_zk.exists(path):
			return new_zk.get(path)
		return None

	#	6. 	Get the number of replicas of a given topic

	# 	7. 	Get the topic listened to by a given consumer group
	def show_consumer_topics(self, new_zk, new_group):
		path = consumers + "/" + new_group + "/owners"
		#print "Getting topics for: " + new_group
		if new_zk.exists(path):
			return new_zk.get_children(path)

	# 	8. 	Show the topic(s) posted by a given producer
	def show_producer_topics(self, new_zk, new_producer):
		path = producers + "/" + new_producer + "/topics" 
		if new_zk.exists(path):
			return new_zk.get_children(path)

	# 		Get number of topics in a given group
	def get_num_topics(new_zk, new_group):
		this_group_topics = consumers + "/" + new_group + "/owners"
		if new_zk.exists(this_group_topics):
			return len(new_zk.get_children(this_group_topics))

	#		Get the total number of topics
	def get_total_num_topics(new_zk):
		if new_zk.exists(topics):
			return len(new_zk.get_children(topics))

	#		Get all the available topics
	def show_all_topics(self, new_zk):
		#print "in show all topics"
		#print "ZK is: " + str(new_zk)
		if new_zk.exists(topics):
			#print "topics exist"
			#for t in new_zk.get_children(topics):
				#print "In show_all_topics: " + t
			return new_zk.get_children(topics)

	#		Show topic consumer
	def show_topic_consumers(self, new_zk, new_topic):
		to_return = []
		if self.get_topic(new_zk, new_topic) is not None:
			#Topic exists
			#Get all the consumers 
			cons = self.show_all_consumers(new_zk)
			for con in cons:
				#For each consumer, get all its topics
				topics = self.show_consumer_topics(new_zk, con)
				for topic in topics:
					#For all the topics in this consumer
					#Check if the given topic is in there
					if topic == new_topic:
						#If it is, append it
						to_return.append(con)
		return to_return

	#		Show topic producer
	def show_topic_producers(self, new_zk, new_topic):
		to_return = []
		if self.get_topic(new_zk, new_topic) is not None:
			#Topic exists
			#Get all the producers
			prods = self.show_all_producers(new_zk)
			for prod in prods:
				#For each producer, get all its topics
				topics = self.show_producer_topics(new_zk, prod)
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
	def show_consumer_producers(self, new_zk):
		prods = self.show_all_producers(new_zk)

		#	Check if producers actually exist in zk 
		if prods is None:
			return None

		con_prod = []
		for producer in prods:
			if self.get_consumer(new_zk, producer) is not None:
				con_prod.append(producer)
		return con_prod

	#		Show unique producers. Producers who are only producers
	def show_unique_producers(self, new_zk):
		prods = self.show_all_producers(new_zk)
		con_prods = self.show_consumer_producers(new_zk)

		#	Check if producers actually exist in zk 
		if prods is None:
			return None

		for con_prod in con_prods:
			prods.remove(con_prod)

		return prods

	#		Show unique consumers. Consumers who are only consuemrs
	def show_unique_consumers(self, new_zk):
		cons = self.show_all_consumers(new_zk)
		con_prods = self.show_consumer_producers(new_zk)

		for con_prod in con_prods:
			cons.remove(con_prod)

		return cons
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
			prods = show_topic_producers(new_zk, topic)
			#print topic + "producers are : " + str(len(producers))
			cons = show_topic_consumers(new_zk, topic)
			#print topic + "consumers are: " + str(len(consumers))

			# Deal with sole producers and sole consumers
			# Create a node for each producer and connect them to the topic
			for producer in prods:
				# If producer is ONLY producer, create the node
				if get_consumer(new_zk, producer) is None:
					p = di_graph.add_vertex()
					v_p[p] = producer
					di_graph.add_edge(p, t)

			#Create a node for each consumer and connect them to the topic
			for consumer in cons:
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

	#Get the graph data in form of json
	def get_json(self, new_zk):
		mega_data = []
		#data['key'] = 'value'

		prods = self.show_all_producers(new_zk)
		cons = self.show_all_consumers(new_zk)
		#Generate the data to pass to the sketching graph

		#Check For cases where the producers aren't available
		if prods is not None:
			#	Producers are in zk, go ahead
			for p in prods:
				topics = self.show_producer_topics(new_zk,p)
				for t in topics:
					data = {}
					data['source'] = p
					data['target'] = t
					#data['type'] = 'producer'
					mega_data.append(data)

			#Connect all to a source root node
			for p0 in self.show_unique_producers(new_zk):
				data = {}
				data['source'] = 'root'
				data['target'] = p0
				data['type'] = 'root'
				mega_data.append(data)

		for c in cons:
			topics = self.show_consumer_topics(new_zk,c)
			#print "COnsumer: " + c
			for t in topics:
				#print "Topic: " + t
				data = {}
				data['source'] = t
				data['target'] = c
				#data['type'] = 'topic'
				mega_data.append(data)

		#Connect all to a source root node
		for t in self.show_all_topics(new_zk):
			data = {}
			data['source'] = 'root'
			data['target'] = t
			data['type'] = 'root'
			mega_data.append(data)

		return mega_data


	# #Get the graph data in form of json
	# def get_json(self, new_zk):
	# 	mega_data = []
	# 	#data['key'] = 'value'

	# 	up = self.show_unique_producers(new_zk)
	# 	uc = self.show_unique_consumers(new_zk)
	# 	cp = self.show_consumer_producers(new_zk)
	# 	#Generate the data to pass to the sketching graph
	# 	for p in up:
	# 		topics = self.show_producer_topics(new_zk,p)
	# 		#print "Producers: " + p
	# 		for t in topics:
	# 			data = {}
	# 			data['source'] = p
	# 			data['target'] = t
	# 			data['type'] = 'producer'
	# 			mega_data.append(data)

	# 	for c in uc:
	# 		#print "Consuemrs: " + c
	# 		topics = self.show_consumer_topics(new_zk,c)
	# 		for t in topics:
	# 			data = {}
	# 			data['source'] = t
	# 			data['target'] = c
	# 			data['type'] = 'topic'
	# 			mega_data.append(data)

		
	# 	for i in cp:
	# 		#CP as a consumer
	# 		#print "Consuemr producers: " + i
	# 		topics = self.show_consumer_topics(new_zk,i)
	# 		for t in topics:
	# 			data = {}
	# 			data['source'] = t
	# 			data['target'] = i
	# 			data['type'] = 'topic'
	# 			mega_data.append(data)

	# 		#CP as a producer
	# 		topics = self.show_producer_topics(new_zk,i)
	# 		for t in topics:
	# 			data = {}
	# 			data['source'] = i
	# 			data['target'] = t
	# 			data['type'] = 'consumer-producer'
	# 			mega_data.append(data)


	# 	#Connect all to a source root node
	# 	for p0 in up:
	# 		data = {}
	# 		data['source'] = 'root'
	# 		data['target'] = p0
	# 		data['type'] = 'root'
	# 		mega_data.append(data)

	# 	return json.dumps(mega_data)

	#Get the graph nodes in form of json
	def get_nodes_json(self, new_zk):
		mega_data = []
		#data['key'] = 'value'

		uni_prod = self.show_unique_producers(new_zk)

		if uni_prod is not None:
			#	Producers are in zk, go ahead
			con_prod = self.show_consumer_producers(new_zk)
			uni_cons = self.show_unique_consumers(new_zk)

			#	Consumer producers
			for cp in con_prod:	
				data = {}
				data['name'] = cp
				data['type'] = 'consumer_producer'
				
				#Get the nodes where cp produces to and consumers from
				prods = self.show_producers_given_consumer(new_zk, cp)
				cons = self.show_consumers_given_producer(new_zk, cp)
				w = len(cons) + len(prods)
				data['weight'] = w
				data['poststo'] = cons
				data['getsfrom'] = prods
				mega_data.append(data)

			#	Unique consumers
			for uc in uni_cons:
				data = {}
				data['name'] = uc
				data['type'] = 'consumer'
				
				#Show the producers to this consumer
				prods = self.show_producers_given_consumer(new_zk, uc)
				w = len(prods)
				data['weight'] = w
				data['getsfrom'] = prods
				mega_data.append(data)

			# 	Unique producers
			for up in self.show_unique_producers(new_zk):
				data = {}
				data['name'] = up
				data['type'] = 'producer'
				
				#Get the consumers this producer produces to
				cons = self.show_consumers_given_producer(new_zk, up)
				w = len(cons)
				data['weight'] = w
				data['poststo'] = cons
				mega_data.append(data)

			# 	Topics
			for t in self.show_all_topics(new_zk):
				data = {}
				data['name'] = t
				data['type'] = 'topic'
				w = len(self.show_topic_consumers(new_zk, t)) + len(self.show_topic_producers(new_zk, t))
				data['weight'] = w
				mega_data.append(data)

			#	Root node
			data = {}
			data['name'] = 'root'
			data['type'] = 'root'
			w = len(self.show_unique_producers(new_zk))
			data['weight'] = w
			data['zkhost'] = self.host
			data['zkport'] = self.port
			mega_data.append(data)

		else:
			#	No producers in zk
			cons = self.show_all_consumers(new_zk)

			#	Create all consumer nodes
			for c in cons:
				data = {}
				data['name'] = c
				data['type'] = 'consumer'
				
				#Show topics consumed
				tops = self.show_topics_consumed(new_zk, c)
				w = len(tops)
				data['weight'] = w
				data['getsfrom'] = tops
				mega_data.append(data)

			# 	Create all Topic nodes
			for t in self.show_all_topics(new_zk):
				data = {}
				data['name'] = t
				data['type'] = 'topic'
				w = len(self.show_topic_consumers(new_zk, t))
				data['weight'] = w
				mega_data.append(data)

			#	Root node
			data = {}
			data['name'] = 'root'
			data['type'] = 'root'
			w = len(self.show_all_topics(new_zk))
			data['weight'] = w
			data['zkhost'] = self.host
			data['zkport'] = self.port
			mega_data.append(data)


		return mega_data

	#Get the graph nodes in form of json
	def get_edges_json(self, new_zk):
		mega_data = []
		#data['key'] = 'value'

		prods = self.show_all_producers(new_zk)
		cons = self.show_all_consumers(new_zk)
		#Generate the data to pass to the sketching graph
		if prods is not None:
			# Producers are available
			# Get all the amazing data
			for p in prods:
				topics = self.show_producer_topics(new_zk,p)
				for t in topics:
					data = {}
					data['source'] = p
					data['target'] = t
					data['weight'] = 1;
					mega_data.append(data)

			for c in cons:
				topics = self.show_consumer_topics(new_zk,c)
				for t in topics:
					data = {}
					data['source'] = t
					data['target'] = c
					data['weight'] = 1;
					mega_data.append(data)

			#Connect all to a source root node
			for p0 in self.show_unique_producers(new_zk):
				data = {}
				data['source'] = 'root'
				data['target'] = p0
				data['weight'] = 1;
				mega_data.append(data)

		else:
			# Producer information not available
			# only use the consumers and topics
			for c in cons:
				topics = self.show_consumer_topics(new_zk,c)
				for t in topics:
					data = {}
					data['source'] = t
					data['target'] = c
					data['weight'] = 1;
					mega_data.append(data)

		return mega_data

		#`	Get the largest weight
	def get_largest_weight(self, new_zk):
		a = self.get_node_with_largest_weight(new_zk)["weight"]
		#print "Largest: " + str(a)
		return a

	#`	Get the smallest weight
	def get_smallest_weight(self, new_zk):
		a = self.get_node_with_smallest_weight(new_zk)["weight"]
		#print "Smallest: " + str(a)
		return a

	#	Get the node with the largest weight
	def get_node_with_largest_weight(self, new_zk):
		nodes = self.get_nodes_json(new_zk)
		w = 0
		largest_node = None

		for n in nodes:
			if n['weight'] > w:
				w = n['weight']
				largest_node = n
		#print "Largest node: " + str(largest_node)
		return largest_node

	#	Get the node with the smallest weight
	def get_node_with_smallest_weight(self, new_zk):
		nodes = self.get_nodes_json(new_zk)
		w = 1000000
		smallest_node = None

		for n in nodes:
			if n['weight'] < w:
				w = n['weight']
				smallest_node = n

		return smallest_node

	#	Returns the average offset for a particular consumer
	def get_consumer_offset(self, new_zk, consumer, topic):
		var = consumers + "/" + consumer + "/offsets/" + topic + "/0"
		if new_zk.exists(var):
			payload = str(new_zk.get(var))
			#print payload
			deli = '\''
			
			beg = payload.index(deli) + 1
			#print "beg: " + str(beg)
			end = payload.index(deli, beg)
			#print "end: " + str(end)
			offset = payload[beg:end]

			return int(offset)
		return None
	
	def get_accumulated_topic_offset(self, new_zk, topic):
		con = self.show_topic_consumers(new_zk, topic)
		accumulated_offset = 0
		for c in con:
			offset = int(self.get_consumer_offset(new_zk, c, topic))
			accumulated_offset = accumulated_offset + offset
		return accumulated_offset
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
logging.basicConfig()

#print "instantiating the class"
#eC = extended_client('localhost:2181')

#Start an instance of the extended_client
ext_client = extended_client('localhost',2181)

#Start zookeeper client
zk = ext_client.zk
zk.start()

#Get broker information
broker_ids = ext_client.show_brokers_ids(zk)
offset = ext_client.get_consumer_offset(zk, "node4", "t1")
#print "Offset is: " + str(offset)

#for bi in broker_ids:
	#print ext_client.get_broker(zk, bi)
#print show
# #Register zookeeper listener
# zk.add_listener(my_listener)
# prods = show_all_producers(zk)

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
