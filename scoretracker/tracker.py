"""
The main logic of the bot.

This file implements the database and bot command parsing.
"""
import json
import os

from collections import defaultdict

import connexion
import requests


BOT_ID = os.environ['BOT_ID']
DB_FILE = 'data.json'
POST_URL = 'https://api.groupme.com/v3/bots/post'


def defaultdict_of_ints(init=None):
    """
    Constructor for defaultdict(int)
    """
    return defaultdict(int, init or {})


def get_db(filename=DB_FILE):
    """
    Try to load a JSON file and return a default dictionary containing
    the scores for a given person.

    If the file is not found or is not a valid JSON object, an empty
    collection is returned.
    """
    try:
        with open(filename, 'r') as db:
            data = json.load(db)
    except (FileNotFoundError, IOError, json.JSONDecodeError):
        data = {}

    return defaultdict(defaultdict_of_ints, data)


def increment_score(score, person, number):
    """
    Increments/decrements the score for the given user by number.

    Ed: /score show ron disappointment
    Scorebot: ron:
                  disappointment: 420
    Ed: /score ron disappointment + 420
    Scorebot: Incremented disappointment by 420 for ron
    Ed: /score show ron disappointment
    Scorebot: ron:
                  disappointment: 840
    """
    database = get_db()

    try:
        database[person][score] += number
    except KeyError:
        database[person][score] = number

    if database[person][score] == 0:
        database[person].pop(score)
        if database[person] == {}:
            database.pop(person)

    with open(DB_FILE, 'w') as db:
        json.dump(database, db)

    response = {
        'bot_id': BOT_ID,
        'text': 'Incremented {score} score by {number} for {person}'.format(
            score=score, number=number, person=person
        )
    }
    requests.post(POST_URL, json.dumps(response))


def get_scores(database, person, multi=True):
    """
    Return a string representing the scores a person has in the database.

    The parameter `multi' is to specify whether the scores are used for
    displaying the scores of a single person or multiple people.
    """
    indent = '     ' if multi else ''
    return ''.join(
        indent + '{score}: {points}\n'.format(score=score, points=points)
        for score, points in database[person].items()
    )


def show_score(person=None, score=None):
    """
    Sends to the chat the information about:
    * All (person, score) combinations
    * All scores of a given user
    * A given user's score in a specific topic

    Ed: /score show ron
    Scorebot: ron:
                  disappointment: 420
                  understanding-the-rules: -69
    """
    response = {'bot_id': BOT_ID}
    response['text'] = ''

    database = get_db()

    if not database:
        # Backup did not exist or was empty
        response['text'] = 'There are no scores yet!'

    elif person is None:
        response['text'] = '\n'.join(
            '{person}:\n{scores}'.format(
                person=person,
                scores=get_scores(database, person)
            )
            for person in database
        )

    elif person not in database:
        response['text'] = 'User is either unrecognized or has no points'

    elif score is None:
        response['text'] = get_scores(database, person, multi=False)

    else:
        response['text'] = '{person}:\n    {score}: {points}'.format(
            person=person, score=score, points=database[person][score]
        )

    requests.post(POST_URL, json.dumps(response))


def invalid_request():
    """
    Respond to the chat informing the user that they entered an invalid
    command for the bot.
    """
    response = {
        'bot_id': BOT_ID,
        'text': 'That was not a valid scorebot command. Valid commands include:\n'+
        '/score show: Shows all scores\n'+
        '/score show <person> [category]: Shows all of [person]\'s scores, or score in [category]\n'+
        '/score <person> <category> <+/-> <#>: Modifies [person]\'s score in [category] by [#]'
    }
    requests.post(POST_URL, json.dumps(response))


def recv_msg():
    """
    Handles the CRUD operations represented by the following commands:

    Increment/Decrement a score:
        /score <person> <score> <+/-> <#>

    Show all user's scores:
        /score show

    Show a specific person's score(s):
        /score show <person> [score]
    """
    message = connexion.request.json['text']
    message = message.split(' ')
    if message[0] == '/score':
        if len(message) == 5:
            print("Change scores")
            _, person, score, plus_minus, number = message
            increment = -int(number) if plus_minus == '-' else int(number)
            increment_score(score, person, increment)
        elif len(message) == 4 and message[1] == 'show':
            print("Show one score for one person")
            _, _, person, score = message
            show_score(person, score)
        elif len(message) == 3 and message[1] == 'show':
            print("Show all scores for one person")
            person = message[2]
            show_score(person)
        elif len(message) == 2 and message[1] == 'show':
            print("Show all scores for everyone")
            show_score()
        else:
            invalid_request()
