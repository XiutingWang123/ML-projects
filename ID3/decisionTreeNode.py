# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 19:45:52 2016

@author: yyc
"""

class TreeNode:
	def __init__(self, label = None, numPos = None, numNeg = None, \
				 decisionAttr = None, decisionValue = None):
		self.label = label
		self.numPos = numPos
		self.numNeg = numNeg
		self.decisionAttr = decisionAttr
		self.decisionValue = decisionValue
		self.children = []
