NUM_CHANNELS = 6
FOURIER_BINS = 8


distance = 2

def removeTransitionDataPoints(data):
	toInclude = [1] * len(data)
	for i in range(len(data)-1):
		if data[i][-1][0] != data[i+1][-1][0]:	#change in state, ignore for +- <distance> samples
			for j in range(-distance+1, distance+1):
				if j + i > 0 and j+i < len(data):
					toInclude[j+i] = 0
					
	result = []
	ignoredCount = 0
	for dat, include in zip(data, toInclude):
		if include:
			result.append(dat)
		else:
			ignoredCount +=1
			
	print 'ignored %s points at state transitions' % ignoredCount
	return result
	

"""scales inputs between 0-1 based on the largest value in the inputs"""
def scaleInputs(inputs, scalingValue = None):
	if scalingValue is None:
		largest = max(map(lambda x: max(x), inputs))
	
	scaled = []
	for input in inputs:
		scaled.append([float(x) / largest for x in input])
		
	return scaled
	
def getNumChannels(channels):
	numChannels = 0
	for i in range(NUM_CHANNELS):
		if (1<<i) & channels:
			numChannels += 1
	
	return numChannels
	
def normalizeData(data):
	#data is a list of lists of ints
	#transform to a list of lists of floats where the mean value is 1
	if NORMALIZE:
		u = stats.mean([stats.mean(d) for d in data])
		result = [[float(x) / u for x in d] for d in data]
		return result
	else:
		return data
