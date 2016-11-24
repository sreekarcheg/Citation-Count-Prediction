import gensim
import cPickle as pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import re

en_stop =  stopwords.words('english')
model = gensim.models.ldamulticore.LdaMulticore.load('LDAModel.pkl')
dictionary = pickle.load(open('dictionary.pkl', 'rb'))
paperData = None
with open('paperData.pkl', 'rb') as f:
        paperData = pickle.load(f)
p_stemmer = PorterStemmer()

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

if __name__ == '__main__':
        print 'Done loading stuff!'
        d = dict()
        i = 0
        for paperIdx in paperData:
                d[paperIdx] = getTopics(paperIdx)
                i += 1
                if i % 1000 == 0:
                        print 'Done with %d papers!'%i
        with open('paperTopics.pkl', 'wb') as f:
                pickle.dump(d, f)
