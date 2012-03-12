from svmutil import *
import math
import datetime
import helpers

#filename = 'data2_ringFinger_2.txt'
filename = '../data.txt'

def loadData(fn):
	f = open(fn)
	outputs = int(f.readline())
	print 'number of outputs: %s' % outputs
	lines = f.read().strip('\n').split('\n')
	data = map(lambda x: [int(y) for y in x.split(',')], lines)
	data = map(lambda x: [x[:-outputs], x[-outputs:]], data)
	return data
	
def makeModel(data):
	models = []#one model per output variable

	start = datetime.datetime.now()	

	inputs = [d[0] for d in data]
	#inputs = scaleInputs(inputs)
	
	for i in range(len(data[0][1])):
		outputs = [d[1][i] for d in data]
		
		prob = svm_problem(outputs, inputs)
		param = svm_parameter()
		param.kernel_type = LINEAR
		
		#cost parameter - the cost of misclassifying a value.  Increasing will produce a more perfect fit to training data,
		#but that may not generalize as well.  lowering seems to reduce training time, without a significant reduction in accuracy (sometimes increased)
		param.C = 0.001
		
		model = svm_train(prob, param)
		models.append(model)
	
	elapsed = datetime.datetime.now() - start
	print 'time to make model: ' + str(elapsed)

	return models
	
def getClassifyData(data):
	return makeModel(data)
	
def classifyFunction(models, inputs, callback = None):
	#svm_predict takes a list of answers (which is dumb), a list of inputs (where each input is a list of features), and a model class
	predictions = []	#contains detailed info about the prediction
	states = []			#contains just the 1 or 0
	
	for model in models:
		prediction = svm_predict([0], [inputs], model)
		state = prediction[0][0]
		
		predictions.append(prediction)
		states.append(state)

	if callback:
		callback(states)
		
	return predictions

def extractWeightVectorsAndOffset(models):
	result = []	#list of each model, where each model is a list of floats
	for model in models:
		dim = len(model.get_SV()[0])
		weights = [0 for _ in range(dim)]
		weights[0] = - svm_predict([0], [[0] *(dim-1)], model)[2][0][0]
		
		for i in range(dim-1):
			testVector = [1.0 if x == i else 0.0 for x in range(dim-1)]
			weights[i+1] = svm_predict([0], [testVector], model)[2][0][0] + weights[0]
		
		result.append(weights)
		
	return result
	
def main():
	fn = filename
	if len(sys.argv) > 1:
		fn = sys.argv[1]
		
	data = loadData(fn)
	numOutputs = len(data[0][1])
	
	data = helpers.removeTransitionDataPoints(data)
	
	training = data#[:len(data)*3/4]
	testing = data#[len(data)*3/4:]
	
	model = makeModel(training)
	
	#classifyFunction(model, [0, 1, 2, 3, 4, 5, 6, 7])
	#return
	matrices = [[[0, 0], [0, 0]] for _ in range(numOutputs)]
	for d in testing:
		inputs = d[:-1]
		predictData = classifyFunction(model, inputs[0])
		
		predictions = [int(x[0][0]) for x in predictData]
		answers = d[-1]
		
		for i, (pred, ans) in enumerate(zip(predictions, answers)):
			matrices[i][pred][ans] += 1
	
	for i in range(numOutputs):	
		correct = matrices[i][0][0] + matrices[i][1][1]
	
		print 'OUTPUT # %s: overall accuracy: %s' % (i, str(100.0 * correct / len(testing)))
	
		print 'error matrix: predicted on vertical, actual on horizontal' 
		print '\n'.join('\t'.join(str(mi) for mi in m) for m in matrices[i])
	
	
	modelComplete = makeModel(data)
	weights = extractWeightVectorsAndOffset(modelComplete)
	#return
	for i in range(numOutputs):			
		frequencyWeights = weights[i][1:]#0 term is the offset
		largest = max(frequencyWeights)
		
		print '\noffset: %s' % weights[i][0]
		print 'relative frequency bin weights:'
		relativeWeights = [x/largest for x in frequencyWeights]
		print '\n'.join(str(x) for x in relativeWeights)
	
	if 1:
		print '\n manual predictions based on extract weights vs model predictions'
		for d in testing:
			inputs = d[:-1][0]
			answer = d[-1]
			pred1 = [sum([t * w for w, t in zip(wv[1:], inputs)]) - wv[0] for wv in weights]
			pred2 = [x[2][0][0] for x in classifyFunction(modelComplete, inputs)]
			print pred1, pred2, answer
	
if __name__ == "__main__":
	main()