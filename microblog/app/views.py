#from flask.templating import render_template
#	Also installed redis
from app import app
from flask import Flask, request, url_for, Response, redirect
from extended_client import extended_client
import json
from jinja2 import Environment, PackageLoader
import logging
from time import sleep

#To access JMX Rest api
import requests

#To allow calling of sh commands from python
import commands

#Threading purposes
import threading

#For async tasks
from celery import Celery

#For doing msg_out rate calculations
import math

#For the timing of things
import datetime

#messages_in_topic_per_second = 'java -cp $JAVA_HOME/lib/tools.jar:../target/scala-2.10/cjmx.jar cjmx.Main 3628 \"mbeans \'kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,*\' select *\"'
#For getting the process id of kafka
#import os
#PIDs = os.system("ps aux | grep \"kafka.Kafka\" | grep -v grep | awk '{print $2}'")

#For getting ipaddress 
import socket
ip = socket.gethostbyname(socket.gethostname()) + ""
host = {}
host["ip"] = ip


#Jinja templating
env = Environment(loader=PackageLoader('app','templates'))

ext_client=None
json_data=None
json_nodes=None
zk=None
json_topics=None
remote_server = {}
remote_server["host"]= "John"
local = "local"
remote = "remote"
#CSS File
#reading_from={}
reading_from=""

#Store the offsets for each topic all consumers consume from
#Objects for keeping track of rates for CONSUMERS
prev_consumer_info = {}
prev_consumer_counts = {}

#Store the accumulated offset
accumulated_topic_rates = {}

consumers = ""

#Stores information for msgs_out
second_counter = 0
seconds_in_a_day = 86400 #(60*60*24)

#Objects for keeping track of rates for TOPICS
topic_sums = {}
prev_topic_info = {}
prev_topic_counts = {}

#Proxy server 
proxy = None


#reading_from["data"] = None
#
#
#	FUNCTIONS
#
#

#	The thing that the user sees
@app.route('/')
@app.route('/index')
def index():
	print "Index called"
	template = env.get_template('index.html')
	title = "Fufuka"
	client_url = ""#ext_client.url_port

	return template.render(page_title=title, zk_client=client_url)

#	Gets all the form data from the "Start visualization page"
@app.route('/', methods=['POST'])
def index_return_values():
	print "/ with data. Form received"
	start = datetime.datetime.now()
	#hostname = request.local
	dictionary = request.form
	print "Dict: " + str(dictionary) + " :" + str(len(dictionary))
	#print list(v for k,v in dictionary.iteritems() if 'jmx' in k) 
	if len(dictionary) > 1:
		#Dealing with a remote connection
		print "Remotely"
		global reading_from
		#reading_from["data"] = str(remote)
		reading_from = str(remote)
		hostname = request.form.get("hostname", None)
		zkhostnamePort = request.form.get("zkhostnameport", None)
		proxy = request.form.get("proxy", None)

		print "Connecting to: " + hostname
		print "With zk at: " + zkhostnamePort
		global proxy
		print "Proxy: " + proxy
		global hostandport

		#Set the remote host
		remote_server["host"] = str(hostname)

		#Set all the JMX ports that need to be listened to
		jmx_ports = list(v for k,v in dictionary.iteritems() if 'jmx' in k)
		remote_server["ports"] = []
		for port in jmx_ports:
			print "JMX ports: " + str(port)
			remote_server["ports"].append(str(port))

	else:
		#Dealing with a local connection
		global reading_from
		#reading_from["data"] = str(local)
		reading_from = str(local)
		print "Local"
		zkhostnamePort = request.form.get("zkhostnameport", None)
		print "Connecting to: " + zkhostnamePort

	# Process data for getting to zk instance
	#
	#
	split = zkhostnamePort.index(':')
	hostname = zkhostnamePort[:split]
	port = int(zkhostnamePort[split+1:])

	#Start an instance of the extended_client
	global ext_client
	ext_client = extended_client(hostname, port)

	#Start zookeeper client
	global zk
	zk = ext_client.zk
	zk.start()

	#Once the returned values are found, set them all
	#Get consumers and producers

	topics = ext_client.show_all_topics(zk)

	#Populate topic holder
	for t in topics:
		topic_sums[t] = 0
		prev_topic_info[t] = {}
		prev_topic_counts[t] = []

	global json_topics
	json_topics = json.dumps(topics)

	#Get the json data and store it
	global json_data
	json_data = json.dumps(ext_client.get_json(zk))
	
	global json_nodes
	json_nodes = json.dumps(ext_client.get_nodes_json(zk))
	json_edges = json.dumps(ext_client.get_edges_json(zk))

	end = datetime.datetime.now()
	print "Total time to load zk information: " + str(end-start)
	return redirect("/zk")

#	Main viewing area for zks
@app.route('/zk')
def zk_client():
	print "/zk called"

	#Set the consumers then continously calculate their offsets
	print "Creating consumer holders:"
	start_time = datetime.datetime.now()
	global consumers
	consumers = ext_client.show_all_consumers(zk)
	#Populate consumer holders
	for c in consumers:
		prev_consumer_info[c] = {}
		prev_consumer_counts[c] = []

	for c in consumers:
		topics = ext_client.show_topics_consumed(zk, c)
		for t in topics:
			prev_consumer_info[c][t] = {}
			#print prev_consumer_info
	end_time = datetime.datetime.now()

	calculate_offsets()

	#Set the template of the page
	template = env.get_template('zk_client.html')
	#brokers = ext_client.show_brokers_ids(zk)

	#Get the information of the current zookeeper instance
	data = {}
	data["zkinfo"] = str(ext_client.url_port)

	print "Total con: " + str(len(consumers))
	print "Total time to load /zk page: " + str(end_time-start_time)
	return template.render(data=data)#consumers=consumers, brokers=brokers, producers=producers, topics=topics)#, r=r.content)

#	Loads the d3 graph onto the iframe
@app.route('/test')
def test_2():
	print "/test called"
	start = datetime.datetime.now()
	template = env.get_template('test2_graph.html')
	js_url = url_for('static', filename='js/loadGraph.js')
	# graph={}
	# graph["nodes"] = json_nodes
	# graph["edges"] = json_edges
	data = {}
	data["json_data"] = json_data
	data["json_nodes"] = json_nodes
	data["json_topics"] = json_topics
	data["js_url"] = js_url
	data["host"] = host
	data["remote_server"] = remote_server
	data["reading_from"] = reading_from
	data["largest_weight"] = ext_client.get_largest_weight(zk)
	data["smallest_weight"] = ext_client.get_smallest_weight(zk)
	data["proxy"] = proxy
	sendData = json.dumps(data)
	# print "---------------------------"
	# print "---------------------------"
	# print "---------------------------"
	end = datetime.datetime.now()
	print "Total time to load /test page: " + str(end-start)
	#print data
	return template.render(data=sendData)#json_data=json_data, json_nodes=json_nodes, json_topics=json_topics, js_url=js_url, host=host, remote_server=remote_server, readingFrom=reading_from)

#	Method to return offset rates
def get_rate(rate_type, prevData):
	one_minute = 60
	if rate_type == "minute":
		#Get the minute rate
		if len(prevData) > one_minute:
			#print " Min rate "
			#print "L: " + str(prevData[second_counter+1]) + " S: " + str(prevData[second_counter-one_minute])
			#min_rate = abs(prevData[second_counter+1] - prevData[second_counter-one_minute])
			min_rate = abs(prevData[second_counter] - prevData[second_counter-one_minute])/(one_minute + 0.0)
			return min_rate
		else:
			min_rate = 0
			return min_rate

	if rate_type == "mean":
		#Get the mean rate
		global second_counter
		if second_counter > 0:
			#print " Mean rate"
			#Method 1
			#global predata_sum
			#mean_rate = predata_sum/(second_counter+0.0)
			
			#Method 2
			# print "L: " + str(prevData[second_counter+1]) + " S: " + str(prevData[0])
			# mean_rate = abs(prevData[second_counter+1] - prevData[0])/(second_counter+0.0)

			#Method 3
			# print " ArrLen: " + str(len(prevData))
			# print " SC: " + str(second_counter)
			# print " L: " + str(prevData[second_counter])+ " S: " + str(prevData[0])
			mean_rate = abs(prevData[second_counter] - prevData[0])/(second_counter+0.0)
			#print " MeanR " + str(mean_rate)
			return mean_rate

		else:
			mean_rate = -1
			return mean_rate


# 	Threaded method which calculates the offsets
def calculate_offsets():
	#Get individual offsets of a consumer
	for c in consumers:
		global prev_consumer_info
		#prev_consumer_info[c] = {}
		topics = ext_client.show_topics_consumed(zk, c)
		for t in topics:
			#
			#
			#	Consumer Rates
			#
			#
			# Get the offsets for every consumer and correpsonding topic
			offset = ext_client.get_consumer_offset(zk, c, t)

			#Append count to the array holder
			prev_consumer_counts[c].append(offset)

			#Get the msg_out_minute_rate for this topic
			min_rate = get_rate("minute", prev_consumer_counts[c])
			#print "Min: " + str(min_rate)
			mean_rate = get_rate("mean", prev_consumer_counts[c])
			#print "Mean: " + str(mean_rate)

			if mean_rate == -1:
				mean_rate = 0
			#Update the holder for this topic
			global prev_consumer_info
			prev_consumer_info[c][t]["count"] = offset
			prev_consumer_info[c][t]["min_rate"] = min_rate
			prev_consumer_info[c][t]["mean_rate"] = mean_rate

			#
			#
			#	Topic rates
			#
			#
			#Get the count for this topic
			count = ext_client.get_accumulated_topic_offset(zk, t)

			#Update the sum for this topic
			topic_sums[t] = topic_sums[t] + count

			#Append count to the array holder
			prev_topic_counts[t].append(count)

			#Get the msg_out_minute_rate for this topic
			min_rate = get_rate("minute", prev_topic_counts[t])
			mean_rate = get_rate("mean", prev_topic_counts[t])

			if mean_rate == -1:
				mean_rate = 0
			#Update the holder for this topic
			global prev_topic_info
			prev_topic_info[t]["count"] = count
			prev_topic_info[t]["min_rate"] = min_rate
			prev_topic_info[t]["mean_rate"] = mean_rate

	global second_counter
	second_counter = second_counter + 1
	
	#Reset the rate calculations every 24hrs
	if second_counter == seconds_in_a_day:
		second_counter = 0

	threading.Timer(1, calculate_offsets).start()

#	Returns the consumer offsets
@app.route('/getconsumerrates')
def get_consumer_offsets():
	return json.dumps(prev_consumer_info)

#	Returns the accumulated offsets for each topic
@app.route('/getaccumulatedrates')
def get_accumulated_offsets():
	return json.dumps(prev_topic_info)


#	Takes care of the currently selected node
@app.route('/current_node')
def draw_node():
	print "Draw node called"
	template = env.get_template('node.html')
	return template.render(json_data=json_data)

@app.route('/orgraph')
def or_graph():
	template = env.get_template('orgraph.html')
	return template.render(json_data=json_data)
