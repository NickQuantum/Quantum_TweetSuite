# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 00:58:09 2015

@author: Quantum Solutions
"""
import flask, flask.views
import tweepy
import json


import login
from utils import login_required
from sys import platform as _platform



class Search(flask.views.MethodView):
    @login_required
    def get(self):
        return flask.render_template('search.html')
    
    @login_required    
    def post(self):
        ## tweet collector code here --
        #query = 'python'
        print('Search POST called')
        query = flask.request.form['Query']
        max_tweets = 100

        api = login.sapi
        searched_tweets = [status for status in tweepy.Cursor(api.search, q=query).items(max_tweets)]
        if _platform == "linux" or _platform == "linux2":
            # linux
            filepath = 'static/tweets/'+flask.session['uid']+'.txt'  
        elif _platform == "win32":
            # Windows...
            filepath = 'static//tweets//'+flask.session['uid']+'.txt'  

        print('file name =' + flask.session['username'])

        target = open(filepath, 'w')
        
        for tweet in searched_tweets:
            tweet_str = json.dumps(tweet._json)
            target.write(tweet_str + "\n")
        
        target.close()
        #result = flask.request.form['searchtxt']
        #flask.flash(result)
        print('tweets dumpted as json - next preparation for graph')
        import networkx as nx
        from networkx.readwrite import json_graph

        g = nx.Graph()
        

        #initialize a dict
        #iterate through all the tweets and get the user ids and the retweet user ids
        
        #Store user id and retweet user ids in a dict
        #Iterate through retweet user ids and user ids and add node and edge to graph
        
        retweet_user_dict = {}
        mention_user_dict = {}
        username_dict = {}
        user_list = []
        retweet_user_list = []
        mention_user_listoflists = []
        mention_user_list = []
        complete_user_list = []
        chunks = []
        tweets_file = open(filepath, "r")
        
        for line in tweets_file:
                try:
                    tweet = json.loads(line)
                    #hashtags = [hashtag['text'] for hashtag in tweet['entities']['hashtags']]
                    user_id = tweet['user']['id']            
                    user_list.append(user_id)
                    if 'retweeted_status' in tweet: 
                       
                        #pprint.pprint(tweet)
                        retweet_user_id = tweet['retweeted_status']['user']['id']                
                        retweet_user_list.append(retweet_user_id)
                        retweet_user_dict[user_id] = retweet_user_id
                    if 'entities' in tweet and len(tweet['entities']['user_mentions']) > 0:
                         mention_user_ids = [mention['id'] for mention in tweet['entities']['user_mentions']]
                         mention_user_listoflists.append(mention_user_ids)
                         mention_user_dict[user_id] = mention_user_ids
                    #pprint.pprint(user_list)
                    #print(tweets_data)
                except:
                    continue

        print('completed reading tweets file')
                    
        def get_user_info(user_ids):
            
            users = api.lookup_users(user_ids)
            for user in users:
                username_dict[user.id] = user.screen_name
            return username_dict            
        
        
        
        for mention_user_ids in mention_user_listoflists:
            for mention_user_id in mention_user_ids:
                mention_user_list.append(mention_user_id)
            
        # Added code to break into chunks of 100 as the api.looup_users has limit of 100 at a time
        ##username_dict = get_user_info(user_list + retweet_user_list + mention_user_list)
        complete_user_list = user_list + retweet_user_list + mention_user_list
        chunks=[complete_user_list[x:x+100] for x in xrange(0, len(complete_user_list), 100)]
        for i in range(len(chunks)):
            username_dict = get_user_info(chunks[i])
            
        print mention_user_list
                
        print username_dict
                
        def add_node_tw(n, weight=None, time=None, source=None):
            if not g.has_node(n):
                screen_name = username_dict.get(n)
                g.add_node(n)
                g.node[n]['weight'] = 1
                g.node[n]['screen_name'] = screen_name
            
            else:
                g.node[n]['weight']+=1
                
        def add_edge_tw(n1,n2, weight=None):
            if not g.has_edge(n1,n2):
                g.add_edge(n1,n2)
                g[n1][n2]['weight']=1
            else:
                g[n1][n2]['weight']+=1
        

        
        for user_id in user_list:
            add_node_tw(user_id)
            if user_id in retweet_user_dict:
                    retweet_user_id = retweet_user_dict.get(user_id)           
                    add_node_tw(retweet_user_id)
                    add_edge_tw(retweet_user_id,user_id)
            if user_id in mention_user_dict:
                for mention_user_id in mention_user_dict.get(user_id):
                
                    add_node_tw(mention_user_id)
                    add_edge_tw(mention_user_id,user_id)
        
        ## gexf is not needed now; until we start using GEPHI    
        ##nx.write_gexf(g, 'C://Temp//test.gexf')
        if _platform == "linux" or _platform == "linux2":
            # linux
            filepathjson = 'static/tweets/'+flask.session['uid']+'.json'  ##'/tmp/tweetgraph.json' 
            print(filepathjson)
        elif _platform == "win32":
            # Windows...
            filepathjson = 'static//tweets//'+flask.session['uid']+'.json' 
            
        try:
            print('before readwrite')
            data = json_graph.node_link_data(g)
            print('readwrite successful')
            ##pprint.pprint(data) 
            with open(filepathjson, 'w') as outfile:
                json.dump(data, outfile)
                print json.dumps(data)       
                print('JSON file Created!')
        except:
            print('JSON FILE Creation FAILED')
        

        
        
        return flask.redirect(flask.url_for('result'))