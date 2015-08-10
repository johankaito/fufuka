#!flask/venv/bin/python

#Used to get the ip address for run purposes
import socket
from app import app
# Reload the page whenever code changes
# app.run(debug=False)
# Set the port where application should run
ip = socket.gethostbyname(socket.gethostname());
print "Run: Host is="+ip 

app.run(
	debug=True,
	#host="10.15.100.202",
	#host="192.168.1.105",
	host=ip,
	port=9990
	)