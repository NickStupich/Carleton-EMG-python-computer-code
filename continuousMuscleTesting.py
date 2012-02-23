from serialCom import *
from keyListener import *
import sys
import helpers
import time
from continuous import covarianceLinearFit


trainingOutputs = [0.5, 1.0]	#0% is gathered once for all channels as well
trainingPeriod = 2.0			# in seconds
prepareDelay = 2

channels = sum([x<<i for i, x in enumerate([1, 0, 0, 0, 0, 0])])
numChannels = helpers.getNumChannels(channels)

keyListener = KeyListener(numChannels)

correlationCoefficients = [[None for _ in range(numChannels)] for x in range(FOURIER_BINS)]

currentAnswer = None
recordData = False

#totally potentential threading issues here...
trainingData = []
def trainCallback(data):
	if recordData:
		trainingData.append((data, currentAnswer))

#gathers training data for each channel, for each output size for <trainingPeriod> seconds
def getTrainingData():
	global currentAnswer
	global recordData
	global trainingData
	
	ser = SerialCommunication(trainCallback)	
	ser.Start(channels)
	
	#get the relaxed data
	currentAnswer = [0.0 for _ in range(numChannels)]
	print 'relax, data gathering begins in %s seconds...' % prepareDelay
	time.sleep(prepareDelay)
	sys.stdout.write('data is being gathered...')
	recordData = True
	time.sleep(trainingPeriod)
	recordData = False
	print 'Done'
	
	for channel in range(numChannels):
		print 'start training muscle %s' % channel
		
		for trainingOutput in trainingOutputs:
			currentAnswer = [trainingOutput if x == channel else 0.0 for x in range(numChannels)]
			
			print 'tense muscle %s to %s%%, data gathering begining in %s seconds...' % (channel, trainingOutput * 100, prepareDelay)
			time.sleep(prepareDelay)
			sys.stdout.write('data is being gathered...')
			recordData = True
			time.sleep(trainingPeriod)
			recordData = False
			print 'Done'
			
		
	print 'Done all training data gathering'
	ser.Stop()
	return trainingData
			
def saveTrainingData(data, filename = 'data_continuous.txt'):
	f = open(filename, 'w')
	f.write(str(numChannels) + '\n')
	print data
	f.write('\n'.join(['\t'.join([str(x) for x in input + output]) for input, output in data]))
	f.close()
	
def postClassifyCallback(output):
	sys.stdout.write('\b' * len(output) * 20 + '\t'.join(str(x) for x in output))
	
def main():
	module = covarianceLinearFit
	
	data = getTrainingData()
	saveTrainingData(data)
	model = module.getModel(data)
	
	classifier = functools.partial(module.classifyFunction, model,
	callback = postClassifyCallback)
	
	#restart the serial communication to get current muscle data
	ser = SerialCommunication(classifier)
	ser.Start(channels)
	
	print 'Hit enter to stop testing'
	s = raw_input()
	ser.Stop()
	
if __name__ == "__main__":
	main()