from flask import Flask
# create the application object (of class Flask) 
app = Flask(__name__)
# and then imports the views module from app package 
# THE TWO ARE NOT RELATED
from app import views
