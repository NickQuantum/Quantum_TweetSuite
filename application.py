# -*- coding: utf-8 -*-
"""

@author: Gerald Varghese
"""

import flask, flask.views
import tweepy

#import os


#views
from classes.login import Login
from classes.search import Search
from classes.register import Register
from classes.result import Result



#Declare the application
application = flask.Flask(__name__)
application.secret_key = "bacon"





class ShowTweets(flask.views.MethodView):
    def get(self):
        consumer_key = "mpIuWJYkQKUvaiS4FPwQpGVr8"
        consumer_secret = "EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE"
        access_token = "3080403725-gleW4H38K4tJ69vtUFJDZgBCr2VtqFb3D06Xk7y"
        access_token_secret = "zWxk43qe3c8QlP6Pua2A81UvDTlpe90lqUVC5PxZEzcqg"
        tweets= []
        
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        
        api = tweepy.API(auth)
        
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
