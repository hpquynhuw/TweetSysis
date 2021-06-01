from flask import Flask, render_template, url_for, redirect, request, send_from_directory, jsonify
from flask_cors import CORS
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('spacytextblob')

import requests

from secrets import twitter_token, base_url, search_url, token2, search_url2

places = {'Seattle': '2490383',
          'Toronto': '4118',
          'Sydney': '1105779',
          'London': '44418'}

headers = {"Authorization": "Bearer {}".format(twitter_token)}
headers2 = {"Authorization": "Bearer {}".format(token2)}

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


# @app.route('/')
# def hello_world():
#     return render_template('base.html', data=[], place="")


@app.route('/sentiment/', methods=['POST'])
def spacy_sent():
    if request.method == 'POST':
        post_data = request.get_json()
    print(post_data)
    doc=nlp(post_data.get('text'))
    return jsonify({
        'status': 'success',
        'polarity': doc._.polarity,      # Polarity: [-1,1]
        'subjectivity': doc._.subjectivity, # Sujectivity: 0.9
        'assessment': doc._.assessments,
    })


@app.route('/trends/<location>', methods=['GET'])
def get_trends_today(location):
    TRENDS = []
    trend_url = base_url + "trends/place.json?id=" + places[location]
    res = requests.get(trend_url, headers=headers)
    tweet_data = res.json()
    for i in tweet_data[0]['trends']:
        if i['tweet_volume'] is not None:
            TRENDS.append({
                'name': i['name'],
                'tweet_volume': i['tweet_volume']
            })
    return jsonify({
        'status': 'success',
        'trends': TRENDS
    })


@app.route('/tweets/', methods=['GET', 'POST'])
def search():
    tweet_fields = "tweet.fields=author_id,created_at"
    if request.method == 'POST':
        post_data = request.get_json()
    query = parse_query(post_data.get('name'))
    query_url = search_url2.format(query, tweet_fields)
    print(query_url)
    res = requests.get(query_url, headers=headers2)
    tweet_data = res.json()
    print(tweet_data)
    return jsonify({
        'status': 'success',
        'tweets': tweet_data
    })


def parse_query(query):
    parsed = ''
    for i in query:
        if i == ' ':
            parsed += '%20'
        elif i == '#':
            parsed += '%23'
        else:
            parsed += i
    return parsed

if __name__ == '__main__':
    app.run()
