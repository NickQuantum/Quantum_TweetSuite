# -*- coding: utf-8 -*-
"""

@author: Quantum Solutions
"""
import flask, flask.views
from sys import platform as _platform

#Declare the application
tweetsuite = application = flask.Flask(__name__)

@application.route('/')

class Demo(flask.views.MethodView):
    def get(self):
        print('Demo Page Invoked!!')
        return flask.render_template('demo_sna_graph.html')

tweetsuite.add_url_rule('/demo',
                 view_func=Demo.as_view('demo'),
                 methods=['GET'])
   
if _platform == "win64" or  _platform == "win32":
    application.debug = True
              
if __name__ == '__main__':
    tweetsuite.run(host='0.0.0.0', port=5000)

