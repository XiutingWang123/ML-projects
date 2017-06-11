# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 18:33:59 2016

@author: yyc
"""

import sys
import arffParser
import math
import numpy as np
import matplotlib.pyplot as plt
from kNeighborsClassifier import KNeighborsClassifier

USAGE = "<train-set-file> <test-set-file>"

def accCurve(trainData, testData, classification, labels):
	k_range = [1, 5, 10, 20, 30]
	acc_range = []		
	for k in k_range:
		knn = KNeighborsClassifier(trainData, testData, k, classification, labels)
		predictedData = knn.getPrediction()
		numCorrect = 0
		acc = 0
		for row in predictedData:
			if row[0] == row[1]:
				numCorrect += 1
		acc = float(numCorrect / len(predictedData))
		acc_range.append(acc)
	# plot graph
	plt.figure()
	plt.plot(k_range, acc_range, marker='H')
	plt.xlabel('Value of k')
	plt.ylabel('Test Set Accuracy')
	plt.title('Test Accuracy vs Value of k')
	plt.grid(True)
	plt.xlim(0, 32)
	plt.savefig('1.jpg', dpi=1200)
				
def confusionMatrix(trainDataSet, testData, classification, labels):
	k_range = [1, 30]
	for k in k_range:
		knn = KNeighborsClassifier(trainDataSet['data'], testData, k, classification, labels)
		predictedData = knn.getPrediction()
		labels = trainDataSet['attributes'][-1][1]
		M = {}
		results = []
		
			
		for label in labels:
			for item in labels:
				M[item] = 0
			for i in predictedData:
				if i[1] == label:
					M[i[0]] += 1
			res = []
			for item in labels:
				res.append(M[item])
			results.append(res)
		print('k = {0}'.format(k))
		#print(results)
		 
		# plot confusion matrix		
		norm_conf = []
		for i in results:
			a = 0
			tmp = []
			a = sum(i, 0)
			for j in i:
				if a == 0:
					tmp.append(0)
				else:
					tmp.append(float(j)/float(a))
			norm_conf.append(tmp)
			
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.set_aspect(1)
		color = ax.imshow(np.array(norm_conf), cmap=plt.cm.jet, interpolation='nearest')
		width, height = np.array(results).shape
		for x in range(width):
			for y in range(height):
				ax.annotate(str(results[x][y]), xy =(y, x), horizontalalignment='center', verticalalignment='center')
		
		fig.colorbar(color)
		plt.xticks(range(width), labels)
		plt.yticks(range(height), labels)
		plt.xlabel('Predicted Class')
		plt.ylabel('Actual Class')
		plt.savefig('3_%d.jpg' % k, dpi=1200)
		
		
	
	
		
def maeCurve(trainData, testData, classification, labels):
	k_range = [1, 2, 3, 5, 10]
	mae_range = []		
	for k in k_range:
		knn = KNeighborsClassifier(trainData, testData, k, classification, labels)
		predictedData = knn.getPrediction()
		totalError = 0
		mae = 0
		for row in predictedData:
			totalError += math.fabs(row[0]-row[1])
		mae = float(totalError / len(predictedData))
		mae_range.append(mae)
	# plot graph
	plt.figure()
	plt.plot(k_range, mae_range, marker='H')
	plt.xlabel('Value of k')
	plt.ylabel('Test Set Mean Absolute Error')
	plt.title('Test Mean Absolute Error vs Value of k')
	plt.grid(True)
	plt.xlim(0, 12)
	plt.savefig('2.jpg', dpi=1200)
	
	

def getArgs():
	if len(sys.argv) < 3:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)

	try:
		return sys.argv[1], sys.argv[2]
	except ValueError:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)

def main():
	trainSetFile, testSetFile = getArgs()
	trainDataSet = arffParser.parse(trainSetFile)
	testDataSet = arffParser.parse(testSetFile)
	trainData = trainDataSet['data']
	testData = testDataSet['data']
	labels = trainDataSet['attributes'][-1][1]
	
	if trainDataSet['attributes'][-1][0] == 'class': 
		classification = True
	elif trainDataSet['attributes'][-1][0] == 'response':
		classification = False
	else:
		raise Exception('Invalid label description: {0}'.format('label must be class or response'))
		
	if classification:
		accCurve(trainData, testData, classification, labels)
		confusionMatrix(trainDataSet, testData, classification, labels)
	else:
		maeCurve(trainData, testData, classification, labels)
		
	
	


		
if __name__ == '__main__':
	main()
