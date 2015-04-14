# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import flask, flask.views
#import os
import functools

application = flask.Flask(__name__)
application.secret_key = "bacon"

users = {'admin@admin.com':'admin'}


class Main(flask.views.MethodView):
    def get(self):
        return flask.render_template('index.html')

    def post(self):
        if 'logout' in flask.request.form:
            flask.session.pop('username', None)
            return flask.redirect(flask.url_for('index'))
        required = ['username','passwd']
        for r in required:
            if r not in flask.request.form:
                flask.flash("Error: {0} is required.".format(r))
                return flask.redirect(flask.url_for('index'))
        username = flask.request.form['username']
        passwd = flask.request.form['passwd']
        if username in users and users[username] == passwd:
            flask.session['username'] = username
        else:
            flask.flash("Username doesn't exist or incorrect password")
        return flask.redirect(flask.url_for('index'))



def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return flask.redirect(flask.url_for('index'))
    return wrapper


class Remote(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('remote.html')
    
    @login_required    
    def post(self):
        result = eval(flask.request.form['expression'])
        flask.flash(result)
        return flask.redirect(flask.url_for('remote'))

application.add_url_rule('/',
                 view_func=Main.as_view('index'),
                 methods=["Get","POST"])
application.add_url_rule('/remote/',
                 view_func=Remote.as_view('remote'), 
                 methods=['GET','POST'])

#application.debug = True
if __name__ == '__main__':
    application.run()
