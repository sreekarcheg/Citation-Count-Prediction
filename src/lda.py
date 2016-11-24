from __future__ import unicode_literals
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import pickle
import re
import nltk
import sys
import datetime
import cPickle as pickle

def getLDAModel(paperData, numTopics=25, numPasses=2):
    # create English stop words list
    en_stop =  stopwords.words('english')

    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    
    #Get Doc List
    doc_set = [paperData[paper][0] +' ' + paperData[paper][5] for paper in paperData]

    #Save memory
    del paperData

    print datetime.datetime.now(), ': Got data'

    # list for tokenized documents in loop
    texts = []

    # loop through document list
    count = 0
    for i in doc_set:
        # clean and tokenize document string
        raw = i.lower()
        tokens = nltk.word_tokenize(raw)
        # remove stop words from tokens
        stopped_tokens = [i for i in tokens if not i in en_stop]
        # stem tokens
        stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
        # add tokens to list
        texts.append(filter(lambda x: len(x) > 1, stemmed_tokens))
        count += 1
        if count % 100000 == 0:
            print datetime.datetime.now(), ': Stemmed %d papers'%count

    print datetime.datetime.now(), ': Stemmed all papers!'
    
    #Save memory
    del doc_set

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(texts)
    print datetime.datetime.now(),': turned our tokenized documents into a id <-> term dictionary'
    with open('dictionary.pkl', 'wb') as f:
        pickle.dump(dictionary, f)

    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in texts]
    print datetime.datetime.now(), ': converted tokenized documents into a document-term matrix'

    #Save memory
    del texts

    # generate LDA model - Multi Core
    ldamodel =  gensim.models.ldamulticore.LdaMulticore(corpus, num_topics=numTopics, 
        id2word = dictionary, passes=numPasses)

    print datetime.datetime.now(), ': Model trained.'

    ldamodel.save('LDAModel.pkl')
    print datetime.datetime.now(), ': Model saved.'

    return ldamodel

if __name__ == '__main__':
    paperData = None
    print datetime.datetime.now(), ': Started.'
    with open('paperData.pkl', 'rb') as f:
        paperData = pickle.load(f)
    print datetime.datetime.now(), ': Loaded data'
    #Magic number - 100 topics were used in the original paper in SemanticScholar.
    m = getLDAModel(paperData, 100) 
    print m

