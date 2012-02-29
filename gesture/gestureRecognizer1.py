import stats
import math
import dtw
import distances
from datetime import datetime

def speedTest():
	dFunc = distances.euclideanDistance
	lx = [[math.sin(x/10.0)] for x in range(10)]
	ly = [[math.sin(x/10.0 + 0.5)] for x in range(10)]
	start = datetime.now()
	for _ in range(1000):
		dist = dtw.dtwAcceptPortionOfInputs(lx, ly, dFunc)
	end = datetime.now()
	print (end - start)

def test():
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
	
	dist = dtw.dtwBasic(lx, ly, distances.euclideanDistance)
	print dist
	#speedTest()
	dist = dtw.dtwAcceptPortionOfInputs(lx, ly, dFunc)
	print dist
	
#def train():
	
	
if __name__ == "__main__":
	test()