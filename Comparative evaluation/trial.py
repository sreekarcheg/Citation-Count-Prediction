import cPickle as pickle 

paperData = pickle.load(open('paperData.pkl', 'rb'))
print paperData['2']
print paperData['3']
print paperData['4']