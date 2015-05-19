
import re
import nltk
import nltk.classify
import flask, flask.views

import pandas
import random
import json
#import pprint
#import matplotlib.pyplot as plt
#import numpy as np
import pickle
from sys import platform as _platform



def get_words_in_tweets(tweets): 
    all_words = [] 
    for (sentiment, words) in tweets:
      all_words.extend(words.split()) 
    return all_words 

def get_word_features(wordlist): 

    wordlist = nltk.FreqDist(wordlist) 
    word_features = wordlist.keys() 
    return word_features 



#Call tweet_processor
def getTestDF():
    if _platform == "linux" or _platform == "linux2":
        # linux
        tweets_data_path = 'static/tweets/'+flask.session['uid']+'.txt' 
    elif _platform == "win32":
        # Windows...
        tweets_data_path = 'static//tweets//'+flask.session['uid']+'.txt'  ##'tweepy_text.txt'    #QS changed the file name.     

    tweets_data = []
    tweets_file = open(tweets_data_path, "r")

    #tweets = json.load(tweets_file)
    #tweets["text"]

    for line in tweets_file:
        try:
            tweet = json.loads(line)
            ##pprint.pprint(tweet["text"])
            #print tweet
            #tweet["text"]
            tweets_data.append(tweet)
            #print tweets_data
        except:
            continue

    tweetsDF = pandas.DataFrame.from_records(tweets_data)
    ##tweetsDF = pd.read_json(tweet)

    return tweetsDF
#end


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


# extract the training corpus data from the file
def getTrainingTweets(file_path):
    #file_path = 'sentiment1.csv'
    messages = pandas.read_csv(file_path,usecols=[1,2],dtype=str,
                               converters ={'Sentiment': lambda x: 'negative' if x == '0' else 'positive' })

    return messages
# end

# extract the test data from the file
def getTestTweets(file_path):
    if _platform == "linux" or _platform == "linux2":
        # linux
        file_path = 'static/tweets/sentiment2.csv' 
    elif _platform == "win32":
        # Windows...
        file_path = 'static//tweets//sentiment2.csv' 

    messages = pandas.read_csv(file_path,usecols=[1,2],dtype=str,
                               converters ={'Sentiment': lambda x: 'negative' if x == '0' else 'positive' })

    return messages
# end

# from this feature list , do a extract of featurs
def extract_features(document):
    document_words = set(document) 
    features = {} 
    for word in word_features: 
        features['contains(%s)' % word] = (word in document_words)
    return features

# end
#initialize stopWords
stopWords = []




if _platform == "linux" or _platform == "linux2":
    # linux
    st = open('static/sentiment/stopwords.txt', 'r')
    stopWords = getStopWordList('static/sentiment/stopwords.txt')
    final_list = getTrainingTweets("static/sentiment/sentiment1.csv")
    validation_list = getTrainingTweets("static/sentiment/sentiment2.csv")

elif _platform == "win32":
    # Windows...
    st = open('static//sentiment//stopwords.txt', 'r')
    stopWords = getStopWordList('static//sentiment//stopwords.txt')
    final_list = getTrainingTweets("static//sentiment//sentiment1.csv")
    validation_list = getTrainingTweets("static//sentiment//sentiment2.csv")

#Read the training data tweets one by one and process it
#final_list = getTrainingTweets("static//sentiment//sentiment1.csv")
## some statistics on the tweets


#print (final_list.groupby('Sentiment').describe())
## convert the df into list
list_consolidated_tweets = list(final_list.values.tolist())
random.shuffle(list_consolidated_tweets)

## get word features
word_features = get_word_features(get_words_in_tweets(list_consolidated_tweets))  

print("Word Features")
print word_features
tweets_train = []


##for (words, sentiment) in the array pulled in from corpus:
for (sentiment,words) in list_consolidated_tweets: 
    processedTweet = processTweet(words)
    featureVector = getFeatureVector(processedTweet)
    tweets_train.append((featureVector, sentiment));

print("Labelled Tweets")
print tweets_train   




#print (final_list.groupby('Sentiment').describe())
## convert the df into list
list_validation_tweets = list(validation_list.values.tolist())
random.shuffle(list_validation_tweets)


tweets_test = []


##for (words, sentiment) in the array pulled in from corpus:
for (sentiment,words) in list_validation_tweets: 
    processedTweet = processTweet(words)
    featureVector = getFeatureVector(processedTweet)
    tweets_test.append((featureVector, sentiment));

#print tweets_test

training_set=  nltk.classify.apply_features(extract_features, tweets_train)
test_set = nltk.classify.apply_features(extract_features, tweets_test)

classifier = nltk.classify.NaiveBayesClassifier.train(training_set)
## The Acduracy is biased because tweets_train was used to for feature selection 
print('Accuracy: %4.2f' % nltk.classify.accuracy(classifier, test_set)) 
    

filename ="classifier"
fileObject = open(filename,'wb')
##
##
### this writes the object a to the
### file named 'testfile'
pickle.dump(classifier,fileObject)   

### here we close the fileObject
fileObject.close()

filename ="bagofwords"
fileObject = open(filename,'wb')
##
##
### this writes the object a to the
### file named 'testfile'
pickle.dump(word_features,fileObject)   

### here we close the fileObject
fileObject.close()


##print (nltk.classify.util.accuracy(classifier, dict(\\\)))

## call the tweet_processor and get the dataframe of test tweets
## loop through the dataframe and classify each tweet
## create a new list of the test tweet and corresponding sentiment
##

##print (fromtweepyDF)
##hashtagDF2 =[]
##for index,row in fromtweepyDF.iterrows():
##    tweet =row['text']
##    ## get hashtags
##    hashtags = ''
##    hashtags = re.findall(r"#(\w+)", tweet)
##    for item in hashtags:
##           if item <> '' :
##                hashtagDF2.append( item)
##    ## username
##    user = re.findall('@[^\s]+',tweet)
##   
##    
##    
##  
##
##columns2 = ['hashtags']
##hashtagDF = pandas.DataFrame(data = hashtagDF2,columns =columns2)
##
###print(hashtagDF)
###print(hashtagDF.groupby('hashtags').describe())
##print(nltk.classify.accuracy(classifier,tweet))
classifier.show_most_informative_features()





