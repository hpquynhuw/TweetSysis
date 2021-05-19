from flask import Flask, render_template, url_for, redirect, request, send_from_directory
import json
import os
from datetime import date
import requests

from secrets import twitter_token, base_url, search_url, token2
now = date.today()  # end date

places = {'Seattle':'2490383',
          'Toronto': '4118',
           'Sydney':'1105779',
           'London':'44418'}
headers={"Authorization": "Bearer {}".format(twitter_token)}
headers2={"Authorization": "Bearer {}".format(token2)}

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/')
def hello_world():
    return render_template('base.html', data=[], place="")

@app.route('/home', methods=['GET'])
def back_home():
    return redirect(url_for('hello_world'));

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='favicon.ico')

@app.route('/<place>', methods=['GET'])
def get_trends_today(place):
    trend_url = base_url + "trends/place.json?id=" + places[place]
    res = requests.get(trend_url, headers=headers)
    tweet_data = res.json()
    # render_template('list.html', data=tweet_data, place=place)
    return render_template('base.html', data=tweet_data, place=place);

@app.route('/<place>/<query>', methods=['GET'])
def search(place, query):
    query_url=search_url.format(query)
    res=requests.get(query_url, headers=headers)
    tweet_data=res.json()
    render_template('tweet_list.html', data=tweet_data['statuses'], query=query)
    return redirect(url_for('hello_world'));

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.run(debug=True)
