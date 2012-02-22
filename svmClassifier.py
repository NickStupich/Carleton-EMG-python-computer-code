from svmutil import *
import math
import datetime

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
	prediction = svm_predict([0], [inputs], model)
	if callback:
		callback(prediction[0][0])
	return prediction
	
def main():
	fn = filename
	if len(sys.argv) > 1:
		fn = sys.argv[1]
		
	data = loadData(fn)
	model = makeModel(data)
	
	matrix = [[0, 0], [0, 0]]
	for d in data:
		inputs = d[:-1]
		answer = d[-1][0]
		predictData = classifyFunction(model, inputs)
		prediction = int(round(predictData[0][0]))
		#print prediction, answer
		matrix[prediction][answer] += 1
	
	correct = matrix[0][0] + matrix[1][1]
	
	print 'overall accuracy: ' + str(100.0 * correct / len(data))
	
	print 'error matrix: predicted on vertical, actual on horizontal' 
	print '\n'.join('\t'.join(str(mi) for mi in m) for m in matrix)

if __name__ == "__main__":
	main()