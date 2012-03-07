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
			distance, closestMatch, systemOutput = modelGR.getOutput(previousData)
			print '\b' * 50 + str(round(distance, 2))
		
"""extracts the 'gesture' of outputs[0] moving from 0->1
gesture data format:
	dictionary of {gesture id : list of training data times},
	where each training data time is a list of fourier bins
	for all channels together"""	
def extractGestures1(data):
	gestures = {0: []} #only create gesture 0
	for i in range(len(data) - timeBefore - timeAfter):
		if data[i+timeBefore-2][1][0] == 0 and data[i + timeBefore-1][1][0] == 1:
			gestureData = [d[0] for d in data[i:i+timeBefore + timeAfter]]	#remove the outputs since we've already associated it with a gesture
			if NORMALIZE:
				gestures[0].append(normalizeData(gestureData))
			else:
				gestures[0].append(gestureData)
			
	return gestures
		
def main():
	global channels, state, trainingData, modelGR
	
	ser = SerialCommunication(everythingCallback)
	ser.Start(channels)
	state = programState.TRAINING
	
	print 'Hit enter to finish the training period'
	s = raw_input()
	state = programState.WAITING
	time.sleep(1)
	
	gestures = extractGestures1(trainingData)
	
	gesture0 = gestures[0]	#SHITTY!!!
	formattedGesture0 = [(g, 1.0) for g in gesture0]#get the data structure require by the gesture recognizer
	print formattedGesture0
	modelGR = GestureDistanceCalculator(gesture0)
	
	state = programState.RUNNING
	
	print 'Hit enter to finish the testing period'
	s = raw_input()
	state = programState.WAITING
	ser.Stop()
	
	
if __name__ =="__main__":
	main()
	
	
	