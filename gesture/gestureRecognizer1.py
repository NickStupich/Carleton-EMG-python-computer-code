import stats
import math
import dtw
import distances
import knn
from datetime import datetime

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
	
	

if __name__ == "__main__":
	#testDTW()
	testKnn()