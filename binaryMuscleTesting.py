from serialCom import *
from keyListener import *
from bpnn import NN
import functools
import sys
import helpers

"""Classifiers:
all classifiers should have two functions to be used:
	getClassifyData(data):
		takes a list of data points, where the last value is the output to be predicted
		returns any kind of data structure that will be passed to the classifyFunction for that module
	classifyFunction(data, inputs, callback):
		takes a data structure containing model info, classifies inputs into a class, and calls the callback function
"""
from binary import divideByMeans
from binary import svmClassifier

channels = sum([x<<i for i, x in enumerate([1, 1, 0, 0, 0, 0])])
numChannels = helpers.getNumChannels(channels)

keyListener = KeyListener(numChannels)

trainingData = []
testingPredictions = []
module = svmClassifier

nn = None

def saveTrainingData(data, filename = 'data.txt'):
	f = open(filename, 'w')
	f.write(str(len(data[0][1])) + '\n')
	for (input, output) in data:
		#f.write('\t'.join([str(input), str(output)]) + '\n')
		
		f.write(','.join(str(x) for x in input + output) + '\n')
	f.close()

def trainCallback(data):
	global trainingData
	
	keyState = globals()['keyListener'].getOutputs()
	print data, keyState
	
	trainingData.append((data, keyState))
	
def getTrainingData():
	global channels
	
	ser = SerialCommunication(trainCallback)	
	ser.Start(channels)
	
	print 'Hit enter to finish the training period'
	s = raw_input()
	ser.Stop()
	time.sleep(1)	#just to make sure we don't have some concurrency problem
	
	data = globals()['trainingData']
	print 'number of training instances: %s' % len(data)
	return data
	
def getModelFromData(data):
	return module.getClassifyData(data)
	
def postClassifyCallback(state):
	sys.stdout.write('\b' * 10 * len(state) + '\t'.join([str(s) for s in state]))
	
def trainAndPredict():
	trainingData = getTrainingData()
	
	saveTrainingData(trainingData, 'data.txt')
	trainingData = helpers.removeTransitionDataPoints(trainingData)
	
	#train the classifier, and get the data it needs to classify future data
	model = module.getClassifyData(trainingData)
	
	#get a partial function of the classifying function, with the data already included
	classifier = functools.partial(module.classifyFunction, model,callback = postClassifyCallback)
	
	#restart the serial communication to get current muscle data
	ser = SerialCommunication(classifier)
	ser.Start(channels)
	
	print 'Hit enter to stop testing'
	s = raw_input()
	ser.Stop()
	
def main():
	trainAndPredict()
	
if __name__ == "__main__":
	main()