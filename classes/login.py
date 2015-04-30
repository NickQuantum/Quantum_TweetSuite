# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:54:02 2015

@author: Gerald Varghese
"""
import flask, flask.views
import tweepy

from boto.dynamodb2.table import Table
from sys import platform as _platform

sapi = 0

class Login(flask.views.MethodView):
    def get(self):
        return flask.render_template('login.html')

    def post(self):
        print('this is ' + _platform + ' system')
        if _platform == "linux" or _platform == "linux2":
            # linux
            users = None
            print('this is ' + _platform + ' system')
        elif _platform == "win32":
            # Windows...
            users = {'admin@admin.com':'admin'} 

        required = ['username','passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('login'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        

        print('Before accessing DynamoDB')
        if _platform == "linux" or _platform == "linux2":
            try:
                users = Table('Users')
                validuser = users.get_item(EmailId=username,Password=passwd)
            except:
                validuser = None
                print('Accessing DynamoDB failed')
                pass
        else:
            try:
                if (username in users and users[username] == passwd and _platform == "win32"):
                    validuser = 'success'
            except:
                validuser = None
                print('local authentication failed')
        
        print('before checking the login credentials')

        if validuser:
            print('login successful')
            flask.session['username'] = username
            ## create API Object using Twitter access keys
            ##one time
            consumer_key = "mpIuWJYkQKUvaiS4FPwQpGVr8"
            consumer_secret = "EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE"
            access_token = "3080403725-gleW4H38K4tJ69vtUFJDZgBCr2VtqFb3D06Xk7y"
            access_token_secret = "zWxk43qe3c8QlP6Pua2A81UvDTlpe90lqUVC5PxZEzcqg"
            
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            
            global sapi
            sapi = tweepy.API(auth)
            
            return flask.redirect(flask.url_for('search'))
        else:
            flask.flash("Username doesn't exist or incorrect password")
            return flask.redirect(flask.url_for('login'))

