authorData = pickle.load(open('authorFeatures.pkl', 'rb'))
def getAuthorFeats(paperIdx):
	authFeats = authorData[paperIdx]
