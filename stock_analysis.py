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


f = open("sentiment_classifier.bin", "rb")
sentiment_classifier = pickle.load(f)
f.close()

files = ['aapl.csv', 'goog.csv', 'tsla.csv', 'twtr.csv']

mp = {}
count = {}

for fil in files:
	f = open(fil,"r")
	reader = csv.reader(f, 'excel')
	reader.next()

	for row in reader:
		if row[0] in mp:
			mp[row[0]] += sentiment_classifier.classify(extract_features(getFeatureVector(processTweet(row[1]))))
			count[row[0]] += 1
		else:
			mp[row[0]] = sentiment_classifier.classify(extract_features(getFeatureVector(processTweet(row[1]))))
			count[row[0]] =1.0



