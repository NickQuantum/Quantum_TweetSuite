import re
import nltk
import nltk.classify
import flask, flask.views
import json
import pandas
import numpy as np
import pickle
import math
from nltk.probability import FreqDist, DictionaryProbDist, ELEProbDist, sum_logs
from sys import platform as _platform



#Call tweet_processor
def getTestDF():
    if _platform == "linux" or _platform == "linux2":
        # linux
        tweets_data_path = 'static/tweets/'+flask.session['uid']+'.txt' 
    elif _platform == "win32":
                # Windows...
        tweets_data_path = 'static//tweets//'+flask.session['uid']+'.txt'      
    
    tweets_data = []
    tweets_file = open(tweets_data_path, "r")


    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
       
        except:
            continue
    tweetsDF = pandas.DataFrame.from_records(tweets_data)
  
    return tweetsDF
#end

# from this feature list , do a extract of featurs
def extract_features(document,word_features): 
    document_words = set(document) 
    features = {} 
    for word in word_features: 
        features['contains(%s)' % word] = (word in document_words) 
    return features

# end

# process sentiment
def process_sentiment():
    fromtweepyDF = getTestDF()
    
    ## Load the classifier
    # we open the file for reading
    fileObject = open("static//sentiment//classifier",'r')  
    # load the object from the file into var b
    classifier = pickle.load(fileObject)
    fileObject.close()
    
    ## Load the bag of words
    # we open the file for reading
    fileObject = open("static//sentiment//bagofwords",'r')  
    # load the object from the file into var b
    word_features = pickle.load(fileObject)
    fileObject.close()
    
    
    
    
    hashtagDF2 =[]
    xycoordinates = []
    sentimentlist = []
    columns=['id','user','date','tweet','mentions received','hashtag','sentiment','numberof followers','friends count','retweeted count']
    testtweetDF = pandas.DataFrame(data=np.zeros((0,len(columns))),  columns = columns)
    num_positive_tweets = 0
    num_negative_tweets = 0
    for index,row in fromtweepyDF.iterrows():
        tweet =row['text']
        ## get hashtags
        hashtags = ''
        hashtags = re.findall(r"#(\w+)", tweet)
        for item in hashtags:
               if item <> '' :
                    hashtagDF2.append( item)
        ## username
        user = re.findall('@[^\s]+',tweet)
        xycoordinates= classifier.prob_classify(extract_features(tweet.split(),word_features))
        
        #print (xycoordinates._prob_dict)
        
        retweeted_count = row['retweet_count']
        result= classifier.classify(extract_features(tweet.split(),word_features))
        sentimentlist.append([math.exp(xycoordinates._prob_dict.items()[0][1])*200,
                              math.exp(xycoordinates._prob_dict.items()[1][1])*200, 
                              tweet,result, retweeted_count])
        if result == 'positive':
            num_positive_tweets += 1
        else:
            num_negative_tweets += 1
        
        
        data = [row['id'], user,row['created_at'],tweet,index,hashtags,result,index,index,row['retweet_count']]
        testtweetDF = testtweetDF.T
        testtweetDF[index] = data
        testtweetDF = testtweetDF.T
    
    print ("Number of Positive tweets = ", num_positive_tweets )
    print ("Number of Negative tweets = ", num_negative_tweets )
    ##sentimentlist.extend(result) 
    #print sentimentlist
    
    if _platform == "linux" or _platform == "linux2":
                # linux
                filepathjson = 'static/tweets/'+flask.session['uid']+'splot.json' 
    elif _platform == "win32":
                # Windows...
                filepathjson = filepathjson = 'static//tweets//'+flask.session['uid']+'splot.json' 
                
    try:
        print('before readwrite')
        data = sentimentlist
        print('readwrite successful')
        ##pprint.pprint(data) 
        with open(filepathjson, 'w') as outfile:
            json.dump(data, outfile)
            #print json.dumps(data)       
            print('JSON file Created!')
    except:
        print('JSON FILE Creation FAILED')
        
    columns2 = ['hashtags']
    hashtagDF = pandas.DataFrame(data = hashtagDF2,columns =columns2)
    #print (testtweetDF)
    ##print ( xycoordinates._prob_dict)
    ##print (xycoordinates.max())
    ##print (xycoordinates._prob_dict.items()[1][1])
    classifier.show_most_informative_features()
