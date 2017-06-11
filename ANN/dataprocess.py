# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 23:09:17 2016

@author: yyc
"""

import numpy as np


"""
Transform nominal features into one-of-k encoding
Return 
	modified data set and a list indicating the index of numeric features
""" 

def encoding(item, attributes):
	data = []
	numIndexList = []
	index = 0
	for x, i in zip(item, range(len(attributes))):
		if type(x) != float: #nominal feature
			target = [0.0] * len(attributes[i][1])
			for j in range(len(target)):
				if x == attributes[i][1][j]:
					target[j] = 1.0
			for code in target:
				data.append(code)
			index += len(target)
		else : #numeric feature
			data.append(x)
			numIndexList.append(index)
			index += 1
			
	return data, numIndexList
			

"""
Standardize train dataset
"""

def standardize(data):
	np.seterr(divide='ignore', invalid='ignore')	
	np_data = np.matrix(data)
	mean_array = np_data.mean(0)
	std_array = np.std(np_data, axis=0)
	np_data = (np_data - mean_array)/std_array
	np.nan_to_num(np_data)
	
	return np_data.tolist(), mean_array, std_array


"""
Standardize test dataset
"""

def standardizeTest(data, mean_array, std_array):
	np.seterr(divide='ignore', invalid='ignore')	
	np_data = np.matrix(data)
	np_data = (np_data - mean_array)/std_array
	np.nan_to_num(np_data)
	
	return np_data.tolist()
	

"""
Preprocessing train dataset and test dataset
"""

def process(trainDataSet, testDataSet, labels):	
	trainData = trainDataSet['data']
	testData = testDataSet['data']
		
	#numeric feature -- one input unit, nominal feature -- one-of-k encoding
	editTrainData = []
	numIndexList_train = []	
	for item in trainData:
		editItem, numIndexList_train = encoding(item[0:-1], trainDataSet['attributes'][0:-1])
		editTrainData.append(editItem)
		
	# calculate standardized value in entire train dataset
	stanTrainData, mean_array, std_array = standardize(editTrainData)
	
	# change only numeric features into standardized values
	for i in range(len(numIndexList_train)):	
		for j in range(len(editTrainData)):
			if numIndexList_train[i] == j:
				for x, y in zip(editTrainData, stanTrainData):
					x[j] = y[j]
					
			 				
	# transform class into 0 or 1 and add back into data set
	fullTrain = []	
	for x , y in zip(trainData, editTrainData):
		target = 0
		if x[-1] == labels[1]:
			target = 1
		y.append(target)
		fullTrain.append(y)
		
	
	# transform test dataset
	editTestData = []
	numIndexList_test = []	
	for item in testData:
		editItem, numIndexList_test = encoding(item[0:-1], testDataSet['attributes'][0:-1])
		editTestData.append(editItem)
	
	
	stanTestData = standardizeTest(editTestData, mean_array, std_array)
	for i in range(len(numIndexList_test)):
		for j in range(len(editTestData)):
			if numIndexList_test[i] == j:
				for x, y in zip(editTestData, stanTestData):						
					x[j] = y[j]
				
	
	fullTest = []	
	for x , y in zip(testData, editTestData):
		target = 0
		if x[-1] == labels[1]:
			target = 1
		y.append(target)
		fullTest.append(y)
	
	return fullTrain, fullTest
	