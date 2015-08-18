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
#reading_from["data"] = None
#
#
#	FUNCTIONS
#
#

@app.route('/')
@app.route('/index')
def index():
	print "Index called"
	template = env.get_template('index.html')
	title = "Fufuka"
	client_url = ""#ext_client.url_port

	return template.render(page_title=title, zk_client=client_url)

@app.route('/', methods=['POST'])
def index_return_values():
	print "Index_return_values called"
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
		print "Connecting to: " + hostname
		print "With zk at: " + zkhostnamePort
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
	producers = ext_client.show_all_producers(zk)
	consumers = ext_client.show_all_consumers(zk)
	topics = ext_client.show_all_topics(zk)

	global json_topics
	json_topics = json.dumps(topics)

	#Get the json data and store it
	global json_data
	json_data = json.dumps(ext_client.get_json(zk))
	
	global json_nodes
	json_nodes = json.dumps(ext_client.get_nodes_json(zk))
	json_edges = json.dumps(ext_client.get_edges_json(zk))

	return redirect("/zk")

@app.route('/zk')
def zk_client():
	print "/zk called"
	template = env.get_template('zk_client.html')
	brokers = ext_client.show_brokers_ids(zk)

	#Get the information of the current zookeeper instance
	data = {}
	
	data["zkinfo"] = str(ext_client.url_port)
	return template.render(data=data)#consumers=consumers, brokers=brokers, producers=producers, topics=topics)#, r=r.content)

#	Takes care of the graph that shows up
@app.route('/graph')
def draw_graph():
	print "/graph"
	template = env.get_template('graph.html')
	#print json_data
	return template.render(json_data=json_data)

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

@app.route('/test')
def test_2():
	print "/test called"
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
	sendData = json.dumps(data)
	# print "---------------------------"
	# print "---------------------------"
	# print "---------------------------"

	#print data
	return template.render(data=sendData)#json_data=json_data, json_nodes=json_nodes, json_topics=json_topics, js_url=js_url, host=host, remote_server=remote_server, readingFrom=reading_from)
