# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:03:36 2015

@author: geral_000
"""
import flask, flask.views

from boto.dynamodb2.table import Table


class Register(flask.views.MethodView):
    def get(self):
        return flask.render_template('register.html')

    def post(self):
        print('inside post method')
        required = ['username','password','password2']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0}/{1} is required.".format(r))
                return flask.redirect(flask.url_for('register'))
        username = flask.request.form['username']
        password = flask.request.form['password']
        print('username is: '+  username)
        print('password is: ' + password)
        try:
            users = Table('Users')
            print('Users table successful!')
            users.put_item(data={'EmailId':username,'Password':password})
            print('add item successful')
            flask.flash('You are registered!!')
            return flask.redirect(flask.url_for('login'))
        except:
            flask.flash('Registration failed - user exists!')
            return flask.redirect(flask.url_for('register'))
