from serialCom import *
from keyListener import *
from bpnn import NN
import functools
import sys

"""Classifiers:
all classifiers should have two functions to be used:
	getClassifyData(data):
		takes a list of data points, where the last value is the output to be predicted
		returns any kind of data structure that will be passed to the classifyFunction for that module
	classifyFunction(data, inputs, callback):
		takes a data structure containing model info, classifies inputs into a class, and calls the callback function
"""
import divideByMeans
import svmClassifier

channels = sum([x<<i for i, x in enumerate([1, 0, 0, 0, 0, 0])])
numChannels = getNumChannels(channels)
numOutputs = 1 	#number of keys that can be pushed

numHiddenNodes = 2	#number of hidden nodes in the neural network

keyListener = KeyListener(numOutputs)

trainingData = []
testingPredictions = []

nn = None

def saveTrainingData(data, filename = 'data.txt'):
	f = open(filename, 'w')
	for (input, output) in data:
		#f.write('\t'.join([str(input), str(output)]) + '\n')
		f.write(','.join(str(x) for x in input + output) + '\n')
	f.close()

def trainCallback(data):
	global trainingData
	
	print data
	keyState = globals()['keyListener'].getOutputs()
	trainingData.append((data, keyState))
	
def getTrainingData():
	global channels, numChannels, numOutputs, numHiddenNodes
	
	ser = SerialCommunication(trainCallback)	
	ser.Start(channels)
	
	print 'Hit enter to finish the training period'
	s = raw_input()
	ser.Stop()
	time.sleep(1)	#just to make sure we don't have some concurrency problem
	
	data = globals()['trainingData']
	print 'number of training instances: %s' % len(data)
	return data
	
def postClassifyCallback(state):
	sys.stdout.write('\b' * 6 + str(state))
	
def trainAndPredict(module):
	trainingData = getTrainingData()
	
	saveTrainingData(trainingData, 'data.txt')
	
	#train the classifier, and get the data it needs to classify future data
	model = module.getClassifyData(trainingData)
	
	#get a partial function of the classifying function, with the data already included
	classifier = functools.partial(module.classifyFunction, model, callback = postClassifyCallback)
	
	#restart the serial communication to get current muscle data
	ser = SerialCommunication(classifier)
	ser.Start(channels)
	
	print 'Hit enter to stop testing'
	s = raw_input()
	ser.Stop()
	
def main():
	#classifier = divideByMeans
	classifier = svmClassifier
	
	trainAndPredict(classifier)
	
if __name__ == "__main__":
	main()