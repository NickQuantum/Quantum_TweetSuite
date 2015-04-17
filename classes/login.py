# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:54:02 2015

@author: Gerald Varghese
"""
import flask, flask.views


users = {'admin@admin.com':'admin'}


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
        if username in users and users[username] == passwd:
            flask.session['username'] = username
            return flask.redirect(flask.url_for('search'))
        else:
            flask.flash("Username doesn't exist or incorrect password")
            return flask.redirect(flask.url_for('login'))


