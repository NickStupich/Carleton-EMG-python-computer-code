from serialCom import *
from keyListener import *
from bpnn import NN
from analyze import *
import functools
import sys

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
	
def testCallback(data):
	global nn, testingPredictions
	output = nn.update(data)
	testingPredictions.append((data, output))
	
	print '\t'.join([str(x) for x in output]) + '\t\t' + '='*int(output[0] * 10) + '_'*int(10 - output[0] * 10)
	
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
	
def dividingLineCallback(line, data):
	pressed = sum(data) > line
	sys.stdout.write('\b' * 6 + str(pressed))
	
def RunDividingLine():
	trainingData = getTrainingData()
	
	#convert to the format required
	saveTrainingData(trainingData, 'data2.txt')
	formatted = [input + output for input, output in trainingData]
	
	line = getDividingLine(formatted)
	classifier = functools.partial(dividingLineCallback, line)
	
	ser = SerialCommunication(classifier)
	ser.Start(channels)
	print 'Hit enter to stop testing'
	s = raw_input()
	ser.Stop()

def getTrainedNetwork():
	data = getTrainingData()
	saveTrainingData(data)
	
	nn = NN(numChannels * FOURIER_BINS, numHiddenNodes, numOutputs)
	
	nn.train(data)
	
	return nn
	
def useNetworkToPredict(nn):
	ser = SerialCommunication(testCallback)
	ser.Start(channels)
	print 'Hit enter to stop testing'
	s = raw_input()
	ser.Stop()
	
def main():
	#Neural network stuff
	#global nn
	#nn = getTrainedNetwork()
	#useNetworkToPredict(nn)
	
	#simple dividing line on sum stuff
	RunDividingLine()
	
if __name__ == "__main__":
	main()