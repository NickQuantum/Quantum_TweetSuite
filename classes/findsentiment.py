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


# process sentiment
def process_sentiment():
    fromtweepyDF = getTestDF()
    
    ## Load the classifier
    # we open the file for reading
    if _platform == "linux" or _platform == "linux2":
        # linux
        fileObject = open("static/sentiment/classifier",'r') 
        fileObject = open("static/sentiment/bagofwords",'r')
    elif _platform == "win32":
        # Windows...
        fileObject = open("static//sentiment//classifier",'r') 
        ## Load the bag of words
        # we open the file for reading
        fileObject = open("static//sentiment//bagofwords",'r')

    # load the object from the file into var b
    classifier = pickle.load(fileObject)
    fileObject.close()
  
    # load the object from the file into var b
    word_features = pickle.load(fileObject)
    fileObject.close()
    
    
    
    
    hashtagDF2 =[]
    xycoordinates = []
    sentimentlist = []
    positive_tweet_word_dict = {}
    negative_tweet_word_dict = {}
    positive_tweet_word_list = []
    negative_tweet_word_list = []
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
            for word in getFeatureVector(processTweet(tweet)):
                if not word in positive_tweet_word_dict:
                    positive_tweet_word_dict[word] = 1
                else:
                    positive_tweet_word_dict[word] += 1
            
        else:
            num_negative_tweets += 1
            for word in getFeatureVector(processTweet(tweet)):
                if not word in negative_tweet_word_dict:
                    negative_tweet_word_dict[word] = 1
                else:
                    negative_tweet_word_dict[word] += 1
        
        
       
        
            
        data = [row['id'], user,row['created_at'],tweet,index,hashtags,result,index,index,row['retweet_count']]
        testtweetDF = testtweetDF.T
        testtweetDF[index] = data
        testtweetDF = testtweetDF.T
    
    for key,value in positive_tweet_word_dict.iteritems():
            word_dict = {
                "word": key,
                "weight": value
            }
            positive_tweet_word_list.append(word_dict)
    
    
    for key,value in negative_tweet_word_dict.iteritems():
            word_dict = {
                "word": key,
                "weight": value
            }
            negative_tweet_word_list.append(word_dict)
            
    print ("Number of Positive tweets = ", num_positive_tweets )
    print ("Number of Negative tweets = ", num_negative_tweets )
    #print ("Positive Tweet Word Dict =", positive_tweet_word_dict)
    #print ("Negative Tweet Word Dict =", negative_tweet_word_dict) 
    
    #print ("Positive Tweet Word List =", positive_tweet_word_list)
    
    ##sentimentlist.extend(result) 
    #print sentimentlist
    
    if _platform == "linux" or _platform == "linux2":
                # linux
                filepathjson1 = 'static/tweets/'+flask.session['uid']+'splot1.json' 
                filepathjson2 = 'static/tweets/'+flask.session['uid']+'splot2.json' 

    elif _platform == "win32":
                # Windows...
                filepathjson1 = 'static//tweets//'+flask.session['uid']+'splot1.json' 
                filepathjson2 = 'static//tweets//'+flask.session['uid']+'splot2.json' 
    try:
        print('before readwrite')
        data1 = positive_tweet_word_list
     
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
     
        data2 = negative_tweet_word_list
        print('readwrite successful')
        ##pprint.pprint(data) 
        with open(filepathjson2, 'w') as outfile:
            json.dump(data2, outfile)
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
