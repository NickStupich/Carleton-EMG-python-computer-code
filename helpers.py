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