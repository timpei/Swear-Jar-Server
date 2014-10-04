# all the imports
import json
import time
import swears
from pymongo import MongoClient

from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify


DB_URL = "mongodb://localhost:27017"
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)
client = MongoClient(DB_URL)

@app.route('/')
def hello():
    return render_template('index.html')

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

def getMemberName(number):

    members_collection = g.db.member_numbers
    name = members_collection.find_one({"number": number})
    
    return name

@app.route('/message/send', methods=['POST'])
def logSentMessage():
    message = request.form['message']
    fromNumber = request.form['number']
    toNumber = request.form['contact_number']

    messages_collection = g.db.messages
    jars_collection = g.db.jars

    words = message.split(" ")
    score = 0
    swearWords = []
    cur_time = int(time.time())

    # Compute swear score
    for word in words:
        score += getSwearScore(trimWord(word))
        if score > 0:
            swearWords.append(word)

    if len(swearWords) != 0:
        # count freq
        word_freq_collection = g.db.word_frequency
        word_freq = word_freq_collection.find_one({"fromNumber": fromNumber})
        
        # Store in the per user word table - WHAT do you say
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

        #FromUser freq - WHO are you swearing at?
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

        toName = getMemberName(toNumber)

    # Update the master table
    messages_collection.insert({
        "reference_number": fromNumber,
        "swear_words": swearWords, 
        "score": score,
        "text": message,
        "time": cur_time,
        "toName": toName,
        "toNumber": toNumber
        });

    # Compute and store the new value of the swear jar
    cur_jar = jars_collection.find_one({"fromNumber": fromNumber})
    if cur_jar is None:
        jars_collection.insert({
            "fromNumber": fromNumber, 
            "sum": score
            })

        finalSum = score

    else:
        finalSum = cur_jar['sum'] + score
        jars_collection.update({"fromNumber": fromNumber}, {"$set": {"sum": finalSum}})

    return jsonify(**{
        "score": score,
        "jarSum": finalSum
        })

@app.route('/message/receive', methods=['POST'])
def logReceiveMessage():
    message = request.form['message']
    toNumber = request.form['number']
    fromNumber = request.form['contact_number']

    messages_collection = g.db.messages
    jars_collection = g.db.jars

    words = message.split(" ")
    score = 0
    swearWords = []
    cur_time = int(time.time())
    exitCode = 0 # Modify the exit code accordingly

    for word in words:
        score += getSwearScore(trimWord(word))
        if score > 0:
            swearWords.append(word)

    if len(swearWords) != 0:

        #ToUser freq - Who swears at you?
        #Todo: might need to catch error where member does not exist
        to_member_collection = g.db.to_member_freq
        member_freq = to_member_collection.find_one({"toNumber": toNumber})
        if member_freq is None:
            from_member_collection.insert({
                "toNumber": toNumber, 
                "freq": len(swearWords)
                })
        else:
            from_member_collection.update({"toNumber": toNumber}, {"$set": {"freq": member_freq['freq'] + len(swearWords)}})

        toName = getMemberName(toNumber)

    # Update the master table
    messages_colection.insert({
        "reference_number": toNumber,
        "swear_words": swearWords, 
        "score": score,
        "text": message,
        "time": cur_time,
        "toName": toName, # ERROR HERE, we need the name from registration table
        "toNumber": toNumber
        });

    return jsonify(**{
        "success": exitCode
        })

@app.route('/score/<int:number>', methods=['GET'])
def getScore(number):
    return jsonify(**{"score": 0})

@app.route('/register', methods=['PUT'])
def register():
    newNumber = request.form["number"]
    newName = request.form["name"]
    facebookId = request.form["facebook_id"]

    members_collection = g.db.member_numbers
    exitCode = 0

    # Add the member to the members table
    members_collection.insert({
        "number": newNumber,
        "name": newName,
        "facebook_id": facebookId
        })

    return jsonify(**{
        "success": exitCode 
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0')
