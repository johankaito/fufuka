#from flask.templating import render_template

from app import app
from flask import Flask, request, url_for
from extended_client import extended_client
import json
from jinja2 import Environment, PackageLoader
import logging
from time import sleep

#Jinja templating environment
env = Environment(loader=PackageLoader('app','templates'))

#Start an instance of the extended_client
ext_client = extended_client('localhost:2181')

#Start zookeeper client
zk = ext_client.zk
zk.start()

#Get consumers and producers
producers = ext_client.show_all_producers(zk)
consumers = ext_client.show_all_consumers(zk)


#Get the json data and store it
json_data = ext_client.get_json(zk)
print json_data
#Function to generate json data


@app.route('/')
@app.route('/index')
def index():
	print "Index called"
	template = env.get_template('index.html')
	title = "Fufuka"
	client_url = ext_client.url_port
	#URL for the style sheet
	style_url = url_for('static', filename='styles.css')

	return template.render(page_title=title, zk_client=client_url, style_url=style_url)

@app.route('/zk')
def zk_client():
	print "Zk clients called"
	template = env.get_template('zk_client.html')
#	graph = ext_client.get_digraph(zk)

	brokers = ext_client.show_brokers_ids(zk)
	url_static = url_for('static', filename='image.png')
	#t2 = env.get_template('graph.html')

	#URL for the style sheet
	style_url = url_for('static', filename='styles.css')

	return template.render(consumers=consumers, brokers=brokers, producers=producers, image_url=url_static, style_url=style_url)

@app.route('/graph')
def test_graph():
	template = env.get_template('graph.html')
	return template.render(json_data=json_data)
