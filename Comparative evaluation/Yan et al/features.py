from collections import namedtuple, defaultdict
import sys
import cPickle as pickle
from random import randint
import numpy as np 
import math
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
# from getTopic import getTopics

NumberOfTopics = 100

paperData =  None
#Extract the paper information
print "Load paper data"
with open("paperData.pkl", "r") as inFile1:
	paperData = pickle.load(inFile1)
print "load author data"
authorToPapers = pickle.load(open('authorData.pkl', 'rb'))
print "load venue data"
venueToPapers = pickle.load(open('venueToPapers.pkl', 'rb'))
print "load topic data"
paperTopics = pickle.load(open('topics.pkl', 'rb'))
print "load complete"

def getTopicPopularity(paperCitations):
	topicPopularity = defaultdict()
	for paper in paperTopics:
		topics = paperTopics[paper]
		for topic in topics:
			if paper in paperCitations:
				if topic not in topicPopularity:
					topicPopularity[topic[0]] = paperCitations[paper]*topic[1]
				else:
					topicPopularity[topic[0]] += paperCitations[paper]*topic[1]
	return topicPopularity

def getTopicDiversities():
	topicDiversities = defaultdict()
	for paper in paperTopics:
		topics = paperTopics[paper]
		entropy = 0
		for topic in topics:
			entropy -= topic[1]*math.log(topic[1])
		topicDiversities[paper] = entropy
	return topicDiversities

def getAuthorProductivities(authorToPapers, papers):
	authorProductivityCount = defaultdict()
	for author in authorToPapers:
		authorProductivityCount[author] = len(authorToPapers[author])
	return authorProductivityCount

def getPaperCitations(papers):
	paperCitations = defaultdict(set)
	citationCount = defaultdict()
	for paper in papers:			
		for reference in papers[paper][4]:
			paperCitations[reference].add(paper)
	for paper in papers:
		citationCount[paper] = len(paperCitations[paper])
	return citationCount

def getAuthorCitations(papers, citationCount):
	authorCitations = defaultdict(set)
	i = 0	
	for paper in papers:
		for author in papers[paper][1]:
			authorCitations[author].add(citationCount[paper])
	return authorCitations

#fix for papers that are not there
def getVenueCitations(papers, paperCitations):
	venueCitations = defaultdict(set)
	for venue in venueToPapers:
		for paper in venueToPapers[venue]:
			if paper in paperCitations:
				venueCitations[venue].add(paperCitations[paper])
	return venueCitations

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

def getRanks(dictionary):
	print "\tRanks"
	lis = []
	ranks = defaultdict()
	for element in dictionary:
		lis.append(dictionary[element])
	lis.sort(reverse=True)
	for element in dictionary:
		ranks[element] = lis.index(dictionary[element]) + 1
	return ranks

def getAllAuthorCentricFeatures():

	years = []
	for paper in paperData:
		if paperData[paper][2] not in years:
			years.append(paperData[paper][2])
	years.sort()
	print "year cal complete"

	features = defaultdict()

	topicDiversities = getTopicDiversities()

	for year in years:
		papers = dict()
		for paper in paperData:
			if paperData[paper][2] <= year:
				papers[paper] = paperData[paper]

		print year

		recency = 2018 - year

		dataYear = defaultdict()

		print "paper in year Extracted"
		authorProductivies = getAuthorProductivities(authorToPapers,papers)
		print "authorProductivies in year Extracted"
		paperCitations = getPaperCitations(papers)
		authorCitations = getAuthorCitations(papers, paperCitations)
		venueCitations = getVenueCitations(papers, paperCitations)
		print "authorCitations in year Extracted"
		authorHIndicies = getH_index(authorCitations)
		print "authorHIndicies in year Extracted"
		authorAvgCitations = defaultdict()
		for author in authorCitations:
			authorAvgCitations[author] = sum(authorCitations[author])*1.0/len(authorCitations[author])
		authorRanks = getRanks(authorAvgCitations)
		print "author ranks Extracted"
		venueAvgCitations = defaultdict()
		for venue in venueCitations:
			venueAvgCitations[venue] = sum(venueCitations[venue])*1.0/len(venueCitations[venue])
		venueRanks = getRanks(venueAvgCitations)
		print "venue ranks Extracted"
		authorNOCAs = getAuthorSociality(papers)
		print "authorNOCAs Extracted"
		topicPopularity = getTopicPopularity(paperCitations)
		topicRanks = getRanks(topicPopularity)
		print "topicPopularity Extracted"

		for paper in papers:
			sum_productivity = 0
			first_productivity = 0
			sum_HIndex = 0
			first_HIndex = 0
			sum_authorRank = 0
			first_authorRank = 0
			sum_NOCA = 0
			first_NOCA = 0
			idx = 0
			ranks = 0
			topicRank = -1
			try:
				for topic in paperTopics[paper]:
					ranks += topicRanks[topic[0]]
				topicRank = ranks*1.0/len(paperTopics[paper])
			except ZeroDivisionError:
				print paper
				topicRank = 100
			for author in papers[paper][1]:
				#Calculate the sum and avg of producitvities of all the authors of a paper.
				authorProductivity = authorProductivies[author]
				sum_productivity += authorProductivity
				if idx == 0:
					first_productivity = authorProductivity
				#Calculate the sum and avg of H-indices of all the authors of a paper.
				authorHIndex = authorHIndicies[author]
				sum_HIndex += authorHIndex
				if idx == 0:
					first_HIndex = authorHIndex
				#Calculate the sum and avg of ranks of all the authors of a paper.
				authorRank = authorRanks[author]
				sum_authorRank += authorRank
				if idx == 0:
					first_authorRank = authorRank
				#Calculate the sum and avg of Sociability of all the authors of a paper.
				if author not in authorNOCAs:
					authorNOCA = 0
				else:
					authorNOCA = authorNOCAs[author]
				sum_NOCA += authorNOCA
				if idx == 0:
					first_NOCA = authorNOCA		

			numberOfAuthors = len(papers[paper][1])
			avg_productivity = sum_productivity*1.0/numberOfAuthors
			avg_HIndex = sum_HIndex*1.0/numberOfAuthors
			avg_authorRank = sum_authorRank*1.0/numberOfAuthors
			avg_NOCA = sum_NOCA*1.0/numberOfAuthors

			dataYear[paper] = [paperCitations[paper],[topicRank, topicDiversities[paper], recency, first_HIndex, avg_HIndex, first_authorRank, avg_authorRank, first_productivity, avg_productivity, first_NOCA, avg_NOCA, venueRanks[papers[paper][3]]]]
		features[year] = dataYear
		print "Papers so far: " + str(len(dataYear))
	return features

feat = getAllAuthorCentricFeatures()
with open('akshitaFeatures.pkl', 'wb') as f:
	pickle.dump(feat, f)

def getAuthorCentricFeatures(paperIdx):
	data = pickle.load(open('akshitaFeatures.pkl', 'rb'))
	return data[paperIdx]
