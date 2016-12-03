import math
paperData = pickle.load(open('paperData.pkl', 'rb'))
topics = pickle.load(open('topics.pkl', 'rb'))

def getRDI(paperIdx):
	ref_topics = [0]*100
	for ref in paperData[paperIdx][4]:
		for topic in topics[ref]:
			ref_topics[topic[0]] += 1
	numTopics = 0
	total = 0.0
	for ref in ref_topics:
		if ref>0:
			numTopics += 1
			total = total + (ref*math.log(ref))
	if numTopics == 0:
		return 0
	RDI = total/numTopics
	return -1*RDI


def getTopicDiv(paperIdx):
	topicDiv = [0.0]*100
	for topic in topics[paperIdx]:
		topicDiv[topic[0]] = topic[1]
	return topicDiv


def getPaperFeats(paperIdx):
	paperFeats = [len(paperData[paperIdx][1]), len(paperData[paperIdx][4]), getRDI(paperIdx)] + getTopicDiv(paperIdx)
	return paperFeats

paperFeats = {}
count = 0
for paperIdx in paperData:
	count += 1
	if count%100000==0:
		print 'Parsed', count, 'papers'
	paperFeats[paperIdx] = getPaperFeats(paperIdx)

