# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:54:02 2015

@author: Quantum Solutions
"""
import flask, flask.views


from boto.dynamodb2.table import Table
from sys import platform as _platform
import utils

#sapi = 0

class Login(flask.views.MethodView):
    def get(self):
        try:
            if flask.session['username']:
                print(flask.session['username'])
                return flask.redirect(flask.url_for('search'))
        except:
            flask.session.pop('username', None)
            flask.session.pop('uid',None)
        return flask.render_template('index.html')

    def isValidUser(self, username, passwd):
        print('this is ' + _platform + ' system')
        users = {'admin@admin.com':'admin'} 

        if _platform == "linux" or _platform == "linux2":
            try:
                print('Before accessing DynamoDB')
                users = Table('Users')
                validuser = users.get_item(EmailId=username,Password=passwd)
                print('Linux - dynamodb authorization successful')
            except:
                validuser = None
                print('Accessing DynamoDB failed')
                pass
        else:
            try:
                if (username in users and users[username] == passwd and _platform == "win32"):
                    validuser = 'success'
                    print('Windows - authorization successful')
                else:
                    validuser = None
                    print('Windows authorization failed!')
            except:
                validuser = None
                print('local authentication failed')
        return validuser

    def post(self):
        required = ['username','passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('login'))
        username = flask.request.form['username']
        print('username: ' + username)
        passwd = flask.request.form['passwd']
        print('password: ' + passwd)
        
        print('before checking the login credentials')
        validuser = self.isValidUser(username, passwd)

        if validuser:
            print('login successful')
           
            utils.settwitterapi(username)
            
            return flask.redirect(flask.url_for('search'))
        else:
            flask.flash("Username doesn't exist or incorrect password")
            return flask.redirect(flask.url_for('login'))

        
