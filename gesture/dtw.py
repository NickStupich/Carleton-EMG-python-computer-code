import distances

INFINITY = float('inf')

def printCostMatrix(costs):
	print '\n'.join('\t'.join(str(round(x, 3)) for x in row) for row in costs)

def dtwBasic(lx, ly, distanceFunc):
	lenX = len(lx)
	lenY = len(ly)
	
	results = [[None for y in range(lenY)] for x in range(lenX)]
	
	for x in range(lenX):
		results[x][0] = INFINITY
	for y in range(lenY):
		results[0][y] = INFINITY
		
	results[0][0] = 0
	
	for x in range(1, lenX):
		for y in range(1, lenY):
			results[x][y] = distanceFunc(lx[x], ly[y])  + min(	results[x-1][y],
																results[x][y-1],
																results[x-1][y-1])
	
	#printCostMatrix(results)
	#print ' '
	return results[-1][-1]
		
"""
HOW THIS MONSTROSITY (OF AWESOMENESS) WORKS:
1 - understand regular dtw:
	stretch a set of discrete points in time(in this case), such that they fit best together
2 - one signal(or both) may have extra data on either end that isn't relevant to the gesture that is meant to be identified
	- so allow the algorithm to creep into the beginning of either sample, at a cost proportional to the square of the percent of the way it creeps in
	- the algorithm can also creep into the end of either sample, at the same cost
	- the algorithm picks the cost of the best path through, starting from anywhere and ending anywhere (anywhere in both samples being compared), and returns this cost
"""

#we can't just let the algorithm ignore stuff without a penalty, so create a function to 
#assign values to the outer row/column of the matrix instead of using infinity
#this way the algorithm should carry along that spot for a bit before it has to jump into the real thing
IGNORING_PENALTY_FUNC = lambda r: r * r * 2.0

def dtwAcceptPortionOfInputs(lx, ly, distanceFunc = distances.euclideanDistance, ignorePenalty = 1):
	#print 'dtw list 1: ' + str(lx)
	#print 'dtw list 2: ' + str(ly)
	lenX = len(lx)
	lenY = len(ly)
	
	costs = [[distanceFunc(lx[x], ly[y]) for y in range(lenY)] for x in range(lenX)]
	
	for x in range(lenX):
		costs[x][0] += IGNORING_PENALTY_FUNC(float(x) / lenX) * ignorePenalty
		costs[x][-1] += IGNORING_PENALTY_FUNC((lenX - float(x)-1) / lenX) * ignorePenalty
	for y in range(lenY):
		costs[0][y] += IGNORING_PENALTY_FUNC(float(y) / lenY) * ignorePenalty
		costs[-1][y] += IGNORING_PENALTY_FUNC((lenY - float(y)-1) / lenY) * ignorePenalty
		
	#initializing with costs means that the top\left row\column work out
	results = [[costs[x][y] for y in range(lenY)] for x in range(lenX)]
	
	for x in range(1, lenX):
		for y in range(1, lenY):
			results[x][y] = costs[x][y] + min(	results[x-1][y],
												results[x][y-1],
												results[x-1][y-1])
	
	if 0:
		printCostMatrix(costs)
		print ' '
		printCostMatrix(results)
		print ' '
	
	#with the costs added to the exit row and column, we can exit by the least costly path
	result = min(results[-1] + [r[-1] for r in results])
	return result
	#return results[-1][-1]
	
def dtwSlopeConstraint(lx, ly, distanceFunc = distances.euclideanDistance, constraint = 2):
	lenX = len(lx)
	lenY = len(ly)
	
	results = [[INFINITY for y in range(lenY)] for x in range(lenX)]
	
	for x in range(lenX):
		results[x][0] = INFINITY
	for y in range(lenY):
		results[0][y] = INFINITY
		
	results[0][0] = 0
	
	for x in range(1, lenX):
		for y in range(max(1, x-constraint), min(lenY, x+constraint)):
			results[x][y] = distanceFunc(lx[x], ly[y])  + min(	results[x-1][y],
																results[x][y-1],
																results[x-1][y-1])
	
	#printCostMatrix(results)
	#print ' '
	return results[-1][-1]