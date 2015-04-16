# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 01:03:36 2015

@author: geral_000
"""
import flask, flask.views


class Register(flask.views.MethodView):
    def get(self):
        return flask.render_template('register.html')

    def post(self):
        flask.flash('You are registered!!')
        return flask.redirect(flask.url_for('login'))