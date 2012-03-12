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

import gestureDistanceCalculator
import stats

TESTING_FOLDS = 5	#number of times to break up the data and find distances

def calculateDividingLine(gestures, maybeGestures, nonGestures):
	numFolds = min(TESTING_FOLDS, len(gestures))
	
	allGestureDistances = []
	allNonGestureDistances = []
	
	for foldNum in range(numFolds):	
		trainingGestures = [gesture for i, gesture in enumerate(gestures) if i % numFolds != foldNum]
		testingGestures = [localTimeGestures for i, localTimeGestures in enumerate(maybeGestures) if i % numFolds == foldNum]
		
		#print 'train, test #s: ', len(trainingGestures), len(testingGestures)
		
		#make a distance calculator based on the subset of hte training data
		distanceCalculator = gestureDistanceCalculator.GestureDistanceCalculator(trainingGestures)
		
		#each localTimeGestures is a list of the closest times to when a gesture was identified in training
		#since the output can be triggered at slightly different times, we should look for a minimum near where
		#the gesture is known to have happened, compared to the training gestures
		gestureDistances = []
		#print testingGestures
		for localTimeGestureSet in testingGestures:
			
			closestDistance = min(map(distanceCalculator.getDistance, localTimeGestureSet))
			gestureDistances.append(closestDistance)
		
		#gestureDistances = map(distanceCalculator.getDistance, testingGestures)
		#print gestureDistances
		nonGestureDistances = map(distanceCalculator.getDistance, nonGestures)
		#print gestureDistances
		
		allGestureDistances += gestureDistances
		allNonGestureDistances += nonGestureDistances
		#break
		
	#print len(allGestureDistances), len(allNonGestureDistances)
	print 'means: ', stats.mean(allGestureDistances), stats.mean(allNonGestureDistances)
	
	print 'std devs: ', stats.stdDev(allGestureDistances), stats.stdDev(allNonGestureDistances)
	
	meanGesture = stats.mean(allGestureDistances)
	meanNon = stats.mean(allNonGestureDistances)
	
	devGesture = stats.stdDev(allGestureDistances)
	devNon = stats.stdDev(allNonGestureDistances)
	
	line = (meanGesture * devNon + meanNon * devGesture) / ( devGesture + devNon)
	
	#print line
	return line
	
class GestureRecognizer():
	def __init__(self, gestures, maybeGestures, nonGestures):
		self.distanceCalculator = gestureDistanceCalculator.GestureDistanceCalculator(gestures)
		#print nonGestures
		self.dividingLine = calculateDividingLine(gestures, maybeGestures, nonGestures)
		#print gestures
		
	def getOutput(self, input):
		minDistance = self.distanceCalculator.getDistance(input)
		isGesture = (minDistance < self.dividingLine)
		#return the distance as well to make debugging a little easier
		return isGesture, minDistance
		
