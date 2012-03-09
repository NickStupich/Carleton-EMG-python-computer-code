import stats
import distances

def weightingOneOverD(d):
	return 1.0 / d
	
class KNNModel():
	def __init__(self, n = 1, weightingFunction = weightingOneOverD, distanceFunction = distances.euclideanDistance):
		self.weightingFunction = weightingFunction
		self.n = n
		self.distanceFunction = distanceFunction
		
	def train(self, data):
		self.data = data
		
	def predict(self, test):
		if self.n == 1:
			best = (float('inf'), None, None)
			for sampleMaybeTuple in self.data:
				#print 'knn: distance between : ', test, sample
				#print sample
				if type(sampleMaybeTuple) == type(()):
					sample = sampleMaybeTuple[0]
				else:
					sample = sampleMaybeTuple
				
				d = self.distanceFunction(test, sample)

				#print test, sample, d
				if d < best[0]:
					best = (d, sample[0], sample[1])
			
			#print best
			return best
		else:	
			raise Exception("n>1 not yet implemented")
				
		
		