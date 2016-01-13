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

from datetime import datetime
from threading import Thread
##from flask import render_template, copy_current_request_context, current_app



#Call tweet_processor
def getTestDF():
    print('INSIDE getTestDF method in findsentiment.py')
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

#start process_tweet
def processTweet(tweet):
    # process the tweets

    #Convert to lower case
    tweet = tweet.lower()
    #Convert www.* or https?://* to URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    #Convert @username to AT_USER
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    #Remove additional white spaces
    tweet = re.sub('[\s]+', ' ', tweet)
    #Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    #trim
    tweet = tweet.strip('\'"')
    return tweet
#end
    
    #start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

#start getStopWordList
def getStopWordList(stopWordListFileName):
    #read the stopwords file and build a list
    stopWords = []
    stopWords.append('AT_USER')
    stopWords.append('URL')

    fp = open(stopWordListFileName, 'r')
    line = fp.readline()
    while line:
        word = line.strip()
        stopWords.append(word)
        line = fp.readline()
    fp.close()
    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet):
    featureVector = []
    #split tweet into words
    words = tweet.split()
    for w in words:
        #replace two or more with two occurrences
        w = replaceTwoOrMore(w)
        #strip punctuation
        w = w.strip('\'"?,.')
        #check if the word stats with an alphabet
        val = re.search(r"^[a-zA-Z][a-zA-Z0-9]*$", w)
        #ignore if it is a stop word
        if(w in stopWords or val is None):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end
    
##stopWords = getStopWordList('C://Users//u23139//QuantumTweetSuite//static//sentiment//stopwords.txt')


if _platform == "linux" or _platform == "linux2":
    # linux
    stopWords = getStopWordList('static/sentiment/stopwords.txt')    
elif _platform == "win32":
    # Windows...
    stopWords = getStopWordList('static//sentiment//stopwords.txt')

# process tweet sentiment thread
###@copy_current_request_context
def process_sentiment_thread(classifier, word_features, fromtweepyDF, sessionuid):
    
    thashtagDF2 =[]
    txycoordinates = []
    tsentimentlist = []
    tpositive_tweet_word_dict = {}
    tnegative_tweet_word_dict = {}
    tnum_positive_tweets = 0
    tnum_negative_tweets = 0
   
    print('Inside Tweet sentiment THREAD' + str(datetime.now()))

    
    ## added to here
    for index,row in fromtweepyDF.iterrows():
        tweet =row['text']
        ## get hashtags
        hashtags = ''
        hashtags = re.findall(r"#(\w+)", tweet)
        for item in hashtags:
               if item <> '' :
                    thashtagDF2.append( item)
        ## username
        ##user = re.findall('@[^\s]+',tweet)
        txycoordinates= classifier.prob_classify(extract_features(tweet.split(),word_features))
        
        #print (txycoordinates._prob_dict)
        
        retweeted_count = row['retweet_count']
        result= classifier.classify(extract_features(tweet.split(),word_features))
        tsentimentlist.append([math.exp(txycoordinates._prob_dict.items()[0][1])*200,
                              math.exp(txycoordinates._prob_dict.items()[1][1])*200, 
                              tweet,result, retweeted_count])
        if result == 'positive':
            tnum_positive_tweets += 1
            for word in getFeatureVector(processTweet(tweet)):
                if not word in tpositive_tweet_word_dict:
                    tpositive_tweet_word_dict[word] = 1
                else:
                    tpositive_tweet_word_dict[word] += 1
            
        else:
            tnum_negative_tweets += 1
            for word in getFeatureVector(processTweet(tweet)):
                if not word in tnegative_tweet_word_dict:
                    tnegative_tweet_word_dict[word] = 1
                else:
                    tnegative_tweet_word_dict[word] += 1

    print('Completed Tweet sentiment THREAD' + str(datetime.now()))
    ## Part 2

    print('After tweet classification THREAD' + str(datetime.now()))

    positive_tweet_word_list = []
    negative_tweet_word_list = []
    num_positive_tweets = 0
    num_negative_tweets = 0 
    
    for key,value in tpositive_tweet_word_dict.iteritems():
           # word_dict = {
           #     "word": key,
           #     "weight": value
           # }
            word_dict = key, value
            positive_tweet_word_list.append(word_dict)
    
    
    for key,value in tnegative_tweet_word_dict.iteritems():
           #  word_dict = {
           #     "word": key,
           #     "weight": value
           # }
            word_dict = key, value
            negative_tweet_word_list.append(word_dict)
            
    print ("Number of Positive tweets = ", num_positive_tweets )
    print ("Number of Negative tweets = ", num_negative_tweets )
    #print ("Positive Tweet Word Dict =", positive_tweet_word_dict)
    #print ("Negative Tweet Word Dict =", negative_tweet_word_dict) 
    
    print ("Positive Tweet Word List =", positive_tweet_word_list)
    
    ##sentimentlist.extend(result) 
    #print sentimentlist
    print('BEFORE writing to JSON Tweet sentiment THREAD' + str(datetime.now()))    
    print('uid --->' + sessionuid)

    write_sentiment_2json(positive_tweet_word_list, negative_tweet_word_list, sessionuid)
    
    columns2 = ['hashtags']
    hashtagDF = pandas.DataFrame(data = thashtagDF2,columns =columns2)

    ## added to here
    
    #return thashtagDF2, txycoordinates, tsentimentlist, tpositive_tweet_word_dict, tnegative_tweet_word_dict
    print('THREAD COMPLETED' + str(datetime.now()))


# process sentiment
def process_sentiment():
    print('INSIDE Process_Sentiment definition')
    print('before getTestDF() {} ' + format(str(datetime.now())))
    fromtweepyDF = getTestDF()
    print('After getTestDF()' + str(datetime.now()))
    print('AFTER getTESTDF call; before opening classifier and bag of words')
    ## Load the classifier
    # we open the file for reading
    if _platform == "linux" or _platform == "linux2":
        # linux
        fileObjectclassfier = open("static/sentiment/classifier",'r') 
        fileObjectbow = open("static/sentiment/bagofwords",'r')
    elif _platform == "win32":
        # Windows...
        fileObjectclassfier = open("static//sentiment//classifier",'r') 
        ## Load the bag of words
        # we open the file for reading
        fileObjectbow = open("static//sentiment//bagofwords",'r')

    # load the object from the file into var b
    classifier = pickle.load(fileObjectclassfier)
    fileObjectclassfier.close()
  
    # load the object from the file into var b
    word_features = pickle.load(fileObjectbow)
    fileObjectbow.close()
    
    print ('FINISHED reading pickle' + str(datetime.now()))

    # variable declaration
        
    #hashtagDF2 =[]
    #xycoordinates = []
    #sentimentlist = []
    #positive_tweet_word_dict = {}
    #negative_tweet_word_dict = {}
    ##columns=['id','user','date','tweet','mentions received','hashtag','sentiment','numberof followers','friends count','retweeted count']
    ##testtweetDF = pandas.DataFrame(data=np.zeros((0,len(columns))),  columns = columns)
   

    print('Before tweet classification' + str(datetime.now()))

    #moved from here

    #moved till here

        ##data = [row['id'], user,row['created_at'],tweet,index,hashtags,result,index,index,row['retweet_count']]
        ##testtweetDF = testtweetDF.T
        ##testtweetDF[index] = data
        ##testtweetDF = testtweetDF.T

    sessionuid = flask.session['uid']
    print('Child thread being submitted' + str(datetime.now()) + sessionuid)
    
    #hashtagDF2, xycoordinates, sentimentlist, positive_tweet_word_dict, negative_tweet_word_dict = process_sentiment_thread(classifier, word_features, fromtweepyDF)
    t1 = Thread(target=process_sentiment_thread, args=(classifier, word_features, fromtweepyDF,sessionuid))
    t1.start()
    
    print('Child submitted and process sentiment ends' + str(datetime.now()))
 


    #print (testtweetDF)
    ##print ( xycoordinates._prob_dict)
    ##print (xycoordinates.max())
    ##print (xycoordinates._prob_dict.items()[1][1])
    ###classifier.show_most_informative_features()


def write_sentiment_2json(data1, data2, sessionuid):
    print('THREAD WRITE SENTIMENT ' + sessionuid +' JSON')
    print('before declaring json file')
    if _platform == "linux" or _platform == "linux2":
                # linux
                filepathjson1 = 'static/tweets/'+sessionuid+'splot1.json' 
                filepathjson2 = 'static/tweets/'+sessionuid+'splot2.json' 

    elif _platform == "win32":
                # Windows...
                filepathjson1 = 'static//tweets//'+sessionuid+'splot1.json' 
                filepathjson2 = 'static//tweets//'+sessionuid+'splot2.json' 
    try:
        print('before readwrite')
        #data1 = positive_tweet_word_list
     
        print('readwrite successful')
        ##pprint.pprint(data) 
        with open(filepathjson1, 'w') as outfile:
            json.dump(data1, outfile)
            #print json.dumps(data)       
            print('JSON file Created!')
    except:
        print('JSON FILE Creation FAILED')
    try:
        print('before readwrite')
     
        #data2 = negative_tweet_word_list
        print('readwrite successful')
        ##pprint.pprint(data) 
        with open(filepathjson2, 'w') as outfile:
            json.dump(data2, outfile)
            #print json.dumps(data)       
            print('JSON file Created!')
    except:
        print('JSON FILE Creation FAILED')