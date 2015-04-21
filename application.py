# -*- coding: utf-8 -*-
"""

@author: Gerald Varghese
"""

import flask, flask.views
#import os


#views
from classes.login import Login, sapi
from classes.search import Search
from classes.register import Register
from classes.result import Result
from classes.utils import login_required


#Declare the application
application = flask.Flask(__name__)
application.secret_key = "bacon"
##application = app = Flask(__name__)
##app.config.from_object(__name__)




class ShowTweets(flask.views.MethodView):
    @login_required
    def get(self):
        api = sapi
        tweets=[]
        public_tweets = api.home_timeline()
        for tweet in public_tweets:
            #tweets.append(tweet.text)
            #hashtags = [hashtag.text for hashtag in tweet.entities.hashtags]
            #print(hashtags)
            tweets.append([tweet.text,tweet.user.screen_name,tweet.favorite_count])
        print(tweets)
        return flask.render_template('show_tweets.html', tweets=tweets)


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
application.add_url_rule('/result/',
                 view_func=Result.as_view('result'), 
                 methods=['GET'])
application.add_url_rule('/showtweets',
                 view_func=ShowTweets.as_view('showtweets'),
                 methods=['GET'])

#handler to page not found - or incorrect URL
@application.errorhandler(404)
def page_not_found(error):
    return flask.redirect(flask.url_for('login'))
#application.debug = True
if __name__ == '__main__':
    application.run()
