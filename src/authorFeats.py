from collections import namedtuple, defaultdict
import sys
import cPickle as pickle
from random import randint
import numpy as np
import math
import gensim
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models

NumberOfTopics = 100

paperData =  dict()
#Extract the paper information
print "Load paper data"
with open("paperData.pkl", "r") as inFile1:
	paperData = pickle.load(inFile1)
inFile1.close()
print "load author data"
authorToPapers = pickle.load(open('authorData.pkl', 'rb'))
print "load complete"

en_stop =  stopwords.words('english')
#model = gensim.models.ldamulticore.LdaMulticore.load('LDAModel.pkl')
#dictionary = pickle.load(open('dictionary.pkl', 'rb'))
p_stemmer = PorterStemmer()
paperToTopics = None
with open('paperToTopics.pkl', 'rb') as f:
    paperToTopics = pickle.load(f)

def getTopics(paperIdx):
    #paperText = preProcess(paperData[paperIdx][0] + ' ' + paperData[paperIdx][5])
    #return model[paperText]
    return paperToTopics[paperIdx]

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

def getPaperTopics(authorToPapers, papers):
    authorPaperVector = defaultdict()
    for (idx, author) in enumerate(authorToPapers):
        topicVector = np.zeros(NumberOfTopics)
        for paper in authorToPapers[author]:
            topicVector = np.zeros(100)
            lisOfTopics = getTopics(paper)
            for topic in lisOfTopics:
                topicVector[topic[0]] += 1
        if idx % 50000 == 0:
            print "completed " +str(idx)
        authorPaperVector[author] = topicVector
    return authorPaperVector

def getAuthorDiversities(authorPaperTopics, authorProductivies):
	authorDiversities = defaultdict()
	for author in authorPaperTopics:
		ent = 0
		numberOfPapers = authorProductivies[author]
		authorTopicVector = authorPaperTopics[author]
		for topic in authorTopicVector:
			if topic != 0:
				ent -= (topic/numberOfPapers) * math.log((topic/numberOfPapers))
		authorDiversities[author] = ent
	return authorDiversities

def getAuthorProductivities(authorToPapers, papers):
	authorProductivityCount = defaultdict()
	for author in authorToPapers:
		count = 0
		for paper in authorToPapers[author]:
			if paper in papers:
				count += 1
		authorProductivityCount[author] = count
	return authorProductivityCount

def getCitations(papers):
	paperCitations = defaultdict(set)
	authorCitations = defaultdict(set)
	citationCount = defaultdict()
	i = 0
	for paper in papers:
		for reference in papers[paper][4]:
			paperCitations[reference].add(paper)
	for paper in papers:
		citationCount[paper] = len(paperCitations[paper])
		for author in papers[paper][1]:
			authorCitations[author].add(citationCount[paper])
	return authorCitations

def getH_index(authorCitations):
	authorHIndicies = defaultdict()
	for author in authorCitations:
		citations = list(authorCitations[author])
		citations.sort(reverse=True)
		h = 0
		for cite in citations:
			if cite > h:
				h += 1
		authorHIndicies[author] = h
	return authorHIndicies

def getAuthorSociality(papers):
	authorNOCA = defaultdict(set)
	authorNOCACount = defaultdict()
	for paper in papers:
		for author in papers[paper][1]:
			for others in papers[paper][1]:
				if author != others and others not in authorNOCA[author]:
					authorNOCA[author].add(others)
	for author in authorNOCA:
		authorNOCACount[author] = len(authorNOCA[author])
	return authorNOCACount

def getAllAuthorCentricFeatures():

	data = defaultdict()

	years = []
	for paper in paperData:
		if paperData[paper][2] not in years:
			years.append(paperData[paper][2])
	years.sort()
	print "year cal complete"

	for year in years:
		dataYear = defaultdict()
		papers = dict()
		for paper in paperData:
			if paperData[paper][2] <= year:
				papers[paper] = paperData[paper]

		print year

		print "paper in year Extracted"
		authorProductivies = getAuthorProductivities(authorToPapers,papers)
		print "authorProductivies in year Extracted"
		authorCitations = getCitations(papers)
		print "authorCitations in year Extracted"
		authorHIndicies = getH_index(authorCitations)
		print "authorHIndicies in year Extracted"
		#authorPaperTopics = getPaperTopics(authorToPapers, papers)
		#print "authorPaperTopics in year Extracted"
		#authorDiversities = getAuthorDiversities(authorPaperTopics, authorProductivies)
		#print "authorDiversities in year Extracted"
		authorNOCAs = getAuthorSociality(papers)
		print "authorNOCAs"

		for paper in papers:
			sum_productivity = 0
			max_productivity = 0
			sum_HIndex = 0
			max_HIndex = 0
			sum_diversity = 0
			max_diversity = 0
			sum_NOCA = 0
			max_NOCA = 0
			for author in papers[paper][1]:
				#Calculate the sum and avg of producitvities of all the authors of a paper.
				authorProductivity = authorProductivies[author]
				sum_productivity += authorProductivity
				if max_productivity < authorProductivity:
					max_productivity = authorProductivity
				#Calculate the sum and avg of H-indices of all the authors of a paper.
				authorHIndex = authorHIndicies[author]
				sum_HIndex += authorHIndex
				if max_HIndex < authorHIndex:
					max_HIndex = authorHIndex
				#Calculate the sum and avg of diversities of all the authors of a paper.
				#authorDiversity = authorDiversities[author]
				#sum_diversity += authorDiversity
				#if max_diversity < authorDiversity:
				#	max_diversity = authorDiversity
				#Calculate the sum and avg of Sociability of all the authors of a paper.
				if author not in authorNOCAs:
					authorNOCA = 0
				else:
					authorNOCA = authorNOCAs[author]
				sum_NOCA += authorNOCA
				if max_NOCA < authorNOCA:
					max_NOCA = authorNOCA

			numberOfAuthors = len(papers[paper][1])
			temp = []
			#Feature 1: Add the avg and max productivity values onto the feature list.
			avg_productivity = sum_productivity/numberOfAuthors
			temp.append(avg_productivity)
			temp.append(max_productivity)
			#Feature 2: Add the avg and max H-indices values onto the feature list.
			avg_HIndex = sum_HIndex/numberOfAuthors
			temp.append(avg_HIndex)
			temp.append(max_HIndex)
			#Feature 3: Add the avg and max diversity values onto the feature list.
			#avg_diversity = sum_diversity/numberOfAuthors
			#temp.append(avg_diversity)
			#temp.append(max_diversity)
			#Feature 4: Add the avg and max NOCA values onto the feature list.
			avg_NOCA = sum_NOCA/numberOfAuthors
			temp.append(avg_NOCA)
			temp.append(max_NOCA)
			dataYear[paper] = temp
		data[year] = dataYear
	return data

feat = getAllAuthorCentricFeatures()
with open('authorFeatures.pkl', 'wb') as f:
	pickle.dump(feat, f)

def getAuthorCentricFeatures(paperIdx, year):
	data = pickle.load(open('authorFeatures.pkl', 'rb'))
	return data[year][paperIdx]


'''
years = []
for paper in paperData:
	if paperData[paper][2] not in years:
		years.append(paperData[paper][2])
years.sort()
print "year cal complete"

for year in years:
	print year

'''
