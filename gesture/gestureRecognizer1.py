import stats
import math
import dtw
import distances

def test():
	dFunc = distances.euclideanDistance
	#lx = [[math.sin(x/10.0)] for x in range(10)]
	#ly = [[math.sin(x/10.0 + 0.5)] for x in range(10)]
	#print lx, '\n'
	#print ly, '\n'
	
	lx = [[x] for x in [0, 0, 0, 1, 2, 3, 3, 3, 2]]
	ly = [[x] for x in [1, 2, 3, 3, 3, 2]]
	
	#print dFunc(lx[-1], ly[6])
	
	#lx = [[x] for x in [1,1,2,3,2,0]]
	#ly = [[y] for y in [0,1,1,2,3,2,1]]
	
	#print distances.euclideanDistance([1.0], [5.0])
	
	#dist = dtw.dtwBasic(lx, ly, distances.euclideanDistance)
	dist = dtw.dtwAcceptPortionOfInputs(lx, ly, dFunc)
	print dist
	
if __name__ == "__main__":
	test()