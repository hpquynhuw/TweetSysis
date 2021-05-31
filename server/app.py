from flask import Flask, render_template, url_for, redirect, request, send_from_directory, jsonify
from flask_cors import CORS
import json
import os
from datetime import date
import requests

from secrets import twitter_token, base_url, search_url, token2

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


# @app.route('/home', methods=['GET'])
# def back_home():
#     return redirect(url_for('hello_world'));


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


# @app.route('/<place>/<query>', methods=['GET'])
# def search(place, query):
#     query_url = search_url.format(query)
#     res = requests.get(query_url, headers=headers)
#     tweet_data = res.json()
#     render_template('tweet_list.html', data=tweet_data['statuses'], query=query)
#     return redirect(url_for('hello_world'));
#

if __name__ == '__main__':
    app.run()
