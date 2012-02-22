
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
	