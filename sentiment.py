import re
import base64
import csv
import gc
import time
import nltk
try:
   import cPickle as pickle
except:
   import pickle

import numpy as np

from sklearn.decomposition import RandomizedPCA
from sklearn.decomposition import SparseCoder
from sklearn.decomposition import DictionaryLearning

from sklearn.linear_model import LogisticRegression
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier

from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import BernoulliRBM

import skimage.io as io
import skimage.transform as trans


from nltk.corpus import stopwords


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
def getStopWordList():
    #read the stopwords file and build a list
    stopWords = stopwords.words('english')
    stopWords.append('AT_USER')
    stopWords.append('URL')

    return stopWords
#end

#start getfeatureVector
def getFeatureVector(tweet):
    stopWords = getStopWordList()
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
        if(w in stopWords):
            continue
        else:
            featureVector.append(w.lower())
    return featureVector
#end

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in feature_list:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

def getSVMFeatureVectorAndLabels(tweets, featureList):
    sortedFeatures = sorted(featureList)
    map = {}
    feature_vector = []
    labels = []
    for t in tweets:
        label = 0
        map = {}
        #Initialize empty map
        for w in sortedFeatures:
            map[w] = 0

        tweet_words = t[0]
        tweet_opinion = t[1]
        #Fill the map
        for word in tweet_words:
            #process the word (remove repetitions and punctuations)
            word = replaceTwoOrMore(word)
            word = word.strip('\'"?,.')
            #set map[word] to 1 if word exists
            if word in map:
                map[word] = 1
        #end for loop
        values = map.values()
        feature_vector.append(values)
        labels.append(tweet_opinion)
    #return the list of feature_vector and labels
    return {'feature_vector' : feature_vector, 'labels': labels}
#end

#############################################################

tweets = []
feature_list = []

#Read the tweets one by one and process it
f = open('training.1600000.processed.noemoticon.csv', 'r')
reader = csv.reader(f, 'excel')

reader.next()
counter = 0
for row in reader:
    counter += 1
    if counter <= 12000 or (counter >= 800000 and counter <= 812000 ):
        print counter
        feature_vector = getFeatureVector(processTweet(row[5])) 
        tweets.append((feature_vector, row[0]))
        feature_list.extend(feature_vector)
f.close()

feature_list = list(set(feature_list))

with open('feature_list.bin', 'wb') as fp:
    pickle.dump(feature_list, fp)
fp.close()

training_set = nltk.classify.util.apply_features(extract_features, tweets)

Start = time.time() 
print Start
NBClassifier = nltk.NaiveBayesClassifier.train(training_set)
End = time.time()
print End
print "elapsed time: ", End-Start

testTweet = 'Congrats @ravikiranj, i heard you wrote a new tech post on sentiment analysis'
processedTestTweet = processTweet(testTweet)
print NBClassifier.classify(extract_features(getFeatureVector(processedTestTweet)))

with open('sentiment_classifier.bin', 'wb') as fp:
    pickle.dump(NBClassifier, fp)
fp.close()