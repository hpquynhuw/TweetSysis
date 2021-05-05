from flask import Flask, render_template, url_for, redirect, request, send_from_directory
import json
import os
from datetime import date
import requests

from secrets import twitter_token
from secrets import base_url
now = date.today()  # end date

places = {'seattle':'2490383',
          'toronto': '4118',
           'sydney':'1105779',
           'london':'44418'}
headers={"Authorization": "Bearer {}".format(twitter_token)}
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('test.html')

@app.route('/home', methods=['GET'])
def back_home():
    return redirect(url_for('hello_world'));

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')

@app.route('/<place>', methods=['GET'])
def get_trends_today(place):
    # a=str(place)
    # print(a)
    trend_url = base_url + "trends/place.json?id=" + places[place]
    res = requests.get(trend_url, headers=headers)
    # filename = os.path.join(app.static_folder, 'data', f'{place}_2020-07-14.json')
    # data = json.load(open(filename))
    tweet_data = res.json()
    # filename = os.path.join(app.static_folder, 'data', 'seattle_2020-07-14.json')
    # data = json.load(tweet_data)
    return render_template('list.html', data=tweet_data)
