# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:43:57 2016

@author: yyc
"""

import sys
import arffParser
from decisionTree import DecisionTree


USAGE = "<train-set-file> <test-set-file> m"
USAGE_HINT = "m should be an integer."

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
	trainSetFilename, testSetFilename, m = getArgs()
	trainData = arffParser.parse(trainSetFilename)
	testData = arffParser.parse(testSetFilename)

	data = trainData['data']
	attr = trainData['attributes']
	targetIndex = len(trainData['attributes']) - 1
	tree = DecisionTree(data, attr, targetIndex, m)
	
	if tree.root == None:
		return
	tree.printTree()
	print('<Predictions for the Test Set Instances>')
	predictedData = []
	for row in testData['data']:
		predictedClass = tree.classify(row, testData['attributes'])
		predictedRow = row[-1:] + [predictedClass] 
		predictedData.append(predictedRow)
	
	numCorrect = 0
	for i, row in zip(list(range(1, len(predictedData)+1)), predictedData):
		print('{0}: Actual: {1} Predicted: {2}'.format(i, row[0], row[1]))
		if row[0] == row[1]:
			numCorrect += 1	
	print('Number of correctly classified: ' + str(numCorrect),'Total number of test instances: ' + str(len(predictedData)))
	
	
		
if __name__ == '__main__':
	main()
