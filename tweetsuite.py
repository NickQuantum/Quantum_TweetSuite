# -*- coding: utf-8 -*-
"""

@author: Quantum Solutions
"""

import flask, flask.views


#views
from classes.login import Login
from classes.search import Search
from classes.register import Register
from classes.result import Result
from classes.utils import settwitterapi
from sys import platform as _platform


#Declare the application
tweetsuite = application = flask.Flask(__name__)
tweetsuite.secret_key = "bacon"


 
class Logout(flask.views.MethodView):
    def get(self):
        flask.session.pop('username', None)
        flask.session.pop('uid',None)
        flask.session.pop('query', None)
        
        # set dummy user - "demo"
        username = "demo"
        settwitterapi(username)
        return flask.render_template('index.html')

class MainLine(flask.views.MethodView):
    def get(self):
        print('Index Page with GET invoked!')
        return flask.redirect(flask.url_for('logout'))
        
    def post(self):
        print('Index Page with POST invoked!')
        return flask.redirect(flask.url_for('login'))


class Demo(flask.views.MethodView):
    def get(self):
        print('Demo Page Invoked!!')
        return flask.render_template('demo_sna_graph.html')

#routes
tweetsuite.add_url_rule('/',
                 view_func=MainLine.as_view('index'),
                 methods=["Get","POST"])
tweetsuite.add_url_rule('/login',
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
tweetsuite.add_url_rule('/demo',
                 view_func=Demo.as_view('demo'),
                 methods=['GET'])

#handler to page not found - or incorrect URL
@tweetsuite.errorhandler(404)
def page_not_found(error):
    return flask.redirect(flask.url_for('login'))
    
if _platform == "win32":
    application.debug = True

if __name__ == '__main__':
    tweetsuite.run(host='0.0.0.0', port=5000)
