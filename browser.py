# all the imports
import json
import os
import time
import swears
from pymongo import MongoClient

from flask import Flask, request, Response, session, g, redirect, url_for, abort, render_template, flash, jsonify

DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_URL = "mongodb://%s:%s@ds043220.mongolab.com:43220/swearjar" % (DB_USER, DB_PASS)
#DB_URL = "mongodb://localhost:27017"
DEBUG = True

EXPLICIT = False

app = Flask(__name__)
app.config.from_object(__name__)
client = MongoClient(DB_URL)

@app.route('/')
def hello():
    return render_template('index.html')

@app.before_request
def before_request():
    g.db = client.swearjar

#@app.teardown_request
#def teardown_request(exception):
    # closes the db instance coneection if needed
#    return

def getSwearScore(word):
    if EXPLICIT: 
        if word in swears.swearList:
            return swears.swearList[word]
        else:
            return 0
    else:
        if word in swears.cleanSwearList:
            return swears.cleanSwearList[word]
        else:
            return 0

def trimWord(word):
    return word.lower().strip('.,!?:"\'')

def getMemberName(number):

    members_collection = g.db.member_numbers
    member = members_collection.find_one({"number": number})
    if member is None:
        return number
    else:
        return member["name"]

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
        if getSwearScore(trimWord(word)) > 0:
            score += getSwearScore(trimWord(word))
            swearWords.append(trimWord(word))

    if len(swearWords) != 0:
        # count freq
        word_freq_collection = g.db.word_frequency
        word_freq = word_freq_collection.find_one({"fromNumber": fromNumber})
        
        # Store in the per user word table - WHAT do you say
        if word_freq is None:
            word_freq = {}
            for word in swearWords:
                word_freq[word] = word_freq.get(word, 0) + 1
            word_freq_collection.insert({
                "fromNumber": fromNumber, 
                "freq": word_freq
                })
        else:
            word_freq = word_freq['freq']
            for word in swearWords:
                word_freq[word] = word_freq.get(word, 0) + 1
            word_freq_collection.update({"fromNumber": fromNumber}, {"$set": {"freq": word_freq}})

        #FromUser freq - WHO are you swearing at?
        #Todo: might need to catch error where member does not exist
        from_member_collection = g.db.from_member_freq
        member_freq = from_member_collection.find_one({"fromNumber": fromNumber})
        if member_freq is None:
            from_member_collection.insert(
                {
                    "fromNumber": fromNumber,
                    "to": {
                        toNumber: len(swearWords)
                    }
                })
        else:
            to_member_freq = member_freq["to"]
            if not toNumber in to_member_freq:
                to_member_freq[toNumber] = len(swearWords)
            else:
                to_member_freq[toNumber] += len(swearWords)

            from_member_collection.update({"fromNumber": fromNumber}, {"$set": {"to": to_member_freq}})

        # do ass word freq
        ass_words_collection = g.db.ass_word_frequency
        for swearWord in swearWords:
            ass_words_obj = ass_words_collection.find_one({"number": fromNumber, "from": 1, "word": swearWord})
            if not ass_words_obj is None:
                ass_words = ass_words_obj["ass_words"]
            else: 
                ass_words = {}

            for word in words:
                trimed_word = trimWord(word)
                if swearWord != trimed_word:
                    ass_words[trimed_word] = ass_words.get(trimed_word, 0) + 1
            if ass_words_obj is None:
                ass_words_collection.insert({
                    "number": fromNumber,
                    "from": 1,
                    "word": swearWord,
                    "ass_words": ass_words,
                    })
            else:
                print ass_words
                ass_words_collection.update({"number": fromNumber, "from": 1, "word": swearWord}, {"$set": {"ass_words": ass_words}})


    # Update the master table
    messages_collection.insert({
        "reference_number": fromNumber,
        "swear_words": swearWords, 
        "score": score,
        "text": message,
        "time": cur_time,
        "fromName": getMemberName(fromNumber),
        "fromNumber": fromNumber,
        "toName": getMemberName(toNumber),
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
        if getSwearScore(trimWord(word)) > 0:
            score += getSwearScore(trimWord(word))
            swearWords.append(trimWord(word))

    if len(swearWords) != 0:

        #ToUser freq - Who swears at you?
        #Todo: might need to catch error where member does not exist
        to_member_collection = g.db.to_member_freq
        member_freq = to_member_collection.find_one({"toNumber": toNumber})
        if member_freq is None:
            to_member_collection.insert({
                "toNumber": toNumber, 
                "from": {
                    fromNumber: len(swearWords)
                    }
                })
        else:
            from_member_freq = member_freq["from"]
            if not fromNumber in from_member_freq:
                from_member_freq[fromNumber] = len(swearWords)
            else:
                from_member_freq[fromNumber] += len(swearWords)

            to_member_collection.update({"toNumber": toNumber}, {"$set": {"from": from_member_freq}})


        # do ass word freq
        ass_words_collection = g.db.ass_word_frequency
        for swearWord in swearWords:
            ass_words_obj = ass_words_collection.find_one({"number": toNumber, "from": 0, "word": swearWord})
            if not ass_words_obj is None:
                ass_words = ass_words_obj["ass_words"]
            else: 
                ass_words = {}
            
            for word in words:
                trimed_word = trimWord(word)
                if swearWord != trimed_word:
                    ass_words[trimed_word] = ass_words.get(trimed_word, 0) + 1
            if ass_words_obj is None:
                ass_words_collection.insert({
                    "number": toNumber,
                    "from": 0,
                    "word": swearWord,
                    "ass_words": ass_words,
                    })
            else:
                ass_words_collection.update({"number": toNumber, "from": 0, "word": swearWord}, {"$set": {"ass_words": ass_words}})


    # Update the master table
    messages_collection.insert({
        "reference_number": toNumber,
        "swear_words": swearWords, 
        "score": score,
        "text": message,
        "time": cur_time,
        "fromName": getMemberName(fromNumber),
        "fromNumber": fromNumber,
        "toName": getMemberName(toNumber),
        "toNumber": toNumber
        });

    return jsonify(**{
        "success": exitCode
        })

@app.route('/score/<number>', methods=['GET'])
def getScore(number):
    jars_collection = g.db.jars
    jar = jars_collection.find_one({"fromNumber": number})
    if jar is None:
        return jsonify(**{"score": 0})
    else:
        return jsonify(**{"score": jar['sum']})

@app.route('/register/<number>', methods=['POST'])   
def register(number):
    newNumber = number
    newName = request.form["name"]
    facebookId = request.form["facebook_id"]

    members_collection = g.db.member_numbers
    success = 0

    if members_collection.find({"number": newNumber}).count() == 0:
        # Add the member to the members table
        members_collection.insert({
            "number": newNumber,
            "name": newName,
            "facebook_id": facebookId
            })
        success = 1

    return jsonify(**{
        "success": success 
        })

@app.route('/jar/empty/<number>', methods=['POST'])
def emptyJar(number):
    jars_collection = g.db.jars
    jar = jars_collection.find_one({"fromNumber": number})

    if jar is None:
        return jsonify(**{"success": 0})
    else:
        jars_collection.update({"fromNumber": number}, {"$set": {"sum": 0}})
        return jsonify(**{"success": 1})

"""
Web APIs
"""
@app.route('/data/member/<fb_id>', methods=['GET'])
def getUserInfoByFb(fb_id):
    user_collection = g.db.member_numbers
    member_data = user_collection.find_one({"facebook_id": fb_id})
    if member_data is None:
        member_data = {}
    else:
        member_data.pop("_id")
    return jsonify(**member_data)

@app.route('/data/member/number/<number>', methods=['GET'])
def getUserInfoByNumber(number):
    user_collection = g.db.member_numbers
    member_data = user_collection.find_one({"number": number})
    if member_data is None:
        member_data = {}
    else:
        member_data.pop("_id")
    return jsonify(**member_data)

@app.route('/data/words/<userNumber>', methods=['GET'])
def getWordFrequency(userNumber, date = 0):
    word_freq_collection = g.db.word_frequency
    word_freq = word_freq_collection.find_one({"fromNumber": userNumber})

    if word_freq is None:
        return jsonify(**{"freq": []})
    else:
        return jsonify(**{"freq": word_freq['freq']})

@app.route('/data/who/<userNumber>', methods=['GET'])
def getMemberRelationships(userNumber, date = 0):
    from_freq_collection = g.db.from_member_freq
    from_freq = from_freq_collection.find_one({"fromNumber": userNumber})
    from_ret = {} if from_freq is None else from_freq["to"]
    from_ret = {getMemberName(number): val for number, val in from_ret.items()}

    to_freq_collection = g.db.to_member_freq
    to_freq = to_freq_collection.find_one({"toNumber": userNumber})
    to_ret = {} if to_freq is None else to_freq["from"]
    to_ret = {getMemberName(number): val for number, val in to_ret.items()}

    return jsonify(**{
        "from": from_ret,
        "to": to_ret
        })

@app.route('/data/why/<fromNumber>/<swearWord>', methods=['GET'])
def getAssociatedSwearWord(fromNumber, swearWord):
    ass_words_collection = g.db.ass_word_frequency
    sent_obj = ass_words_collection.find_one({"number": fromNumber, "from": 1, "word": swearWord})
    if sent_obj is None:
        sent_obj = {}
    else:
        sent_obj = sent_obj['ass_words']
    received_obj = ass_words_collection.find_one({"number": fromNumber, "from": 0, "word": swearWord})
    if received_obj is None:
        received_obj = {} 
    else:
        received_obj = received_obj['ass_words']

    return jsonify(**{
        "from": sent_obj,
        "to": received_obj
        })

@app.route('/data/timeseries/<fromNumber>/<int:startdate>/<int:enddate>', methods=['GET'])
def getMessagesByTime(fromNumber, startdate, enddate):
    messages_collection = g.db.messages

    msg_sent = messages_collection.find({
        "reference_number": fromNumber,
        "fromNumber": fromNumber,
        "time": {"$gt": startdate, "$lt": enddate}
        })
    swears_sent = [i for i in msg_sent if len(i['swear_words']) != 0]
    for swear in swears_sent:
        del swear["_id"]

    msg_receieved = messages_collection.find({
        "reference_number": fromNumber,
        "toNumber": fromNumber,
        "time": {"$gt": startdate, "$lt": enddate}
        })
    swears_receieved = [i for i in msg_receieved if len(i['swear_words']) != 0]
    for swear in swears_receieved:
        del swear["_id"]

    print swears_sent
    print swears_receieved
    return jsonify(**{
        "from": swears_sent,
        "to": swears_receieved
        })



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
