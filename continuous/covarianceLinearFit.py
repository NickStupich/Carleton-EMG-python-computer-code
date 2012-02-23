import helpers
import stats

class Model():
	def __init__(self, numInputs, numOutputs):
		self.__numInputs = numInputs
		self.__numOutputs = numOuputs
		
		self.pearsons = [[None for x in range(numInputs)] for y in range(numOutputs)]
		
		self.yInts = [[None for x in range(numInputs)] for y in range(numOutputs)]
		
		self.slopes = [[None for x in range(numInputs)] for y in range(numOutputs)]
		
	def getOutput(self, input):
		result = []
		for i in range(self.numOutputs):
			num = 0
			denom = 0
			for j in range(self.numInputs):
				pred = self.yInts[j][i] + self.slopes[j][i] * input[j][i]
				num += pred * self.pearsons[j][i]
				denom += abs(self.pearsons[j][i])
				
			result.append(num / denom)
			
		return result
				
def getModel(data):
	numInputs = len(data[0][0])
	numOutputs = len(data[0][1])
	
	model = Model(numInputs, numOutputs)
	
	for input in range(numInputs):
	
		#extract fourier bin from training data
		x = map(lambda x: x[0][input], data)
		
		for output in range(numOutputs):
			#extract outputs to train against
			y = map(lambda x: x[1][output], data)
			
			#calculate pearson score between input and output
			p = stats.pearson(x, y)
			
			model.pearsons[input][output] = p
			
			#get the slope and y-int of the line of best fit between in put and output
			
			(slope, yInt) = stats.lineOfBestFit(x, y)
			model.slopes[input][output] = slope
			model.yInts[input][output] = yInt
			
			
def classifyFunction(model, input, callback = None):
	result = model.getOutput(input)
	if callback:
		callback(result)
		
	return result
			
			