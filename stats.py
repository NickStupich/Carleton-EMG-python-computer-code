import math

def covariance(lx, ly):
	ux = mean(lx)
	uy = mean(ly)
	
	result = sum([(x - ux) * (y - uy) for x, y in zip(lx, ly)]) / (len(lx)-1)
	return result
	
def variance(l):
	u = mean(l)
	return sum([(i-u)**2.0 for i in l]) / (len(l)-1)

def pearson(lx, ly):
	vx = variance(lx)
	vy = variance(ly)
	if vx == 0.0 or vy == 0.0:
		print 'Pearson(): variance is 0, returning 0 as pearson score'
		return 0	#doesn't really make sense
		
	return covariance(lx, ly) / math.sqrt(vx * vy)
	
def mean(l):
	return sum(l) / float(len(l))
	
def lineOfBestFit(lx, ly):
	lx2 = [float(x) * x for x in lx]
	lxy = [float(x) * y for x, y in zip(lx, ly)]
	
	n = float(len(lx))
	sx2 = sum(lx2)
	sxy = sum(lxy)
	sx = sum([float(x) for x in lx])
	sy = sum([float(y) for y in ly])
	
	denom = n * sx2 - sx * sx
	
	yint = (sy * sx2 - sx * sxy) / denom
	slope = float(n * sxy - sx * sy) / denom
	
	return (slope, yint)
	
	
if __name__ == "__main__":
	l1 = [0, 1, 2]
	l2 = [2, 4, 9]
	
	print 'variance: %s' % variance(l2)
	print 'covariance: %s ' % covariance(l1, l2)
	print 'pearson: %s' % pearson(l1, l2)
	print 'slope, yint: %s, %s' % lineOfBestFit(l1, l2)
	
	l1 = [1, 2, 3]
	l2 = [3, 2, 1]
	
	print 'covariance: %s' % covariance(l1, l2)
	print 'pearson: %s ' % pearson(l1, l2)