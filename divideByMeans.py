import math

filename = 'data2_ringFinger.txt'

def loadData(fn):
	f = open(fn)
	lines = f.read().strip('\n').split('\n')
	data = map(lambda x: [int(y) for y in x.split(',')], lines)
	return data

def mean(l):
	return float(sum(l)) / len(l)
	
def stdDev(l):
	u = mean(l)
	x = sum([(u - li)**2.0 for li in l])
	x /= (len(l) - 1)
	return math.sqrt(x)
	
def getDividingLine(data):
	#take sum of all values, find optimal dividing line between the two classes
	sums = [[], []]
	for vals in data:
		s = sum(vals[:-1])
		sums[vals[-1]].append(s)
		
	mean1 = mean(sums[0])
	mean2 = mean(sums[1])

	stdDev1 = stdDev(sums[0])
	stdDev2 = stdDev(sums[1])

	print 'average of class 0: %s with stdDev: %s' % (mean1, stdDev1)
	print 'average of class 1: %s with stdDev: %s' % (mean2, stdDev2)

	#find a dividing line, which is just the weighted mean of the two classes
	line = (mean1 * stdDev2 + mean2 * stdDev1) / (stdDev1 + stdDev2)
	print 'dividing line: %s' % line

	#find the accuracy of the line
	matrix = [[0, 0], [0, 0]]
	for (answer, total) in enumerate(sums):
		for t in total:
			matrix[(t>line)][answer] += 1
			#print line, s, (s>line), answer
			#if (t > line) == answer:
			#	correct+= 1
	correct = matrix[0][0] + matrix[1][1]		

	total = len(data)
	accuracy = float(correct) / total

	print 'accuracy of dividing line:' + str(100 * accuracy)

	print 'error matrix: predicted on vertical, actual on horizontal' 
	print '\n'.join('\t'.join(str(mi) for mi in m) for m in matrix)
	
	return line

def getClassifyData(data):
	#convert to the format required
	formatted = [input + output for input, output in data]
	
	return getDividingLine(formatted)
	
def classifyFunction(model, inputs, callback = None):
	prediction = sum(inputs) > model
	if callback:
		callback(prediction)
		
	return prediction
	
def main():
	data = loadData(filename)
	line = getDividingLine(data)
			
if __name__ == "__main__":
	main()
	