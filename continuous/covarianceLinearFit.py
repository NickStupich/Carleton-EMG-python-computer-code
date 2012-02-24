import helpers
import stats

class Model():
	def __init__(self, numInputs, numOutputs):
		self.__numInputs = numInputs
		self.__numOutputs = numOutputs
		
		self.pearsons = [[None for x in range(numOutputs)] for y in range(numInputs)]
		
		self.yInts = [[None for x in range(numOutputs)] for y in range(numInputs)]
		
		self.slopes = [[None for x in range(numOutputs)] for y in range(numInputs)]
		
	def getOutput(self, input):
		result = []
		for i in range(self.__numOutputs):
			num = 0
			denom = 0
			for j in range(self.__numInputs):
				predicted = self.yInts[j][i] + self.slopes[j][i] * input[j]
				num += predicted * self.pearsons[j][i]
				denom += abs(self.pearsons[j][i])
				
			result.append(num / denom)
			
		return result
		
	def save(self, filename = "covLinModel.txt"):
		f = open(filename, 'w')
		f.write(','.join(str(x) for x in [self.__numInputs, self.__numOutputs]) + '\n')
		f.write(','.join(str(x) for x in self.pearsons) + '\n')
		f.write(','.join(str(x) for x in self.yInts) + '\n')
		f.write(','.join(str(x) for x in self.slopes) + '\n')
				
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
			
	return model
			
def classifyFunction(model, input, callback = None):
	result = model.getOutput(input)
	if callback:
		callback(result)
		
	return result
			
			