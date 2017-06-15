# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 21:34:52 2016

@author: yyc
"""

import sys
import arffParser
from decisionTree import DecisionTree
from sampling import randomSample
import matplotlib.pyplot as plt

def curveTrainSize(data, attr,targetIndex,testData):  
    print('=== PART 2 ===')
    accAve = []
    accMin = []
    accMax = [] 
    ratioSet =  [0.05, 0.1, 0.2, 0.5, 1]  
    for ratio in ratioSet:
        print('sample size ratio = {0}'.format(ratio))
        accSet = []       
        for i in range(10):
            sampleData = randomSample(data, attr, targetIndex, ratio)
            tree = DecisionTree(sampleData, attr, targetIndex, 4)
            predictedData = []
            for row in testData['data']:
                predictedClass = tree.classify(row, testData['attributes'])
                predictedRow = row[-1:] + [predictedClass]
                predictedData.append(predictedRow)
                
            numCorrect = 0
            for row in predictedData:
                if row[0] == row[1]:
                   numCorrect += 1
            accuracy = numCorrect / float(len(predictedData))           
            print('{0:.5f}'.format(accuracy))
            accSet.append(accuracy)
           
        accAve.append(sum(accSet)/float(10))
        accMin.append(min(accSet))
        accMax.append(max(accSet))
        print('accAve:', accAve)
        print('accMin:', accMin)
        print('accMax:', accMax)
#Plot graph
    plt.figure()
    plt.plot(ratioSet, accAve, label='Ave accuracy', marker='H')   
    plt.plot(ratioSet, accMin, label='Min accuracy', marker='H')
    plt.plot(ratioSet, accMax, label='Max accuracy', marker='H')
    plt.xlabel('Ratio of Training Set Size')
    plt.ylabel('Test Set Accuracy')
    plt.title('Test Accuracy vs Training Set Size')
    plt.legend(loc='lower right')
    plt.xlim(0, 1.2)
    plt.ylim(0.3, 0.9)
    plt.grid(True)


def curveTreeSize(data, attr, targetIndex, testData):    
    print('=== PART 3 ===')
    mSet = [2, 5, 10, 20] 
    accSet = []
    for m in mSet:
        print('m = {0}'.format(m))
        tree  = DecisionTree(data, attr, targetIndex, m)
        
        predictedData = []
        for row in testData['data']:
            predictedClass = tree.classify(row, testData['attributes'])
            predictedRow = row[-1:] + [predictedClass]
            predictedData.append(predictedRow)

        numCorrect = 0
        for row in predictedData:
            if row[0] == row[1]:
                numCorrect += 1
        accuracy = numCorrect / float(len(predictedData))
        print('{0:.5f}'.format(accuracy))
        accSet.append(accuracy)
    #Plot graph
    plt.figure() 
    plt.plot(mSet, accSet, marker='H')   
    
    plt.xlabel('Value of m')
    plt.ylabel('Test Set Accuracy')
    plt.title('Test Accuracy vs Value of m')
    
    plt.xlim(0, 22)
    plt.ylim(0.6, 0.8)
    plt.grid(True)


USAGE = "<train-set-file> <test-set-file>"


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
    trainFile, testFile = getArgs()    
    trainData = arffParser.parse(trainFile)
    testData = arffParser.parse(testFile)
    data = trainData['data']
    attr = trainData['attributes']
    targetIndex = len(trainData['attributes']) - 1
    
    
    curveTrainSize(data, attr, targetIndex, testData)
    curveTreeSize(data, attr, targetIndex, testData)
	
		
if __name__ == '__main__':
	main()
