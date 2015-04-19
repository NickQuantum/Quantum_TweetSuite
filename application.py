# -*- coding: utf-8 -*-
"""

@author: Gerald Varghese
"""

import flask, flask.views
import json
import pprint

#import os


#views
from classes.login import Login
from classes.search import Search
from classes.register import Register

#The tweets
tweets_data_path = "/tmp/tweepy_text.txt" #"C:\\Users\\geral_000\\Downloads\\twitter_data.txt" #        
tweets_data = []
tweets_file = open(tweets_data_path, "r")

for line in tweets_file:
        try:
            tweet = json.loads(line)
            #pprint.pprint(tweet["text"])
            pprint.pprint(tweet["user"]["screen_name"])
           #print tweet
            #tweet["text"]
            #tweets_data.append(tweet)
            hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
            print(hashtags)
            tweets_data.append([tweet["text"],tweet["user"]["screen_name"],
                               hashtags])
            pprint.pprint(tweets_data)
            
        except:
            continue

#Declare the application
application = flask.Flask(__name__)
application.secret_key = "bacon"


@application.route('/showtable')
def show_table():
    #table = g.dyndb.get_table('entries')
    #entries = table.scan()
    #logging.info('show_table: N=%s' % entries)
    #return render_template('show_table.html', entries=entries)
    tweets = tweets_data
    return flask.render_template('show_table.html', tweets=tweets)

#routes
application.add_url_rule('/',
                 view_func=Login.as_view('login'),
                 methods=["Get","POST"])
application.add_url_rule('/search/',
                 view_func=Search.as_view('search'), 
                 methods=['GET','POST'])
application.add_url_rule('/register/',
                 view_func=Register.as_view('register'), 
                 methods=['GET','POST'])

#handler to page not found - or incorrect URL
@application.errorhandler(404)
def page_not_found(error):
    return flask.redirect(flask.url_for('login'))
#application.debug = True
if __name__ == '__main__':
    application.run()
