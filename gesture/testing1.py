import stats
import math
import dtw
import distances
import knn
from datetime import datetime
import functools
import time
import gestureRecognizer
import realtimeGR1
import gestureDistanceCalculator

DISTANCE_TO_PRINT = 2000

l1 = 4
l2 = 2

		
def loadData(filename = '../data2_ringFinger2.txt'):
	f = open(filename)
	numOutputs = int(f.readline())
	result = []
	for line in f:
		parts = [int(x) for x in line.split(',')]
		input = parts[:-numOutputs]
		output = parts[-numOutputs:]
		if 0:
			result.append(([sum(input)], output))
		else:
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
	
	lx = [[float(x)] for x in [0, 0, 0, 1, 2, 3, 3, 2]]
	ly = [[float(x)] for x in [1, 2, 3, 3, 3, 2, 0, 1]]
	
	#print dFunc(lx[-1], ly[6])
	
	#lx = [[x] for x in [1,1,2,3,2,0]]
	#ly = [[y] for y in [0,1,1,2,3,2,1]]
	
	#print distances.euclideanDistance([1.0], [5.0])
	
	d1 = dtw.dtwBasic(lx, ly, dFunc)
	#print dist
	d2 = dtw.dtwAcceptPortionOfInputs(lx, ly, dFunc)
	d3 = dtw.dtwSlopeConstraint(lx, ly, dFunc)
	print d1, d2, d3
	#speedTest()
	
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
	gestureLength = l1	#5 samples / 20Hz = 0.25 seconds
	postGestureLength = l2	#time allowed after the gesture was caught in output
	for i in range(len(data) - gestureLength - postGestureLength):
		#print data[i+gestureLength-1][1][0], data[i + gestureLength][1][0]
		if data[i+gestureLength-2][1][0] == 0 and data[i + gestureLength-1][1][0] == 1:
			gestureData = [d[0] for d in data[i:i+gestureLength + postGestureLength]]	#remove the outputs since we've already associated it with a gesture
			normalized = gestureDistanceCalculator.normalizeData(gestureData)
			gestures[0].append(normalized)
			
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
	gestures = realtimeGR1.extractGestures1(data)
	
	g2 = [(g, 1.0) for g in gestures[0][1:]]#reformat and remove the first one
	
	gr = gestureDistanceCalculator.GestureDistanceCalculator(g2)
	
	for i in range(2, 8):
		input = [d[0] for d in data[i:i+l1+l2]]
		#print input
		#print '\n\n\n' + str(input)
		distance, input, ouput = gr.getOutput(input)
		print i, distance
		#print output
	
def testSystem3():
	data = loadData()
	
	gestures, maybeGestures = realtimeGR1.extractGesturesAndMaybe1(data)
	
	examples = gestures[0][1:]
	maybeExamples = maybeGestures[0]
	#examples = [(g, 1.0) for g in gestures[0][1:]]#reformat and remove the first one
	for ex in examples:	print [round(e[0], 2) for e in ex]
	
	training = [(g, 1.0) for g in examples]
	gr = gestureDistanceCalculator.GestureDistanceCalculator(training)
	
	print '\n\n'
	
	fout = open('grOutput.txt', 'w')
	
	allDistances = []
	
	start = time.time()
	
	for i in range(l1 + l2, 30000):
		if i >= len(data): break
		
		input = [d[0] for d in data[i-l1-l2:i]]
		distance, closest, systemOutput = gr.getOutput(input)
		s = '\t'.join([str(i), str([round(i[0], 2) for i in gestureDistanceCalculator.normalizeData(input)]), str(round(distance, 2))])
		
		if distance < DISTANCE_TO_PRINT:
			print s
		
		fout.write(s + '\n')
		
		allDistances.append(distance)
		
	#elapsed = time.time() - start
	#numPoints = len(data) - l1 - l2
	#print 'took %s for %s points' % (elapsed, numPoints)
		
	avDistance = stats.mean(allDistances)
	stdDevDistance = stats.stdDev(allDistances)
	
	print 'average distance: %s with stdDev %s' % (avDistance, stdDevDistance)
	
	fout.close()

def testGestureRecognizer():
	data = loadData()
	gesturesDict, maybeGesturesDict = realtimeGR1.extractGesturesAndMaybe1(data)
	gestures = gesturesDict[0]
	maybeGestures = maybeGesturesDict[0]
	#print maybeGestures
	nonGestures = realtimeGR1.extractNonGestures(data)
	
	
	
	print 'lengths:', len(gestures), len(maybeGestures), len(nonGestures)
	
	gr = gestureRecognizer.GestureRecognizer(gestures, maybeGestures, nonGestures)
	
def testNonGestureExtraction():
	data = loadData()
	gestures = realtimeGR1.extractGestures1(data)[0]
	
	
if __name__ == "__main__":
	#testDTW()
	#testKnn()
	#testSystem2()
	#testSystem3()
	#testGestureExtraction()
	#testNonGestureExtraction()
	testGestureRecognizer()