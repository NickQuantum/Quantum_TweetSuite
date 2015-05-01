# -*- coding: utf-8 -*-
"""

@author: Gerald Varghese
"""

import flask, flask.views
#import os


#views
from classes.login import Login, sapi
from classes.search import Search
from classes.register import Register
from classes.result import Result
from classes.utils import login_required


#Declare the application
tweetsuite = application = flask.Flask(__name__)
tweetsuite.secret_key = "bacon"
##application = app = Flask(__name__)
##app.config.from_object(__name__)




class Logout(flask.views.MethodView):
    def get(self):
        flask.session.pop('username', None)
        flask.session.pop('uid',None)
        return flask.redirect(flask.url_for('login'))


class ShowGraph(flask.views.MethodView):
    def get(self):
        print('Show Graph invoked!')
        return flask.render_template('show_graph.html')

#routes
tweetsuite.add_url_rule('/',
                 view_func=Login.as_view('login'),
                 methods=["Get","POST"])
tweetsuite.add_url_rule('/search/',
                 view_func=Search.as_view('search'), 
                 methods=['GET','POST'])
tweetsuite.add_url_rule('/register/',
                 view_func=Register.as_view('register'), 
                 methods=['GET','POST'])
tweetsuite.add_url_rule('/result/',
                 view_func=Result.as_view('result'), 
                 methods=['GET'])
tweetsuite.add_url_rule('/logout',
                 view_func=Logout.as_view('logout'),
                 methods=['GET'])
tweetsuite.add_url_rule('/showgraph',
                 view_func=ShowGraph.as_view('showgraph'),
                 methods=['GET'])


#handler to page not found - or incorrect URL
@tweetsuite.errorhandler(404)
def page_not_found(error):
    return flask.redirect(flask.url_for('login'))
#application.debug = True
if __name__ == '__main__':
    tweetsuite.run()
