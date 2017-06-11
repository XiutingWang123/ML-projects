# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 22:58:03 2016

@author: yyc
"""

import csv
import math
from operator import itemgetter

class KNeighborsClassifier:
	def __init__(self, trainData, testData, k, classification, labels):
		self.predictedData = []
		if classification:
			for testInstance in testData:
				self.neighbors = getNeighbors(trainData, testInstance, k)
				predictedClass = getClass(self.neighbors, labels)
				predictedRow = [predictedClass] + testInstance[-1:] 
				self.predictedData.append(predictedRow)
		else:
			for testInstance in testData:
				self.neighbors = getNeighbors(trainData, testInstance, k)
				predictedClass = getResponse(self.neighbors)
				predictedRow = [predictedClass] + testInstance[-1:] 
				self.predictedData.append(predictedRow)

	
	def getPrediction(self):
		return self.predictedData



	
  

def euclideanDistance(instance1, instance2):  
	distance = 0
	for i in range(len(instance1)):
	        distance += pow((instance1[i] - instance2[i]), 2)    
	return math.sqrt(distance)

"""
getNeighbors
        compute the eulidean distance between test instance and each train instance
        return the best k neighnors
"""

def getNeighbors (trainData, testInstance, k):
    distances = []
    for trainInstance in trainData:
        dist = euclideanDistance(testInstance[0:-1], trainInstance[0:-1])
        distances.append((trainInstance[-1], dist))
        
								
    distances.sort(key=itemgetter(1))
    neighbors = []
    
    for i in range(k):
        neighbors.append(distances[i][0])
    
    return neighbors

    
"""
getClass
        return the majority vote of class label in neighbors
"""

def getClass(neighbors, labels):
	classVotes = {}
	for label in neighbors:
		if label not in classVotes:
			classVotes[label] = 1
		else:
			classVotes[label] += 1
	
	rank = []
	for label in labels:
		if label not in neighbors:
			rank.append((label, 0))
		else:
			rank.append((label, classVotes[label]))
	
	majorityClass = rank[0][0]
	vote = rank[0][1]	
	for item in rank:
		if item[1] > vote:
			vote = item[1]
			majorityClass = item[0]
		
	#sortedVotes = sorted(classVotes.items(), key=itemgetter(1), reverse=True)
	return majorityClass

    
"""
getResponse
        return the mean value of neighbors
"""
def getResponse(neighbors):
    return float(sum(neighbors) / len(neighbors))
    
    

    