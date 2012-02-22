from svmutil import *
import math
import datetime
import helpers

filename = 'data2_ringFinger.txt'

def loadData(fn):
	f = open(fn)
	lines = f.read().strip('\n').split('\n')
	data = map(lambda x: [int(y) for y in x.split(',')], lines)
	data = map(lambda x: [x[:-1], x[-1:]], data)
	return data

"""scales inputs between 0-1 based on the largest value in the inputs"""
def scaleInputs(inputs):
	largest = max(map(lambda x: max(x), inputs))
	
	scaled = []
	for input in inputs:
		scaled.append([float(x) / largest for x in input])
		
	return scaled
	
def makeModel(data):
	start = datetime.datetime.now()
	inputs = [d[0] for d in data]
	outputs = [d[1][0] for d in data]
	
	scaled = scaleInputs(inputs)
	
	prob = svm_problem(outputs, inputs)
	param = svm_parameter()
	#param.svm_type = EPSILON_SVR
	param.kernel_type = LINEAR
	
	#cost parameter - the cost of misclassifying a value.  Increasing will produce a more perfect fit to training data,
	#but that may not generalize as well.  lowering seems to reduce training time, without a significant reduction in accuracy (sometimes increased)
	param.C = 0.01
	
	model = svm_train(prob, param)
	
	elapsed = datetime.datetime.now() - start
	print 'time to make model: ' + str(elapsed)
	
	return model
	
def getClassifyData(data):
	return makeModel(data)
	
def classifyFunction(model, inputs, callback = None):
	#svm_predict takes a list of answers (which is dumb), a list of inputs (where each input is a list of features), and a model class
	prediction = svm_predict([0], inputs, model)
	if callback:
		callback(prediction[0][0])
	return prediction
	
def extractWeightVectorAndOffset(model):
	dim = len(model.get_SV()[0])
	weights = [0 for _ in range(dim)]
	weights[0] = -classifyFunction(model, [[0] * dim])[2][0][0]
	
	for i in range(dim-1):
		testVector = [1.0 if x == i else 0.0 for x in range(dim-1)]
		#print testVector
		weights[i+1] = classifyFunction(model, [testVector])[2][0][0] + weights[0]
		
	#print weights
	
	#test = [float(x) for x in range(dim-1)]
	#pred1 = sum([t * w for w, t in zip(weights[1:], test)]) - weights[0]
	#pred2 = classifyFunction(model, [test])[2][0][0]
	#print pred1
	#print pred2
	
	return weights
	
def main():
	fn = filename
	if len(sys.argv) > 1:
		fn = sys.argv[1]
		
	data = loadData(fn)
	
	data = helpers.removeTransitionDataPoints(data)
	
	training = data[:len(data)*3/4]
	testing = data[len(data)*3/4:]
	
	model = makeModel(training)
	
	#classifyFunction(model, [0, 1, 2, 3, 4, 5, 6, 7])
	#return
	matrix = [[0, 0], [0, 0]]
	for d in testing:
		inputs = d[:-1]
		answer = d[-1][0]
		predictData = classifyFunction(model, inputs)
		#print predictData
		prediction = int(round(predictData[0][0]))
		#print prediction, answer
		matrix[prediction][answer] += 1
		#break
	
	correct = matrix[0][0] + matrix[1][1]
	
	print 'overall accuracy: ' + str(100.0 * correct / len(testing))
	
	print 'error matrix: predicted on vertical, actual on horizontal' 
	print '\n'.join('\t'.join(str(mi) for mi in m) for m in matrix)
	
	
	modelComplete = makeModel(data)
	weights = extractWeightVectorAndOffset(modelComplete)
	frequencyWeights = weights[1:]#0 term is the offset
	largest = max(frequencyWeights)
	
	print '\nrelative frequency bin weights:'
	relativeWeights = [x/largest for x in frequencyWeights]
	print '\n'.join(str(x) for x in relativeWeights)
	
	for d in testing:
		inputs = d[:-1][0]
		answer = d[-1][0]
		pred1 = sum([t * w for w, t in zip(weights[1:], inputs)]) - weights[0]
		pred2 = classifyFunction(modelComplete, [inputs])[2][0][0]
		print pred1, pred2, answer
	
if __name__ == "__main__":
	main()