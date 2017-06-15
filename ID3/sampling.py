# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:44:38 2016

@author: yyc
"""

from random import randrange

def stratifiedSample(data, attr, targetIndex, sampleSize):
	targetValues, targetCounts = _countTargetValues(data, attr, targetIndex)
	
	ratio = sampleSize / float(len(data))
	
	sampleSize0 = int(ratio * targetCounts[0])
	sampleSize1 = sampleSize - sampleSize0
	
	partitions = _splitData(data, attr, targetIndex)
	
	while len(partitions[0]) > sampleSize0:
		del partitions[0][randrange(len(partitions[0]))]

	while len(partitions[1]) > sampleSize1:
		del partitions[1][randrange(len(partitions[1]))]
	
	return partitions[0] + partitions[1]
	



def randomSample(data, attr, targetIndex, ratio):
	targetValues, targetCounts = _countTargetValues(data, attr, targetIndex)
	
	sampleSize = ratio * float(len(data))
	
	partition = []
	for row in data:
		partition.append(row)
	
	while len(partition) > sampleSize:
		del partition[randrange(len(partition))]

	
	return partition


	
'''
_countTargetValues
	Counts the number of occurrences of each target value in given set of data.
	Target values must be binary.
	Returns list of target values, list of corresponding counts
'''
def _countTargetValues(data, attr, targetIndex):
	targetName, targetValues = attr[targetIndex]
	if len(targetValues) != 2:
		raise Exception("Target value is not binary")
	
	t1 = targetValues[0]
	t2 = targetValues[1]
	countPerVal = {t1: 0, t2: 0}

	for row in data:
		countPerVal[row[targetIndex]] += 1

	return targetValues, [countPerVal[t1], countPerVal[t2]]

def _splitData(data, attr, targetIndex):
	name, values = attr[targetIndex]
		
	M = {}
	for item in values:
		M[item] = []
	
	for row in data:
		if row[targetIndex] in M:
			M[row[targetIndex]].append(row)
		else:
			raise Exception("Invalid attribute {0} (#{1}) in row {2}".format(row[targetIndex], targetIndex, row))
	
	d = []
	for item in values:
		d.append(M[item])

	return d