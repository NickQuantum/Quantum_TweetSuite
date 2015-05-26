# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:01:00 2015

@author: Quantum Solutions
"""
import flask, flask.views
import functools
import tweepy
import uuid


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('login'))
    return wrapper


def settwitterapi(username):
    flask.session['username'] = username
    uid = uuid.uuid4()
    flask.session['uid'] = uid.urn[9:]
    ## create API Object using Twitter access keys
    ##one time
    consumer_key = "mpIuWJYkQKUvaiS4FPwQpGVr8"
    consumer_secret = "EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE"
    access_token = "3080403725-gleW4H38K4tJ69vtUFJDZgBCr2VtqFb3D06Xk7y"
    access_token_secret = "zWxk43qe3c8QlP6Pua2A81UvDTlpe90lqUVC5PxZEzcqg"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    sapi = tweepy.API(auth)
    
    return sapi