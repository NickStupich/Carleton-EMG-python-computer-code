import math
import stats

def euclideanDistance(lx, ly):
	return math.sqrt(sum([(x-y)*(x-y) for x, y in zip(lx, ly)]))
	
def pearsonDistance(lx, ly):	
	return stats.pearson(lx, ly)