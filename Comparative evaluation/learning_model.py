import numpy as np
from sklearn import svm
from nltk.corpus import stopwords
import cPickle as pickle
import nltk
from nltk.stem.porter import PorterStemmer
import gensim
from math import log, fsum
import final

en_stop =  stopwords.words('english')
model = gensim.models.ldamulticore.LdaMulticore.load('LDAModel.pkl')
dictionary = pickle.load(open('dictionary.pkl', 'rb'))
paperToCiters = pickle.load(open('paperToCiters.pkl', 'rb'))
venueToPapers = pickle.load(open('venueData.pkl', 'rb'))
# authorFeats = pickle.load(open('authorFears.pkl', 'rb'))
authorData = pickle.load(open('authorFeatures.pkl', 'rb'))




def longTermVenuePrestige(venue, paperIdx):
	year = paperData[paperIdx][3]
	return sum([len(paperToCiters[paper]) for paper in venueToPapers[venue] if paperData[paper][3] <= year])

def shortTermVenuePrestige(venue, year):
	recentPapers = [paper for paper in venueToPapers[venue] if paperData[paper][2] >= year - 2]
	numCit = sum([len(paperToCiters[paper]) for paper in recentPapers])
	return numCit / len(recentPapers)

def venueDiversity(venue):
	topics = [0] * 100
	ret = 0
	for paper in venueToPapers[venue]:
		for t, p in getTopics(paper):
			topics[t] += p
	l = len(venueToPapers[venue])
	topics = [x/l for x in topics]
	logs = [-log(p) if p != 0 else 0 for p in topics]
	ent = [topics[i] * logs[i] for i in range(100)]
	return fsum(ent)



def getFeatures(paperIdx):
	paperFeats = [len(paperData[paperIdx][1]), len(paperData[paperIdx][4]), getRDI(paperIdx, 100)] + getTopicDiv(paperIdx)
	venue = paperData[paperIdx][3]
	venueFeats = [longTermVenuePrestige(venue), shortTermVenuePrestige(venue, paperData[paperIdx][2]), venueDiversity(venue)]
	authFeats = authorData[paperIdx]
	return paperFeats + venueFeats + authorFeats

def getRDI(paperIdx, numTopics):
	topics = []
	for ref in paperData[paperIdx][4]:
		for ref_topics in getTopics(ref):
			topics.append(ref_topics[0])
	return len(topics)/numTopics

def getTopicDiv(paperIdx):
	topicDiv = [0.0]*100
	for topic in getTopics(paperIdx):
		topicDiv[topic[0]] = topic[1]
	return topicDiv

def getTopics(paperIdx):
	paperText = preProcess(paperData[paperIdx][0] + ' ' + paperData[paperIdx][5])
	return model[paperText]

def preProcess(paperText):
    raw = paperText.lower()
    tokens = nltk.word_tokenize(raw)
    # remove stop words from tokens
    stopped_tokens = [i for i in tokens if not i in en_stop]
    # stem tokens
    stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
    # add tokens to list
    tokens = filter(lambda x: len(x) > 1, stemmed_tokens)
    return dictionary.doc2bow(tokens)


def getCategory(paper):
	if paper in PeakInit:
		return 0
	if paper in PeakMul:
		return 1
	if paper in PeakLate:
		return 2
	if paper in MonDec:
		return 3
	if paper in MonIncr:
		return 4
	if paper in Oth:
		return 5

def trainSVM(trainData):
	X = [getFeatures(paper) for paper in trainData]
	Y = [getCategory(paper) for paper in trainData]
	clf = svm.SVC(decision_function_shape='ovo')
	clf.fit(X, Y) 
	