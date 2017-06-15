# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:46:52 2016

@author: yyc
"""

import sys
import id3
from decisionTreeNode import TreeNode
			
class DecisionTree:
	def __init__(self, data, attr, targetIndex, m):
		if targetIndex < 0:
			self.root = None
		else:
			self.root = id3.ID3(data, attr, attr[:targetIndex] + attr[targetIndex+1:], None, targetIndex, m)
	
	def printTree(self):
		if self.root.label != None:
			print(self.root.label)
		else:
			print(_printTreeHelper(self.root, 0).split('\n',1)[1])
	
	def classify(self, item, attr):
		return _classifyHelper(self.root, item, attr)

def _classifyHelper(root, item, attr):
	if root.label != None:
		return root.label
	else:
		i = _getAttrIndexByName(attr, root.decisionAttr)
		if isinstance(root.decisionValue, list):  # Nominal
			for j in range(0, len(root.decisionValue)):
				if item[i] == root.decisionValue[j]:
					return _classifyHelper(root.children[j], item, attr)
		else:  # Numeric
			if item[i] <= root.decisionValue:
				return _classifyHelper(root.children[0], item, attr)
			else:
				return _classifyHelper(root.children[1], item, attr)
	
def _printTreeHelper(root, level):
	string = ''
	if level > 0:
		string += ' [{0} {1}]'.format(root.numPos, root.numNeg)

	if root.label != None:
		return string + ': {0}'.format(root.label)
	else:
		if isinstance(root.decisionValue, list):  # Nominal
			for i in range(0, len(root.decisionValue)):
				string += '\n'  # Begin new line				
				for j in range(0,level):
					string += '|\t'
				string += '{0} = {1}'.format(root.decisionAttr, root.decisionValue[i])
				string += _printTreeHelper(root.children[i], level + 1)
		else:  # Numeric
			for i, sign in [(0, '<='), (1, '>')]:
				string += '\n'  # Begin new line	
				for j in range(0,level):
					string += '|\t'
				string += '{0} {1} {2:.6f}'.format(
					root.decisionAttr, sign, root.decisionValue)
				string += _printTreeHelper(root.children[i], level + 1)

		return string

'''
_getAttrIndexByName
	Searches list of attribute tuples for given attribute name and returns index.
'''	
def _getAttrIndexByName(attr, name):
	for i in range(0, len(attr)):
		if attr[i][0] == name:
			return i

USAGE = "<arff-file> <m>"
USAGE_HINT = "m should be an integer."

def _getArgs():
	if len(sys.argv) < 3:
		print("Usage: {0} {1}".format(sys.argv[0], USAGE), file=sys.stderr)
		sys.exit(-1)
	
	try:
		return sys.argv[1], int(sys.argv[2])
	except ValueError:
		print("Usage: {0} {1} ({2})".format(sys.argv[0], USAGE, USAGE_HINT), file=sys.stderr)
		sys.exit(-1)		

def _main():	
	filename, m = _getArgs()
	import arffParser
	arff = arffParser.parse(filename)

	tree = DecisionTree(arff['data'], arff['attributes'], len(arff['attributes']) - 1, m)
	if tree.root == None:
		return
	
	tree.printTree()
		
if __name__ == '__main__':
	_main()
