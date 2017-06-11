# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 15:20:22 2016

@author: yyc
"""

import math
import random

#TODO: binary classification problems, one output with threshold 0.5 
#TODO: 0 for first class, 1 for second class
#TODO: randomize the order of the training instances before starting training
#TODO: weights and bias are initialized to random value in [-0.01, 0.01]
#TODO: stochasic gradient descent is used to minimize cross-entropy error

class NeuralNet:
	def __init__ (self, h, o, trainSet):		
		
		# number of input, hidden nodes
		self.ni = len(trainSet[0])
		self.no = o
		if h == 0:
			self.nh = h
		else: 
			self.nh = h + 1 # bias node
			
		# activation for nodes
		self.ai = [1.0] * self.ni
		self.ah = [1.0] * self.nh
		self.ao = [1.0] * self.no
		
		
		# create weights
		if self.nh == 0:
			self.wi = makeMatrix(self.ni, self.no)
			randomWeights(self.wi, self.ni, self.no)
		else:
			self.wi = makeMatrix(self.ni, self.nh)
			randomWeights(self.wi, self.ni, self.nh)
			self.wo = makeMatrix(self.nh, self.no)
			randomWeights(self.wo, self.nh, self.no)
		

	def update(self, inputs):
		if len(inputs) != self.ni - 1:
			raise ValueError('wrong number of train data')
			
		# input activation
		for i in range(self.ni - 1):
			self.ai[i] = inputs[i]
			
		if self.nh == 0:
			for k in range(self.no):
				total = 0.0
				for i in range(self.ni):
					total += self.ai[i] * self.wi[i][k]
				self.ao[k] = sigmoid(total)
				
		else:	 # hidden activation
			for j in range(self.nh - 1):
				total = 0.0
				for i in range(self.ni):
					total += self.ai[i] * self.wi[i][j]
				self.ah[j] = sigmoid(total)
				
			# output activation
			for k in range(self.no):
				total = 0.0
				for j in range(self.nh):
					total += self.ah[j] * self.wo[j][k]
				self.ao[k] = sigmoid(total)
				
		return self.ao
		
	
	def backPropagate(self, target, l):
		
		# calculate output error
		output_deltas = [0.0] * self.no
		for k in range(self.no):
			output_deltas[k] = target - self.ao[k] 
			
		# calculate hidden error
		hidden_deltas = [0.0] * self.nh
		for j in range(self.nh):
			error = 0.0
			for k in range(self.no):
				error += output_deltas[k] * self.wo[j][k]
			hidden_deltas[j] = self.ah[j] * (1 - self.ah[j]) * error
			
		# if hidden units = 0, update input-output weights
		if self.nh == 0:
			for i in range(self.ni):
				for k in range(self.no):
					change = output_deltas[k] * self.ai[i]
					self.wi[i][k] = self.wi[i][k] + l * change
		# if hidden units != 0, update output weights
		else: 
			for j in range(self.nh):
				for k in range(self.no):
					change = output_deltas[k] * self.ah[j]
					self.wo[j][k] = self.wo[j][k] + l * change
			# update input weights
			for i in range(self.ni):
				for j in range(self.nh - 1):
					change = hidden_deltas[j] * self.ai[i]
					self.wi[i][j] = self.wi[i][j] + l * change
		
		# calculate cross entropy
		entropy = 0.0
		for k in range(self.no):
			entropy += -1 * target * math.log(self.ao[k]) - (1.0 - target) * math.log(1.0 - self.ao[k])
			
		return entropy
		
					
	def train(self, trainData, e, l):
		random.shuffle(trainData)
		trainInfo = []
		for i in range(e):
			entropy = 0.0
			correct = 0
			wrong = 0
			for item in trainData:
				ao = self.update(item[0:-1])
				if ao[0] > 0.5:
					inClass = 1
				else:
					inClass = 0
					
				if inClass == item[-1]:
					correct += 1
				else:
					wrong += 1
				
				tmp = self.backPropagate(item[-1], l)
				entropy += tmp
			
			row = [i+1] + [entropy] + [correct] + [wrong]
			trainInfo.append(row)
			
		return trainInfo
			
						
			
						
	def test(self, testData, labels):
		correct = 0
		wrong = 0	
		testInfo = []
		for item in testData:
			ao = self.update(item[0:-1])
			if ao[0] > 0.5:
				inClass = 1
			else:
				inClass = 0
					
			predictedClass = labels[inClass]
			trueClass = labels[item[-1]]
			
			if inClass == item[-1]:
				correct += 1
			else:
				wrong += 1
				
			row = [ao[0]] + [predictedClass] + [trueClass]
			testInfo.append(row)
			
		return testInfo, correct, wrong
				
			
		


def makeMatrix(x, y, fill=0.0):
	m = []
	for i in range(x):
		m.append([fill]*y)
	
	return m


def randomWeights(matrix, x, y):
	for i in range(x):
		for j in range(y):
			matrix[i][j] = random.uniform(-0.01, 0.01)


def sigmoid(x):
	return 1.0/(1.0 + math.exp(-x))	
	
	