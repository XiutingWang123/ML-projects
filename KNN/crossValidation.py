# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 22:10:29 2016

@author: yyc
"""
import sys
import csv
import math
from kNeighborsClassifier import KNeighborsClassifier


class LeaveOneOutCV:
	def __init__(self, trainDataSet, k):		
		self.cvError = leaveOneOut(trainDataSet, k)
		
		
	def getError(self):
		return self.cvError
			
	
	
		

def leaveOneOut(trainDataSet,k):	
	trainData = trainDataSet['data']
	labels = trainDataSet['attributes'][-1][1]
	if trainDataSet['attributes'][-1][0] == 'class': 
		classification = True
	elif trainDataSet['attributes'][-1][0] == 'response':
		classification = False
	else:
		raise Exception('Invalid label description: {0}'.format('label must be class or response'))
	
	# split train set and test set	
	n = len(trainData)
	totalError = 0	
	for i in range(0, n):
		trainIdx = []
		trainIdx.extend(range(0, i))
		trainIdx.extend(range(i+1,n))
		cv_train = [trainData[t] for t in trainIdx]
		cv_test = [trainData[i]]
		knn = KNeighborsClassifier(cv_train, cv_test, k, classification, labels)
		predictedData = knn.getPrediction()
		if classification:			
			if predictedData[0][0] != predictedData[0][1]:
				totalError += 1
		else:
			totalError += math.fabs(predictedData[0][0] - predictedData[0][1])
	if classification:			
		return totalError
	else:
		return totalError / n
					
			
USAGE = "<train-set-file> <test-set-file> k"
USAGE_HINT = "k should be an integer."

def getArgs():
	if len(sys.argv) < 3:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)

	try:
		return sys.argv[1], int(sys.argv[2])
	except ValueError:
		print('Usage: {0} {1} ({2})'.format(sys.argv[0], USAGE, USAGE_HINT), file=sys.stderr)
		sys.exit(-1)
		
		
def _main():
	trainSetFile, k = getArgs()
	import arffParser	
	trainDataSet = arffParser.parse(trainSetFile)
	
	loocv = LeaveOneOutCV(trainDataSet, k)
	error = loocv.getError()
	
	print('k = {0}: {1}'.format(k, error))
	
		
		
if __name__ == '__main__':
	_main()




	