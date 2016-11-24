import cPickle as pickle 
import math

paperData = pickle.load(open('paperData.pkl', 'rb'))
authorFeats = pickle.load(open('authorFeatures.pkl', 'rb'))
venueData = pickle.load(open('venueData.pkl', 'rb'))
topics = pickle.load(open('topics.pkl', 'rb'))
paperFeats = pickle.load(open('paperFeats.pkl', 'rb'))

def getFeatures(paperIdx):
	paperCentricFeats = paperFeats[paperIdx]
	if paperCentricFeats == None:
		print 'paper', paperIdx
	authorCentricFeats = authorFeats[paperIdx]
	if authorCentricFeats == None:
		print 'author', paperIdx
	venueCentricFeats = venueData[paperData[paperIdx][3]]
	if venueCentricFeats == None:
		print 'venue', paperIdx
	return list(paperCentricFeats) + list(authorCentricFeats) + list(venueCentricFeats)