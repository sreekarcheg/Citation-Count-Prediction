from sklearn import datasets, linear_model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
import numpy as np
import cPickle as pickle

n_neighbors = 3

x_train = pickle.load(open('X_train.pkl', 'rb'))
x_test = pickle.load(open('X_test.pkl', 'rb'))
y_train = pickle.load(open('Y_train.pkl', 'rb'))
y_test = pickle.load(open('Y_test.pkl', 'rb'))

print len(x_train)
print len(x_test)
print len(y_train[0])
print len(y_test[0])

def linearModel(y):
	regr = linear_model.LinearRegression()
	regr.fit(x_train, y)
	return regr.predict(x_test)

def knnModel(y):
	knn = KNeighborsClassifier(n_neighbors)
	knn.fit(x_train, y)
	return knn.predict(x_test)

def cartModel(y):
	regressor = DecisionTreeRegressor(random_state=0)
	regressor.fit(x_train, y)
	return regressor.predict(x_test)

def svrModel(y):
	print "In Model"
	# clf = SVR(kernel='poly', C=1e3, degree=2)
	# clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
	clf = SVR(cache_size=7000)
	print "Model created"
	clf.fit(x_train, y)
	print "Training complete"
	return clf.predict(x_test)

def calR2(y_true, y_pred):
	""" Return R^2 where x and y are array-like."""
	# slope, intercept, r_value, p_value, std_err = stats.linregress(prediction, y)
	# return r_value**2
	return r2_score(y_true, y_pred) 

def calMSE(y,prediction):
	return np.mean((prediction - y) ** 2)

# print "\n--------------------"
# print "    Linear Model"
# print "--------------------"
# predLin1 = linearModel(y_train[0])
# R2Lin1 = calR2(y_test[0], predLin1)
# print ("1 year: R2 = %.4f"%R2Lin1)
# MSELin1 = calMSE(y_test[0], predLin1)
# print ("1 year: MSE = %.4f"%MSELin1)

# predLin5 = linearModel(y_train[1])
# R2Lin5 = calR2(y_test[1], predLin5)
# print ("5 year: R2 = %.4f"%R2Lin5)
# MSELin5 = calMSE(y_test[1], predLin5)
# print ("5 year: MSE = %.4f"%MSELin5)

# predLin10 = linearModel(y_train[2])
# R2Lin10 = calR2(y_test[2], predLin10)
# print ("10 year: R2 = %.4f"%R2Lin10)
# MSELin10 = calMSE(y_test[2], predLin10)
# print ("10 year: MSE = %.4f"%MSELin10)


# print "\n--------------------"
# print "     KNN Model"
# print "--------------------"
# predKnn1 = knnModel(y_train[0])
# R2Knn1 = calR2(y_test[0], predKnn1)
# print ("1 year: R2 = %.4f"%R2Knn1)
# MSEKnn1 = calMSE(y_test[0], predKnn1)
# print ("1 year: MSE = %.4f"%MSEKnn1)

# predKnn5 = knnModel(y_train[1])
# R2Knn5 = calR2(y_test[1], predKnn5)
# print ("5 year: R2 = %.4f"%R2Knn5)
# MSEKnn5 = calMSE(y_test[1], predKnn5)
# print ("5 year: MSE = %.4f"%MSEKnn5)

# predKnn10 = knnModel(y_train[2])
# R2Knn10 = calR2(y_test[2], predKnn10)
# print ("10 year: R2 = %.4f"%R2Knn10)
# MSEKnn10 = calMSE(y_test[2], predKnn10)
# print ("10 year: MSE = %.4f"%MSEKnn10)


# print "\n--------------------"
# print "    CART Model"
# print "--------------------"
# predCart1 = cartModel(y_train[0])
# R2Cart1 = calR2(y_test[0], predCart1)
# print ("1 year: R2 = %.4f"%R2Cart1)
# MSECart1 = calMSE(y_test[0], predCart1)
# print ("1 year: MSE = %.4f"%MSECart1)

# predCart5 = cartModel(y_train[1])
# R2Cart5 = calR2(y_test[1], predCart5)
# print ("5 year: R2 = %.4f"%R2Cart5)
# MSECart5 = calMSE(y_test[1], predCart5)
# print ("5 year: MSE = %.4f"%MSECart5)

# predCart10 = cartModel(y_train[2])
# R2Cart10 = calR2(y_test[2], predCart10)
# print ("10 year: R2 = %.4f"%R2Cart10)
# MSECart10 = calMSE(y_test[2], predCart10)
# print ("10 year: MSE = %.4f"%MSECart10)


print "\n--------------------"
print "     SVR Model"
print "--------------------"
predSvr1 = svrModel(y_train[0])
print "prediction received"
R2Svr1 = calR2(y_test[0], predSvr1)
print ("1 year: R2 = %.4f"%R2Svr1)
MSESvr1 = calMSE(y_test[0], predSvr1)
print ("1 year: MSE = %.4f"%MSESvr1)

predSvr5 = svrModel(y_train[1])
print "prediction received"
R2Svr5 = calR2(y_test[1], predSvr5)
print ("5 year: R2 = %.4f"%R2Svr5)
MSESvr5 = calMSE(y_test[1], predSvr5)
print ("5 year: MSE = %.4f"%MSESvr5)

predSvr10 = svrModel(y_train[2])
print "prediction received"
R2Svr10 = calR2(y_test[2], predSvr10)
print ("10 year: R2 = %.4f"%R2Svr10)
MSESvr10 = calMSE(y_test[2], predSvr10)
print ("10 year: MSE = %.4f"%MSESvr10)
