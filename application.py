# -*- coding: utf-8 -*-
"""

@author: Gerald Varghese
"""

import flask, flask.views
#import os


#views
from classes.login import Login
from classes.search import Search
from classes.register import Register

application = flask.Flask(__name__)
application.secret_key = "bacon"


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

#handler to page not found - or incorrect URL
@application.errorhandler(404)
def page_not_found(error):
    return flask.redirect(flask.url_for('login'))
#application.debug = True
if __name__ == '__main__':
    application.run()
