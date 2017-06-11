# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 23:50:23 2016

@author: yyc
"""

import sys
import arff
import dataprocess
from NN import NeuralNet



USAGE = "l h e <train-set-file> <test-set-file>"
USAGE_HINT = "h, k should be integers."

def getArgs():
	if len(sys.argv) < 6:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)

	try:
		return float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]
	except ValueError:
		print("Usage: {0} {1} ({2})".format(sys.argv[0], USAGE, USAGE_HINT), file=sys.stderr)
		sys.exit(-1)
		

					

def main():
	l, h, e, trainSetFile, testSetFile = getArgs()
	trainDataSet = arff.load(open(trainSetFile, 'r'))
	testDataSet = arff.load(open(testSetFile, 'r'))
	labels = trainDataSet['attributes'][-1][1]
	
	fullTrain, fullTest = dataprocess.process(trainDataSet, testDataSet, labels)
		
	
	ann = NeuralNet(h, 1, fullTrain)
	trainInfo = ann.train(fullTrain, e, l)
	for item in trainInfo:
		print('Epoch: {0}\tCross-entropy error: {1}\tCorrectly classified instances: {2}\tMisclassified instances: {3}'.format\
		(item[0], item[1], item[2], item[3]))
	
	testInfo, correct, wrong = ann.test(fullTest, labels)
	for item in testInfo:
		print('Activation of output unit: {0}\tPredicted class: {1}\tCorrect class: {2}'.format\
		(item[0], item[1], item[2]))
	print('Correctly classified instances: {0}\tMisclassified instances: {1}'.format(correct, wrong))
	

	
		
		

		
if __name__ == '__main__':
	main()
