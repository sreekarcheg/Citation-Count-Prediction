from collections import defaultdict
import cPickle as pickle

def getPeaks(L):
	L = [0, 0] + L + [0, 0]
	smoothedL = [sum(L[i-2:i+3])/5.0 for i in range(2, len(L)-2)] #5-year smoothing
	if sum(smoothedL) == 0.0:
		return [False]*6
	smoothedL = [x/max(smoothedL) for x in smoothedL] #Normalizing by max citation count
	peaks = [smoothedL[0]>smoothedL[1]] + [(smoothedL[i]>smoothedL[i-1] and smoothedL[i] > smoothedL[i+1]) for i in range(1, len(smoothedL)-1)] + [smoothedL[-1]>smoothedL[-2]]
	return peaks

citationByYearIdx = {}
def getCitationByYearIdx(paperIdx, citationIdx):
	global citationByYearIdx
	citationByYearIdx[paperIdx] = [0]*6
	yearOfPaper = paperData[paperIdx][2]
	for citation in citationIdx[paperIdx]:
		yearOfCitation = paperData[citation][2]
		diffInYears = int(yearOfCitation) - int(yearOfPaper)
		# assert diffInYears >= 0, 'The paper {} seems to be cited by {} before it has been published!'.format(citation, paperIdx)
		if diffInYears<=5 and diffInYears>=0:
			citationByYearIdx[paperIdx][diffInYears] += 1
	return citationByYearIdx



def makeCitationIdx(paperData):
	citationIdx = defaultdict(set)
	for count, idx in enumerate(paperData):
		for citation in paperData[idx][4]:
			citationIdx[citation].add(idx)
		if count % 100000:
			print 'Parsed', count, 'papers'
	with open('citationIdx.pkl', 'wb') as f:
		pickle.dump(citationIdx, f)
	return citationIdx

def getCitationIdx(paperData):
	return pickle.load(open('citationIdx.pkl', 'rb'))


def ruleBasedClassification(paperData, citationByYearIdx, citationIdx):
	PeakInit, PeakMul, PeakLate, MonDec, MonIncr, Oth = [], [], [], [], [], []
	for paperIdx in paperData:
		L = citationIdx[paperIdx]
		if len(L)/5.0 < 1:
			Oth.append(paperIdx)
			continue
		peaks = getPeaks(citationByYearIdx[paperIdx])
		if peaks.count(True) > 0:
			PeakMul.append(paperIdx)
		else:
			if peaks[:5].count(True) > 0:
				if peaks[0] == true:
					MonDec.append(True)
				else: 
					PeakInit.append(True)
			else:
				if peaks[5] == True:
					MonIncr.append(True)
				else:
					PeakLate.append(True)


	return PeakInit, PeakMul, PeakLate, MonDec, MonIncr, Oth





PeakInit = defaultdict(set)
PeakMul = defaultdict(set)
PeakLate = defaultdict(set)
MonDec = defaultdict(set)
MonIncr = defaultdict(set)
Oth = defaultdict(set)