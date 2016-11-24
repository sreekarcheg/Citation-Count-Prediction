import cPickle as pickle
import seq2seq
from seq2seq.models import SimpleSeq2Seq
import numpy as np
import os

def createModel():
    model = SimpleSeq2Seq(input_dim= 112, output_length= 1, output_dim= 5, depth=1)
    model.compile(loss='mse', optimizer='rmsprop')
    return model

def trainModel(model, trainX, trainY):
    model.fit(trainX, trainY, batch_size=1024, validation_split=0.33, nb_epoch=30, show_accuracy=True, verbose=1)
    saveModel(model)

def saveModel(model):
    file_name = 'weights.dat'
    # file_name = os.path.abspath(os.path.join(__file__, os.pardir)) + '/' + file_name
    model.save_weights('weights.dat')

def loadModel(file_name):
    model = createModel()
    model.load_weights(file_name)


timeData = pickle.load(open('timeData.pkl', 'rb'))
paperData = pickle.load(open('paperData.pkl', 'rb'))

count = 0
completeFeats = []
for paperIdx in paperData:
    count += 1
    L = timeData[paperIdx]
    if len(L)==5:
        completeFeats.append(paperIdx)

feats = {}
labels = {}
for paperIdx in completeFeats:
    L = timeData[paperIdx]
    M = L[0][0]
    feats[paperIdx] = M
    N = L[0][2] , L[1][2] , L[2][2] , L[3][2] , L[4][2]
    labels[paperIdx] = N

X = []
Y = []
for paperIdx in completeFeats:
    X.append(feats[paperIdx])
    Y.append(labels[paperIdx])
X = np.array(X)
Y = np.array(Y)

train_size = int(len(feats) * 0.67)
test_size = len(feats) - train_size

trainX = X[0:train_size, ...]
trainY = Y[0:train_size, ...]
testX = X[train_size:len(feats), ...]
testY = Y[train_size:len(feats), ...]
trainY = np.reshape(trainY, (trainY.shape[0], 1, trainY.shape[1]))
testY = np.reshape(testY, (testY.shape[0], 1, testY.shape[1]))

model = createModel()
trainModel(model, trainX, trainY)
predictedY = model.predict(testX, verbose=1)
print 'MSE on test set:', errorMetrics(testY, predictedY)

def errorMetrics(y_true, y_pred):
    from sklearn.metrics import mean_squared_error
    mse = mean_squared_error(y_true, y_pred)
    return mse
