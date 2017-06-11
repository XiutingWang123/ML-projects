# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:41:55 2016

@author: yyc
"""

import sys
import arff
import math
from kNeighborsClassifier import KNeighborsClassifier


USAGE = "<train-set-file> <test-set-file> k"
USAGE_HINT = "k should be an integer."

def getArgs():
	if len(sys.argv) < 4:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)

	try:
		return sys.argv[1], sys.argv[2], int(sys.argv[3])
	except ValueError:
		print("Usage: {0} {1} ({2})".format(sys.argv[0], USAGE, USAGE_HINT), file=sys.stderr)
		sys.exit(-1)

def main():
	trainSetFile, testSetFile, k = getArgs()
	trainDataSet = arff.load(open(trainSetFile, 'r'))
	testDataSet = arff.load(open(testSetFile, 'r'))
	trainData = trainDataSet['data']
	testData = testDataSet['data']
	labels = trainDataSet['attributes'][-1][1]
	
	if trainDataSet['attributes'][-1][0] == 'class': 
		classification = True
	elif trainDataSet['attributes'][-1][0] == 'response':
		classification = False
	else:
		raise Exception('Invalid label description: {0}'.format('label must be class or response'))
	
	knn = KNeighborsClassifier(trainData, testData, k, classification, labels)
	predictedData = knn.getPrediction();
	
	print('k value : {0}'.format(k))	
	if classification:
		numCorrect = 0
		acc = 0
		for row in predictedData:
			print('Predicted class : {0}\tActual class : {1}'.format(row[0], row[1]))
			if row[0] == row[1]:
				numCorrect += 1
		acc = float(numCorrect / len(predictedData))
		print('Number of correctly classified instances : {0}'.format(numCorrect))
		print('Total number of instances : {0}'.format(len(predictedData)))
		print('Accuracy : {0}'.format(acc))
	else:
		totalError = 0
		mae = 0		
		for row in predictedData:
			print('Predicted value : {0:.6f}\tActual value : {1:.6f}'.format(row[0], row[1]))
			totalError += math.fabs(row[0]-row[1])
		mae = float(totalError / len(predictedData))
		print('Mean absolute error : {0}'.format(mae))
		print('Total number of instances : {0}'.format(len(predictedData)))
		


		
if __name__ == '__main__':
	main()
