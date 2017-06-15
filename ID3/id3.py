# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:44:38 2016

@author: yyc
"""

import sys
import math
from decisionTreeNode import TreeNode

'''
ID3
	Creates decision tree using ID3 algorithm
	Target values must be binary
'''
def ID3 (data, attr, remainingAttr, parentTargetValue, targetIndex, m):
	targetValues, targetCounts = _countTargetValues(data, attr, targetIndex)
         
	mostCommonTargetValue = targetValues[0]
	if targetCounts[0] == targetCounts[1]:
         mostCommonTargetValue = parentTargetValue
	if targetCounts[0] < targetCounts[1]:
		mostCommonTargetValue = targetValues[1]
	
    # Check stopping criteria:
    # (i) all of the training instances reaching the node belong to the same class, 
    # (ii) there are fewer than m training instances reaching the node
    # (iv) there are no more features to split on.
	if len(data) == targetCounts[0] or len(data) == targetCounts[1] or \
	   len(data) < m or \
	   len(remainingAttr) == 0:
		return TreeNode(label = mostCommonTargetValue, numPos = targetCounts[0], numNeg = targetCounts[1])

	decisionAttr, decisionValue = _findBestSplit(data, attr, remainingAttr, targetIndex)
	
    # Check stopping criteria:
	# (iii) no feature has positive information gain
	if decisionAttr == None:
		return TreeNode(label = mostCommonTargetValue, numPos = targetCounts[0], numNeg = targetCounts[1])

	root = TreeNode(numPos = targetCounts[0], numNeg = targetCounts[1], decisionAttr = decisionAttr, decisionValue = decisionValue)

	partitions = _splitData(data, attr, decisionAttr, decisionValue)
	
	if isinstance(decisionValue, list):  # Nominal
		# Remove decisionAttr from list of remaining attributes
		remainingAttr = [a for a in remainingAttr if a[0] != decisionAttr]
		
	for D in partitions:
         if len(D) == 0:
             root.children.append(TreeNode(label = mostCommonTargetValue, numPos = 0, numNeg = 0))        
         else:
             root.children.append(ID3(D, attr, remainingAttr, mostCommonTargetValue, targetIndex, m))
	return root
	
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

'''
_getAttrIndexByName
	Searches list of attribute tuples for given attribute name and returns index.
'''	
def _getAttrIndexByName(attr, name):
	for i in range(0, len(attr)):
		if attr[i][0] == name:
			return i

'''
_findBestSplit
	Returns:
		decisionAttr - Name of best attribute to split on
		decisionValue - Value of attribute to split on
						Single value if attribute is numeric, or list if nominal
'''
def _findBestSplit(data, attr, remainingAttr, targetIndex):
	candidateSplits = []  # (attrName, value)
	for attrName, attrValue in remainingAttr:
		if isinstance(attrValue, list):  # Nominal
			candidateSplits.append((attrName, attrValue))
		else: # Numeric
			candidateSplits += _getCandidateNumericSplits(data, attr, attrName, targetIndex)

	return _ordinaryFindBestSplit(data, attr, targetIndex, candidateSplits)
	
'''
_getCandidateNumericSplits
	Returns list of possible splits
'''
# Run this subroutine for each numeric feature at each node of DT induction
def _getCandidateNumericSplits(data, attr, attrName, targetIndex):
	i = _getAttrIndexByName(attr, attrName)

	C = []
	S = {}  # Partition data into sets with same value
	for row in data:
		if row[i] not in S:
			S[row[i]] = []
		S[row[i]].append(row)
	
	sortedValues = []
	for value in S:
		sortedValues.append(value)
	sortedValues.sort()
	
	for i in range(0, len(sortedValues)-1):
		if _hasDifferentClassLabels(S, sortedValues[i], sortedValues[i+1], targetIndex, attr[targetIndex][1]):
			# Use midpoint for split
			C.append((attrName, (sortedValues[i] + sortedValues[i+1]) / 2))
	
	return C

'''
_hasDifferentClassLabels
	Returns True if rows in S[val1] and S[val2] have different class labels, False otherwise.
'''
def _hasDifferentClassLabels(S, Sval1, Sval2, targetIndex, targetValues):
	Tval1, Tval2 = targetValues
	
	# Which target values are present in each set in S
	presence1 = { Tval1: False, Tval2: False }
	presence2 = { Tval1: False, Tval2: False }
	
	# Iterate through sets and mark presence of target values
	for row in S[Sval1]:
		presence1[row[targetIndex]] = True
	for row in S[Sval2]:
		presence2[row[targetIndex]] = True
	
	if (presence1[Tval1] and presence2[Tval2]) or \
	(presence1[Tval2] and presence2[Tval1]):
		return True
	else:
		return False

def _ordinaryFindBestSplit(data, attr, targetIndex, candidateSplits):
	maxgain = 0
	
	bestSplit = (None, None)
	for split in candidateSplits:
		gain = _infoGain(data, attr, targetIndex, split)
		if gain > maxgain:
			maxgain = gain
			bestSplit = split

	return bestSplit

def _infoGain(data, attr, targetIndex, split):
	return _entropy(data, attr, targetIndex, split) - _condEntropy(data, attr, targetIndex, split)

def _entropy(data, attr, targetIndex, split):
	Tval1, Tval2 = attr[targetIndex][1]
	targetCount = { Tval1: 0, Tval2: 0 }
	
	for row in data:
		targetCount[row[targetIndex]] += 1
	
	total = float(len(data))
	sum = 0
	for val in targetCount:
		if targetCount[val] > 0:
			P = targetCount[val] / total
			if P - 0.0 > 1e-6 or 1.0 - P > 1e-6:
				sum -= P * math.log(P, 2)
	return sum
	
def _condEntropy(data, attr, targetIndex, split):
	partitions = _splitData(data, attr, split[0], split[1])
	
	total = float(len(data))
	sum = 0
	for D in partitions:
		if len(D) > 0:
			P = len(D) / total
			if P - 0.0 > 1e-6:
				sum += P * _entropy(D, attr, targetIndex, split)
	return sum

'''
_splitData
	Splits data on decisionAttr and based on decisionValue.
	Returns list of splits, with each split being a list of data items.
'''
def _splitData(data, attr, decisionAttr, decisionValue):
	if isinstance(decisionValue, list):  # Nominal
		return _splitDataNominal(data, attr, decisionAttr, decisionValue)
	else:  # Numeric
		return _splitDataNumeric(data, attr, decisionAttr, decisionValue)

'''
_splitDataNominal
	Split data into nominal categories of decisionAttr.
	Returns list of splits, with each split being a list of data items.
'''
def _splitDataNominal(data, attr, decisionAttr, decisionValue):
	i = _getAttrIndexByName(attr, decisionAttr)
	if attr[i][1] != decisionValue:
		raise Exception("_splitDataNominal: Inconsistent attribute datatypes")
	
	M = {}
	for item in decisionValue:
		M[item] = []
	
	for row in data:
		if row[i] in M:
			M[row[i]].append(row)
		else:
			raise Exception("Invalid attribute {0} (#{1}) in row {2}".format(row[i], i, row))
	
	d = []
	for item in decisionValue:
		d.append(M[item])

	return d
	
'''
_splitDataNumeric
	Split data into <= decisionValue and > decisionValue.
	Returns list of splits, with each split being a list of data items.
'''
def _splitDataNumeric(data, attr, decisionAttr, decisionValue):
	i = _getAttrIndexByName(attr, decisionAttr)
	if attr[i][1] != float:
		raise Exception("_splitDataNumeric: Inconsistent attribute datatypes")

	d = [[], []]
	for row in data:
		if row[i] <= decisionValue:
			d[0].append(row)
		else:
			d[1].append(row)

	return d
