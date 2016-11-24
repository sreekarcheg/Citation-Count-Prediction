import cPickle as pickle
from math import fsum, log
#from getTopic import getTopics

venueToPapers = None
paperData = None
paperToCiters = None
paperTopics = None

with open('paperData.pkl', 'rb') as f:
    paperData = pickle.load(f)
with open('venueToPapers.pkl', 'rb') as f:
    venueToPapers = pickle.load(f)
with open('paperToCiters.pkl', 'rb') as f:
    paperToCiters = pickle.load(f)
with open('paperTopics.pkl', 'rb') as f:
    paperTopics = pickle.load(f)

print 'Loaded stuff!'

def longTermVenuePrestige(venue, year):
    count = 0
    s = 0
    for paperIdx in venueToPapers[venue]:
        if paperData[paperIdx][2] <= year:
            count += 1
            for cit in paperToCiters[paperIdx]:
                if paperData[cit][2] <= year:
                    s += 1
    if s == 0:
        return 0
    return s/count

def shortTermVenuePrestige(venue, year):
    recentPapers = [paper for paper in venueToPapers[venue] if paperData[paper][2] >= year - 2]
    numCit = sum([len(paperToCiters[paper]) for paper in recentPapers])
    if not recentPapers:
        return 0
    return numCit / len(recentPapers)

def venueDiversity(venue, year):
    topics = [0] * 100
    l = 0
    for paperIdx in venueToPapers[venue]:
        if paperData[paperIdx][2] <= year:
            for t, p in paperTopics[paperIdx]:
                topics[t] += p
                l += 1
    if l == 0:
        return 0
    topics = [x/l for x in topics]
    logs = [-log(p) if p != 0 else 0 for p in topics]
    ent = [topics[i] * logs[i] for i in range(100)]
    return fsum(ent)

def getVenueFeats():
    venueFeats = dict()
    count = 0
    for venue in venueToPapers:
        venueFeats[venue] = dict()
        yrs = {paperData[idx][2] for paperIdx in venueToPapers[venue] for idx in paperData[paperIdx][4]}
        yrs = yrs.union({paperData[paperIdx][2] for paperIdx in venueToPapers[venue]})
        if len(yrs) == 0:
            print venue
        maxYr = max(yrs)
        minYr = min(yrs)
        for year in range(minYr, maxYr + 1):
            venueFeats[venue][year] = [longTermVenuePrestige(venue, year), shortTermVenuePrestige(venue, year), venueDiversity(venue, year)]
        count += 1
        if count % 100 == 0:
            print 'Done with %d venues'%count

    return venueFeats

if __name__ == '__main__':
    with open('venueFeats.pkl', 'wb') as f:
        pickle.dump(getVenueFeats(), f)
