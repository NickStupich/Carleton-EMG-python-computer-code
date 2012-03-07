"""this builds off the gesture distance calculator, by using it.
Idea is to turn the distance from the gesture distance generated
by the distance calculator to output a boolean value of whether or not the 
gesture was likely to have been performed

taking subsections of training data and testing on the subsequent data,
we can find the mean distance between the actual gesture, and between
the non-gesture training data and the gestures.  With these two sets of 
distance, we find the mean distance and standard deviations to 
determine an appropriate dividing line between the two classes.  

Then at runtime it's gesture? = (minGestureDistance < dividingLine)

"""

from gestureDistanceCalculator import *

TESTING_FOLDS = 4	#number of times to break up the data and find distances

def calculateDividingLine(gestures, notGestures):
	numFolds = min(TESTING_FOLDS, len(gestures))
	

class GestureRecognizer():
	def __init__(self, gestures, notGestures):
		self.gestures = gestures
		self.distanceCalculator = GestureDistanceCalculator(self.gestures)
		self.dividingLine = calculateDividingLine(self.gestures, notGestures)
		
	def getOutput(self, input):
		minDistance = self.distanceCalculator.getOutput(input)
		isGesture = (minDistance < self.dividingLine)
		return isGesture
