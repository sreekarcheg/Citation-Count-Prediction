from collections import namedtuple, defaultdict
import cPickle as pickle
import random

print "Load paper data"
with open("paperData.pkl", "r") as inFile1:
	paperData = pickle.load(inFile1)
features = pickle.load(open('akshitaFeatures.pkl', 'rb'))

def getLabels(lisIndices,year):
	cit1 = []
	cit5 = []
	cit10 = []
	for paper in lisIndices:
		cit1.append(features[year+1][paper][0])
		cit5.append(features[year+5][paper][0])
		cit10.append(features[year+10][paper][0])
	return cit1, cit5, cit10

def getTrainingData(year):
	#Get all the features of papers in a year
	paperFeatures = []
	for paper in paperData:
		if paperData[paper][2] == year:
			paperFeatures.append([paper, features[year][paper]])
	#Do random shuffling to get test and train set.
	random.shuffle(paperFeatures)
	train_set = paperFeatures[:len(paperFeatures)/2]
	test_set = paperFeatures[len(paperFeatures)/2:]
	y_indexTrain = []
	y_indexTest = []
	x_train = []
	x_test = []
	for feat in train_set:
		y_indexTrain.append(feat[0])
		x_train.append(feat[1][1])
	for feat in test_set:
		y_indexTest.append(feat[0])
		x_test.append(feat[1][1])
	#Get labels for train and test 1, 5, & 10 years ahead.
	y_train1, y_train5, y_train10 = getLabels(y_indexTrain)
	y_test1, y_test5, y_test10 = getLabels(y_indexTest)
	#pickle everything
	with open('X_train.pkl', 'wb') as f1:
		pickle.dump(x_train, f1)
	with open('X_test.pkl', 'wb') as f2:
		pickle.dump(x_test, f2)
	with open('Y_train', 'wb') as f3:
		pickle.dump([y_train1, y_train5, y_train10], f3)
	with open('Y_test.pkl', 'wb') as f4:
		pickle.dump([y_test1, y_test5, y_test10], f4)

		
getTrainingData(2005)