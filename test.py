from serialCom import *
import time
from keyListener import *
import helpers

channels = sum([x<<i for i, x in enumerate([1, 0, 0, 0, 0, 0])])
numChannels = helpers.getNumChannels(channels)

count = 0
start = None

def timingCallback(array):
	global start, count
	if not start:
		start = time.time()
		
	count+=1
	if count % 100 == 0:
		print 'updates / second: %s' % (count / (time.time() - start))
	
def timingCallback2(array):
	global start, count
	if not start:
		start = time.time()
		
	limit = 100
		
	count += 1
	if count == limit:
		now = time.time()
		count = 0
		elapsed = now - start
		start = now
		print 'updates / second: %s' % (limit / elapsed)
	
i=0
def callback(array):
	global i
	i+=1
	if i % 10 == 0:		
		print '\t'.join([str(x) for x in array]) + ' -  %s' % sum(array) + ' \t\t %s' % str(sum(array) > 5000)
		#print '\n'
	
file = None	
def toFileCallback(array):
	global file
	if not file:
		file = open('data.txt', 'w')
	
	file.write('\t'.join([str(x) for x in array]) + '\n')
	
def train():
	print 'training...'
		
def main():
	#ser = SerialCommunication(callback)
	ser = SerialCommunication(timingCallback2)
	#ser = SerialCommunication(toFileCallback)
	
	ser.Start(channels)

	s = raw_input()
	ser.Stop()
	
from threading import Thread
class KeyTestThread(Thread):
	def run(self):
		
		kl = KeyListener(2)
		
		for _ in range(10):
			time.sleep(0.5)
			print kl.getOutputs()
	
if __name__ == "__main__":	
	main()