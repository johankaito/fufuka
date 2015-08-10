#from flask.templating import render_template
#	Also installed redis
from app import app
from flask import Flask, request, url_for, Response
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

#Start an instance of the extended_client
ext_client = extended_client('localhost', 2181)

#Start zookeeper client
zk = ext_client.zk
zk.start()

#Get consumers and producers
producers = ext_client.show_all_producers(zk)
consumers = ext_client.show_all_consumers(zk)
topics = ext_client.show_all_topics(zk)
json_topics = json.dumps(topics)
#print "number ot topics: " + str(len(topics))

#Get the json data and store it
json_data = ext_client.get_json(zk)
json_nodes = ext_client.get_nodes_json(zk)
json_edges = ext_client.get_edges_json(zk)

r=""

#CSS File

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
	client_url = ext_client.url_port
	#URL for the style sheet
	#style_url = url_for('static', filename='styles.css')

	return template.render(page_title=title, zk_client=client_url)

@app.route('/zk')
def zk_client():
	print "/zk called"
	template = env.get_template('zk_client.html')
	brokers = ext_client.show_brokers_ids(zk)

	#get_topics_jmx();

	
	# #URL for the style sheet
	# style_url = url_for('static', filename='styles.css')
		# call method again in 5 seconds
	return template.render(host=host)#consumers=consumers, brokers=brokers, producers=producers, topics=topics)#, r=r.content)

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
	return template.render(json_data=json_data, json_nodes=json_nodes, json_topics=json_topics, js_url=js_url, host=host)
