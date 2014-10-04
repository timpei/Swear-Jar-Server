# all the imports
import json
import time
import dbconf
from pymongo import MongoClient

from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify


DB_URL = "mongodb://localhost:27017"
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
client = MongoClient(DB_URL)

@app.before_request
def before_request():
    g.db = client.swear_jar

#@app.teardown_request
#def teardown_request(exception):
    # closes the db instance coneection if needed
#    return

def getSwearScore(word):
	return 0

def trimWord(word):
	return word.lower().strip('.,!?:"\'')

@app.route('/message/send', methods=['POST'])
def logSentMessage():
	message = request.form['message']
	fromNumber = request.form['number']
	toName = request.form['contact_name']
	toNumber = request.form['contact_number']

	messages_colection = g.db.messages
	jars_collection = g.db.jars

	words = message.split(" ")
	score = 0
	swearWords = []
	cur_time = int(time.time())

	for word in words:
		score += getSwearScore(trimWord(word))
		if score > 0:
			swearWords.append(word)

	if len(swearWords) != 0:
		# count freq
		word_freq_collection = g.db.word_frequency
		word_freq = word_freq_collection.find_one({"fromNumber": fromNumber})
		if word_freq is None:
			word_freq = {"fromNumber": fromNumber, "freq": []}
			for word in swearWords:
				word_freq['freq'][word] = word_freq.get(word, 0) + 1
			word_freq_collection.insert({
				"fromNumber": fromNumber, 
				"freq": word_freq
				})
		else:
			for word in swearWords:
				word_freq['freq'][word] = word_freq.get(word, 0) + 1
			word_freq_collection.update({"fromNumber": fromNumber}, {"$set": {"freq": word_freq['freq']}})

		#memberToMember freq
		#Todo: might need to catch error where member does not exist
		from_member_collection = g.db.from_member_freq
		member_freq = from_member_collection.find_one({"fromNumber": fromNumber})
		if member_freq is None:
			from_member_collection.insert({
				"fromNumber": fromNumber, 
				"freq": len(swearWords)
				})
		else:
			from_member_collection.update({"fromNumber": fromNumber}, {"$set": {"freq": member_freq['freq'] + len(swearWords)}})

	messages_colection.insert({
		"reference_number": fromNumber,
		"swear_words": swearWords, 
		"score": score,
		"text": message,
		"time": cur_time,
		"toName": toName,
		"toNumber": toNumber
		});

	cur_jar = jars_collection.find_one({"fromNumber": fromNumber})
	if cur_jar is None:
		jars_collection.insert({
			"fromNumber": fromNumber, 
			"sum": score
			})
	else:
		jars_collection.update({"fromNumber": fromNumber}, {"$set": {"sum": cur_jar['sum'] + score}})

	return jsonify(**{
		"score": score,
		"jarSum": cur_jar['sum'] + score
		})

@app.route('/message/receieve', methods=['POST'])
def logReceiveMessage():
	message = request.form['message']
	sendFrom = request.form['contactFrom']
	sendTo = request.form['contactTo']
	return jsonify(**{
		"success": 0
		})

@app.route('/score/<int:number>', methods=['GET'])
def getScore(number):
	return jsonify(**{"score": 0})


if __name__ == '__main__':
    app.run(host='0.0.0.0')
