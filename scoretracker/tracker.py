import os

import connexion
import json
import requests

BOT_ID = os.environ['BOT_ID']


def openDatabaseToWrite():
    return open('data.json', 'w+')


def openDatabaseToRead():
    return open('data.json', 'r')


def increment_score(score, person, number):
    with openDatabaseToWrite() as db:
        try:
            database = json.load(db)
        except Exception:
            database = {}
        try:
            database[person][score] += number
        except KeyError as ke:
            if person in str(ke):
                database[person] = {}
                database[person][score] = number
            elif score in str(ke):
                database[person][score] = number
        db.write(str(database))
    rT = {}
    rT['bot_id'] = BOT_ID
    rT['text'] = 'Incremented '+score+' score by '+str(number)+' for '+person
    requests.post('https://api.groupme.com/v3/bots/post', json.dumps(rT))


def show_score(person=None, score=None):
    rT = {}
    rT['bot_id'] = BOT_ID
    rT['text'] = ''
    with openDatabaseToRead() as db:
        try:
            database = json.load(db)
            if len(database) == 0:
                raise Exception()
        except Exception:
            rT['text'] = 'There are no scores yet!'
            requests.post('https://api.groupme.com/v3/bots/post',
                          json.dumps(rT))
            return
        if person is not None:
            rT['text'] += person + ':\n'
            if score is not None:
                rT['text'] += '    '+score+': '+database[person][score]+'\n'
            else:
                for sco in database[person].keys():
                    rT['text'] += '    '+sco+': '+database[person][sco]+'\n'
        else:
            for per, scores in database.items():
                rT['text'] += person + ':\n'
                for sco in scores:
                    rT['text'] += '    '+sco+': '+database[per][sco]+'\n'
    requests.post('https://api.groupme.com/v3/bots/post', json.dumps(rT))


def invalid_request():
    rT = {}
    rT['bot_id'] = BOT_ID
    rT['text'] = 'That was not a valid scorebot command'
    requests.post('https://api.groupme.com/v3/bots/post', json.dumps(rT))


# /score <person> <score> <+/-> <#>
# /score show
# /score show <person> [score]
def recv_msg():
    message = connexion.request.json['text']
    message = message.split(' ')
    if message[0] == '/score':
        if len(message) == 5:
            print("Change scores")
            score = message[2]
            person = message[1]
            number = int(message[4])
            if message[3] == '-':
                number *= -1
            increment_score(score, person, number)
        elif len(message) == 4:
            print("Show one score for one person")
            score = message[3]
            person = message[2]
            show_score(person, score)
        elif len(message) == 3:
            print("Show all scores for one person")
            person = message[2]
            show_score(person)
        elif len(message) == 2:
            print("Show all scores for everyone")
            show_score()
        else:
            invalid_request()
    # return connexion.request.json, 501
