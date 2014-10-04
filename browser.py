# all the imports
import json

from pymongo import MongoClient

from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify

DB_URL = "mongodb://localhost:27017"

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    
    # returns a pymongo db instance    
    client = MongoClient(DB_URL)
    return client

@app.route('/')
def hello():
    return render_template('index.html')

@app.before_request
def before_request():
    g.db = connect_db()

#@app.teardown_request
#def teardown_request(exception):
    # closes the db instance coneection if needed
#    return

@app.route('/message/send', methods=['POST'])
def logSentMessage():
	message = request.form['message']
	sendFrom = request.form['contactFrom']
	sendTo = request.form['contactTo']
	return jsonify(**{
		"score": 0,
		"jarSum": 0
		})

@app.route('/message/receieve', methods=['POST'])
def logReceiveMessage():
	message = request.form['message']
	sendFrom = request.form['contactFrom']
	sendTo = request.form['contactTo']
	return jsonify(**{
		"success": 0
		})

@app.route('/score', methods=['GET'])
def getScore():
	return jsonify(**{"score": 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
