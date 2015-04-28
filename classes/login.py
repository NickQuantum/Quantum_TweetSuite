# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:54:02 2015

@author: Gerald Varghese
"""
import flask, flask.views
import tweepy

from boto.dynamodb2.table import Table

#users = {'admin@admin.com':'admin'}
sapi = 0

class Login(flask.views.MethodView):
    def get(self):
        return flask.render_template('login.html')

    def post(self):
        required = ['username','passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('login'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        

        users = Table('Users')
        #user = users.get_item(EmailId='admin@admin.com',Password='admin')
        try:
            user = users.get_item(EmailId=username,Password=passwd)
        except:
            user = None
            pass
        
        #if username in users and users[username] == passwd:
        if user:
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

