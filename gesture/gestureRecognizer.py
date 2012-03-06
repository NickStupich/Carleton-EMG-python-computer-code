import distances
import knn
import dtw
import functools
import helpers

NORMALIZE = False
SUM_ONLY = True

def normalizeData(data):
	if NORMALIZE:
		return helpers.normalizeData(data)
	else:
		return data

#extracts information about the likelyhood that a single gesture has been performed
class GestureRecognizer():
	def __init__(self, trainingData, baseDtwFunc = dtw.dtwAcceptPortionOfInputs, distanceFunc = distances.euclideanDistance):
		#need to normalize data...
		if NORMALIZE:
			trainingData = [(normalizeData(input), output) for input, output in trainingData]
		
		self.data = trainingData
		dtwFunction = functools.partial(baseDtwFunc, distanceFunc = distanceFunc)
		
		self.knnModel = knn.KNNModel(distanceFunction = dtwFunction)
		#print 'training data: ' + str(self.data[0])
		self.knnModel.train(self.data)
		
	def getOutput(self, input):
		normalized = normalizeData(input)
		#print normalized
		
		result = self.knnModel.predict(normalized)
		
		return result
