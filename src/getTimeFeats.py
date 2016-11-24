import cPickle as pickle

authorFeats = None
paperData = None
venueFeats = None
paperFeats = None
venueToPapers = None
paperToCiters = None

with open('authorFeatures.pkl', 'rb') as f:
	authorFeats = pickle.load(f)
with open('paperData.pkl', 'rb') as f:
	paperData = pickle.load(f)
with open('venueFeats.pkl', 'rb') as f:
	venueFeats = pickle.load(f)
with open('paperFeats.pkl', 'rb') as f:
	paperFeats = pickle.load(f)
with open('venueToPapers.pkl', 'rb') as f:
        venueToPapers = pickle.load(f)
with open('paperToCiters.pkl', 'rb') as f:
        paperToCiters = pickle.load(f)

print 'Loaded stuff!'

def shortTermVenuePrestige(venue, year):
    recentPapers = [paper for paper in venueToPapers[venue] if paperData[paper][2] >= year - 2]
    numCit = sum([len(paperToCiters[paper]) for paper in recentPapers])
    if not recentPapers:
        return 0
    return numCit / len(recentPapers)

def genFeatureVecs(paperIdx):
	data = paperData[paperIdx]		
	year = data[2]
	cits = data[4]
        for i in range(5):
                yr = year + i
                citsThisYr = filter(lambda x: paperData[x][2] == yr, cits)
                if len(citsThisYr) > 0:
                        print yr, paperIdx
                try:
                        yield paperFeats[paperIdx] + authorFeats[yr][paperIdx] + venueFeats[paperData[paperIdx][3]][yr], i, len(citsThisYr)
                except Exception:
                        vf = venueFeats[paperData[paperIdx][3]]
                        y = yr
                        while vf.get(y) is None:
                                y -= 1
                        lt, st, vd = vf[y]
                        try:
                                yield paperFeats[paperIdx] + authorFeats[yr][paperIdx] + [lt,  shortTermVenuePrestige(paperData[paperIdx][3], y), vd], i, len(citsThisYr)
                        except Exception:
                                raise StopIteration

def getFeatures():
	feats = dict()
        count = 0
	for paperIdx in paperData:
		count += 1
                feats[paperIdx] = list(genFeatureVecs(paperIdx))
                if count % 100000 == 0:
                        print 'Parsed %d papers!'%count
	return feats

if __name__ == '__main__':
	with open('timeData.pkl', 'wb') as f:
		pickle.dump(getFeatures(), f)

