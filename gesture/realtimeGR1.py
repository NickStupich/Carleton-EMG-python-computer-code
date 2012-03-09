import stats
import math
import dtw
import distances
import knn
from datetime import datetime
import functools
from serialCom import *
from keyListener import *
import sys
import helpers
import time
from gestureDistanceCalculator import *

channels = sum([x<<i for i, x in enumerate([1, 0, 0, 0, 0, 0])])
numChannels = helpers.getNumChannels(channels)

keyListener = KeyListener(numChannels)

"""number of transforms before and after a gesture is performed to
consider when finding training data.
Larger -> greater accuracy (i assume)
Smaller -> quicker response to inputs, better performance
"""
timeBefore = 4
timeAfter = 2
minDistanceAway = 8	#for non-gesture extraction
maybeDistanceAway = 3 #allow space on either side for training the system to draw the dividing line

class programState():
	WAITING = 1
	TRAINING = 2
	RUNNING = 3
	
state = programState.WAITING
USE_SUM_OF_DATA	= False
NORMALIZE = False

modelGR = None

trainingData = []
previousData = []
def everythingCallback(data):
	global trainingData, modelGR, previousData
	
	if state == programState.WAITING:
		pass
	elif state == programState.TRAINING:
		keyState = globals()['keyListener'].getOutputs()
	
		if USE_SUM_OF_DATA:
			trainingData.append((sum(data), keyState))
		else:
			trainingData.append((data, keyState))
			
	elif state == programState.RUNNING:
		previousData.append(data)
		if len(previousData) > (timeBefore + timeAfter):
			previousData = previousData[1:]
			#distance, closestMatch, systemOutput = modelGR.getOutput(previousData)
			#print '\b' * 50 + str(round(distance, 2))
		
			output, distance = modelGR.getOutput(previousData)
			sys.stdout.write('\b'* 50 + str(output) + '\t\t' + str(round(distance, 1)))
			
"""extracts the 'gesture' of outputs[0] moving from 0->1
gesture data format:
	dictionary of {gesture id : list of training data times},
	where each training data time is a list of fourier bins
	for all channels together"""	
def extractGesturesAndMaybe1(data):
	gestures = {0: []} #only create gesture 0
	maybeGestures = {0: []}
	
	for i in range(len(data) - timeBefore - timeAfter):
		if data[i+timeBefore-2][1][0] == 0 and data[i + timeBefore-1][1][0] == 1:
			#get the gesture
			gestureData = [d[0] for d in data[i:i+timeBefore + timeAfter]]	#remove the outputs since we've already associated it with a gesture
			if NORMALIZE:
				gestures[0].append(normalizeData(gestureData))
			else:
				gestures[0].append(gestureData)
			
			thisMaybeGesture = []
			#get the maybe gestures used for training
			for j in range(max(0, i - maybeDistanceAway), min(len(data)-timeBefore-timeAfter-1, i + maybeDistanceAway)):
				gestureData = [d[0] for d in data[j:j+timeBefore + timeAfter]]	#remove the outputs since we've already associated it with a gesture
				thisMaybeGesture.append(gestureData)
				
			maybeGestures[0].append(thisMaybeGesture)
			
	return gestures, maybeGestures
	
def extractNonGestures(data):
	global minDistanceAway
	farEnough = [1 for _ in range(len(data))]
	
	for i in range(1, len(data)):
		if data[i-1][1][0] == 0 and data[i][1][0] == 1:
			for j in range(max(0, i-minDistanceAway), min(len(data)-1, i+minDistanceAway)):
				farEnough[j] = 0
			
	#print '\n'.join(str(x1) + '\t' + str(x2) for x1, x2 in enumerate(farEnough))
	
	result = []
	
	for i in range(0, len(data) - timeBefore - timeAfter):
		j = i + timeBefore + timeAfter
		if farEnough[i] and farEnough[j]:#since the (timeBefore + timeAfter) < minDistanceAway this is safe
			nonGesture = [d[0] for d in data[i:j]]
			result.append(nonGesture)
	
	return result
	
def main():
	global channels, state, trainingData, modelGR
	
	ser = SerialCommunication(everythingCallback)
	ser.Start(channels)
	state = programState.TRAINING
	
	print 'Hit enter to finish the training period'
	s = raw_input()
	state = programState.WAITING
	time.sleep(1)
	
	gestures, maybeGestures = extractGestures1(trainingData)
	
	gesture0 = gestures[0]	#SHITTY!!!
	maybeGestures0 = maybeGestures[0]
	nonGesture = extractNonGestures(trainingData)
	
	modelGR = gestureRecognizer.GestureRecognizer(gesture0, maybeGesture0, nonGesture)
	
	"""
	formattedGesture0 = [(g, 1.0) for g in gesture0]#get the data structure require by the gesture recognizer
	print formattedGesture0
	
	modelGR = GestureDistanceCalculator(gesture0)
	"""
	state = programState.RUNNING
	
	print 'Hit enter to finish the testing period'
	s = raw_input()
	state = programState.WAITING
	ser.Stop()
	
	
if __name__ =="__main__":
	main()
	
	
	