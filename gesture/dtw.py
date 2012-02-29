
INFINITY = float('inf')

def printCostMatrix(costs):
	print '\n'.join('\t'.join(str(x)[:4] for x in row) for row in costs)

def dtwBasic(lx, ly, distanceFunc):
	lenX = len(lx)
	lenY = len(ly)
	
	costs = [[None for y in range(lenY)] for x in range(lenX)]
	
	for x in range(lenX):
		costs[x][0] = INFINITY
	for y in range(lenY):
		costs[0][y] = INFINITY
		
	costs[0][0] = distanceFunc(lx[0], ly[0])
	
	for x in range(1, lenX):
		for y in range(1, lenY):
			cost = distanceFunc(lx[x], ly[y])
			costs[x][y] = cost
	
	results = [[None for y in range(lenY)] for x in range(lenX)]
	
	for x in range(1, lenX):
		for y in range(1, lenY):
			results[x][y] = costs[x][y] + min(	costs[x-1][y],
												costs[x][y-1],
												costs[x-1][y-1])
									
	printCostMatrix(costs)
	print ' '
	printCostMatrix(results)
	print ' '
	return results[-1][-1]
		
#we can't just let the algorithm ignore stuff without a penalty, so create a function to 
#assign values to the outer row/column of the matrix instead of using infinity
#this way the algorithm should carry along that spot for a bit before it has to jump into the real thing
IGNORING_PENALTY_FUNC = lambda x: x * 1.0
def dtwAcceptPortionOfInputs(lx, ly, distanceFunc):
	lenX = len(lx)
	lenY = len(ly)
	
	costs = [[None for y in range(lenY)] for x in range(lenX)]
	
	for x in range(lenX):
		costs[x][0] = IGNORING_PENALTY_FUNC(float(x) / lenX)
	for y in range(lenY):
		costs[0][y] = IGNORING_PENALTY_FUNC(float(y) / lenY)
		
	costs[0][0] = distanceFunc(lx[0], ly[0])
	
	for x in range(1, lenX):
		for y in range(1, lenY):
			cost = distanceFunc(lx[x], ly[y])
			costs[x][y] = cost
	
	results = [[None for y in range(lenY)] for x in range(lenX)]
	
	for x in range(1, lenX):
		for y in range(1, lenY):
			results[x][y] = costs[x][y] + min(	costs[x-1][y],
												costs[x][y-1],
												costs[x-1][y-1])
									
	printCostMatrix(costs)
	print ' '
	printCostMatrix(results)
	print ' '
	return results[-1][-1]