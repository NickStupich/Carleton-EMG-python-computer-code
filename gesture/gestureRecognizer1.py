import stats
import math
import dtw
import distances
import knn
from datetime import datetime
import functools

def normalizeData(data):
	#data is a list of lists of ints
	#transform to a list of lists of floats where the mean value is 1
	u = stats.mean([stats.mean(d) for d in data])
	result = [[float(x) / u for x in d] for d in data]
	return result

#extracts information about the likelyhood that a single gesture has been performed
class GestureRecognizer():
	def __init__(self, trainingData):
		#need to normalize data...
		normalized = [(normalizeData(input), output) for input, output in trainingData]
		self.data = normalized
		dtwFunction = functools.partial(dtw.dtwAcceptPortionOfInputs, distanceFunc = distances.euclideanDistance)
		self.knnModel = knn.KNNModel(distanceFunction = dtwFunction)
		#print 'training data: ' + str(self.data[0])
		self.knnModel.train(self.data)
		
	def getOutput(self, input):
		normalized = normalizeData(input)
		#print normalized
		
		result = self.knnModel.predict(normalized)
		
		return result
		

def loadData(filename = '../data2_ringFinger2.txt'):
	f = open(filename)
	numOutputs = int(f.readline())
	result = []
	for line in f:
		parts = [int(x) for x in line.split(',')]
		input = parts[:-numOutputs]
		output = parts[-numOutputs:]
		result.append((input, output))
	
	f.close()
	return result

def speedTest():
	loops = 1000
	dFunc = distances.euclideanDistance
	lx = [[math.sin(x/10.0)]*16 for x in range(10)]
	ly = [[math.sin(x/10.0 + 0.5)]*16 for x in range(10)]
	
	start = datetime.now()
	for _ in xrange(loops):
		dist = dtw.dtwAcceptPortionOfInputs(lx, ly, dFunc)
	end = datetime.now()
	
	elapsed = (end - start)
	print 'total : %s ' % elapsed
	micros = (elapsed).seconds * 1000000 + (elapsed).microseconds
	microsPerLoop = micros / loops
	print 'microseconds per dtw(): %s' % microsPerLoop

def testDTW():
	dFunc = distances.euclideanDistance
	#lx = [[math.sin(x/10.0)] for x in range(10)]
	#ly = [[math.sin(x/10.0 + 0.5)] for x in range(10)]
	#print lx, '\n'
	#print ly, '\n'
	
	lx = [[float(x)] for x in [0, 0, 0, 1, 2, 2, 3, 3, 3, 2]]
	ly = [[float(x)] for x in [1, 2, 3, 3, 3, 2, 0, 1]]
	
	#print dFunc(lx[-1], ly[6])
	
	#lx = [[x] for x in [1,1,2,3,2,0]]
	#ly = [[y] for y in [0,1,1,2,3,2,1]]
	
	#print distances.euclideanDistance([1.0], [5.0])
	
	#dist = dtw.dtwBasic(lx, ly, distances.euclideanDistance)
	#print dist
	#dist = dtw.dtwAcceptPortionOfInputs(lx, ly, dFunc)
	#print dist
	speedTest()
	
def testKnn():	
	training = [[[1, 2, 3], [1]],
				[[1, 2, 2], [1]],
				[[4, 3, 2], [0]],
				[[4, 5, 4], [0]]
				]
				
	model = knn.KNNModel()
	model.train(training)
	
"""a gesture is defined (for now) as the transition between 0 and 1 on a single output"""
def extract0to1Gestures(data):
	gestures = {0: []} #only create gesture 0
	gestureLength = 5	#5 samples / 20Hz = 0.25 seconds
	postGestureLength = 3	#time allowed after the gesture was caught in output
	for i in range(len(data) - gestureLength - postGestureLength):
		#print data[i+gestureLength-1][1][0], data[i + gestureLength][1][0]
		if data[i+gestureLength-2][1][0] == 0 and data[i + gestureLength-1][1][0] == 1:
			gestureData = [d[0] for d in data[i:i+gestureLength + postGestureLength]]	#remove the outputs since we've already associated it with a gesture
			gestures[0].append(gestureData)
			
	return gestures
	
def testGestureExtraction():
	data = loadData()
	print data[0]
	print 'data length: ' + str(len(data))
	gestures = extract0to1Gestures(data)
	print gestures[0][0]

def testSystem1():
	data = loadData()
	gestures = extract0to1Gestures(data)
	
	g2 = [(g, 1.0) for g in gestures[0][1:]]
	print g2[0][0]
	print normalizeData(g2[0][0])
	exit()
	#print g2[1]
	
	dtwFunction = functools.partial(dtw.dtwAcceptPortionOfInputs, distanceFunc = distances.pearsonDistance)
	knnModel = knn.KNNModel(distanceFunction = dtwFunction)
	knnModel.train(g2)
	
	for i in range(20):
		testData = [d[0] for d in data[i:i+5]]
		fit = knnModel.predict(testData)
		distance, input, ouput = fit
		print i, distance
	
def testSystem2():
	data = loadData()
	gestures = extract0to1Gestures(data)
	
	g2 = [(g, 1.0) for g in gestures[0][1:]]#reformat and remove the first one
	
	gr = GestureRecognizer(g2)
	
	for i in range(15):
		input = [d[0] for d in data[i:i+5]]
		#print '\n\n\n' + str(input)
		distance, input, ouput = gr.getOutput(input)
		print i, distance
		#print output
	

if __name__ == "__main__":
	#testDTW()
	#testKnn()
	testSystem2()
	#testGestureExtraction()