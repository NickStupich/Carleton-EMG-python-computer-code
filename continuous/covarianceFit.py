import helpers
import stats

class FitType:
	LINEAR = 1
	EXPONENTIAL = 2
	SIGMOIDAL = 3
	
fitType = FitType.LINEAR

if fitType == FitType.LINEAR:  #for a linear fit
	fittingFunction = stats.lineOfBestFit
	interpolatingFunction = stats.lineInterpolation

elif fitType == FitType.EXPONENTIAL: #for a decaying exponential fit
	fittingFunction = stats.exponentialDecayFit
	interpolatingFunction = stats.exponentialInterpolation
	
elif fitType == FitType.SIGMOIDAL:
	fittingFunction = stats.sigmoidalFit
	interpolatingFunction = stats.sigmoidalInterpolation

def loadData(fn = '../data_continuous_.txt'):
	f = open(fn)
	numOutputs = int(f.readline())
	result = []
	for line in f:
		d = [int(x) for x in line.split('\t')[:-numOutputs]]
		o = [float(x) for x in line.split('\t')[-numOutputs:]]
		result.append((d, o))
		
	return result

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
				predicted = interpolatingFunction(input[j], (self.slopes[j][i], self.yInts[j][i]))
				num += predicted * self.pearsons[j][i]
				denom += abs(self.pearsons[j][i])
				
			result.append(num / denom)
			
		return result
		
	def save(self, filename = "covLinModel.txt"):
		f = open(filename, 'w')
		s = self.getDescription()
		f.write(s)
		f.close()
				
	def printModel(self):
		s = self.getDescription()
		print s
		
	def getDescription(self):
		s = ','.join(str(x) for x in [self.__numInputs, self.__numOutputs]) + '\n' \
		+ ','.join(str(x) for x in self.pearsons) + '\n' \
		+ ','.join(str(x) for x in self.yInts) + '\n' \
		+ ','.join(str(x) for x in self.slopes) + '\n'
		return s
				
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
			
			(slope, yInt) = fittingFunction(x, y)
			
			model.slopes[input][output] = slope
			model.yInts[input][output] = yInt
			
	return model
			
def classifyFunction(model, input, callback = None):
	result = model.getOutput(input)
	if callback:
		callback(result)
		
	return result
			
if __name__ == "__main__":
	data = loadData()
	model = getModel(data)
	model.printModel()
	
	f = open('fit estimates.txt', 'w')
	channel = 1
	
	#get some idea of the level of errors
	totalError = 0
	for input, output in data:
		pred = model.getOutput(input)
		err = sum([(p-o)**2.0 for p, o in zip(pred, output)])
		totalError += err
		
		p = interpolatingFunction(input[0], (model.slopes[0][0], model.yInts[0][0]))
		f.write('%s\t%s\t%s\n' % (input[0], p, output[0]))
		
	f.close()
		
	averageError = totalError / len(data)
	
	print 'average distance squared between predicted and actual output: %s' % averageError
		
		
	