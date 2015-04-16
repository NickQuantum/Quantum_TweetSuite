# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:58:09 2015

@author: Gerald Varghese
"""
import flask, flask.views

from utils import login_required

class Search(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('search.html')
    
    @login_required    
    def post(self):
        result = eval(flask.request.form['searchtxt'])
        flask.flash(result)
        return flask.redirect(flask.url_for('search'))