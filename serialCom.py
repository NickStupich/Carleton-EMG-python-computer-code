import serial
from threading import Thread
import time
import helpers
from helpers import FOURIER_BINS, NUM_CHANNELS

#serial port details
_port = "COM26"
_baud = 57600

#delay once the serial port read() doesn't immediately return anything (in seconds)
_readDelay = 0.01

#protocol details
CONTROL_BYTE = 255

DEBUG_ON = True
"""to easily turn debugging on/off once it starts to output way too much"""
def debug(s):
		if DEBUG_ON:
			print s
			
"""enums"""
class ExpectedNext:
	CONTROL = 1
	GAIN = 2
	DATA = 3

"""basically a structure to deal with the protocol of communication with the microcontroller"""
class FFTInfo:
	def __init__(self, channels):
		
		#get the number of channels being used
		self.numChannels = helpers.getNumChannels(channels)				
		print 'numChannels: %s' % self.numChannels
		
		self.gains = [-1]*self.numChannels
		
		self.data = [[0]*FOURIER_BINS for _ in range(self.numChannels)]
		self.expected = ExpectedNext.CONTROL
		
		self.channelIndex = 0
		self.dataIndex = 0
	
	"""returns a list of all the data.  This should probably be fed into a classification engine"""
	def getList(self):
		return reduce(lambda x, y: x+y, self.data)
		
	"""adds a byte to the list of data obtained for this cycle of data.  Returns true if the 
	chunk of data is complete and ready for getList() to be called and the data processed, false otherwise
	"""
	def addByte(self, byte):
		#debug('received byte: %s' % byte)
		if self.expected == ExpectedNext.CONTROL:	
			if not byte == CONTROL_BYTE:
				raise Exception("Expected Control byte, instead received %s" % byte)

			self.expected = ExpectedNext.GAIN

			#will return true unless it's the first loop through, where gain values are set to -1
			if self.gains[0] < 0:
				return False
			
			#return true here to indicate that we received the next control byte, and the last batch of data
			#is probably ok to be sent off for processing
				
			return True
		
		elif self.expected == ExpectedNext.GAIN:
			if byte == CONTROL_BYTE:
				raise Exception("Expected Gain, received control byte for channel %" % self.channelIndex)
			
			self.gains[self.channelIndex] = byte
			#debug('gain: %s' % byte)
			self.expected = ExpectedNext.DATA
		
		elif self.expected == ExpectedNext.DATA:
			if byte == CONTROL_BYTE:
				msg = "Expected Data, received control byte for channel %s    value %s" % (self.channelIndex, self.dataIndex)
				debug(msg)
				raise Exception(msg)
			
			self.data[self.channelIndex][self.dataIndex] = byte * self.gains[self.channelIndex]
				
			self.dataIndex += 1
			
			if self.dataIndex == FOURIER_BINS:
				self.dataIndex = 0
				self.channelIndex += 1
				self.expected = ExpectedNext.GAIN
				
				if self.channelIndex == self.numChannels:
					#go back to the start, expect a control byte next
					self.channelIndex = 0
					self.dataIndex = 0
					self.expected = ExpectedNext.CONTROL
					
		#return false to indicate that there is not a complete batch of data ready for processing
		return False
	
"""deals with the communication over the serial port, feeds data into the FFTInfo and calls a function
whenever a full 'chunk' of data has been received"""
class SerialCommunication(Thread):
	"""Opens the channel, but does not tell the controller to start doing stuff, nor does it start reading"""
	def __init__(self, newInfoCallback = None):
		Thread.__init__(self)
		self._callback = newInfoCallback
		self.ser = serial.Serial(port = _port, baudrate = _baud, timeout = 0)#opens automatically
		debug("Opened connection")
		self.dataReceived = []
		
		self.isRunning = False
		
	"""Tell the controller to start doing stuff, and start the reading thread"""
	def Start(self, channels):
		self.data = FFTInfo(channels)
		toSend = channels | (1<<7)
		success = False
		
		for retries in range(3):
			self.writeByte(toSend)#1 to indicate that it's a start command
			debug("Wrote start byte")
			self.isRunning = True
			#get the acknowledgement before we start the read thread
			while 1:
				b = self.ser.read(1)
				if b:
					b = ord(b)
					if b != toSend:
						print 'Acknowledgement bit received != start command sent. send: %s received: %s' % (toSend, b)
						self.ser.write(0)	#stop the thing
						time.sleep(2)		#make sure it has time to stop
						
						#then retry
						
						#raise Exception("Acknowledgement bit received != start command sent. send: %s received: %s" % (toSend, b))
					success = True
					break
			
			if success:
				debug("Received start ack")
				
				self.start()
				debug("started read thread")
				
				break
		
		if not success:
			raise Exception("Unable to properly start the bluetooth connection after %s tries" % 3);
		
		
	"""Called continuously to read data while we're running"""
	def run(self):
		while self.isRunning:
			while True:
				#debug('before ser.read(1)')
				char = self.ser.read(1)
				#debug('received %s' % char)
				if not char:
					#debug('not char - length is %s' % len(char))
					break
				
				byte = ord(char)
				#debug("Received byte %s" % byte)
				if self.data.addByte(byte):
					#this returns true when theres a complete batch of data ready
					if self._callback is not None:
						self._callback(self.data.getList()[:])
			
			time.sleep(_readDelay)
	
	"""Tell the conroller to stop doing stuff, and stop the reading threda"""
	def Stop(self):
		self.writeByte(0)
		self.isRunning = False
			
	def writeByte(self, byte):
		if not self.ser.isOpen():
			raise Exception("Attempted to write to a serial channel that is not open")
			
		count = self.ser.write(chr(byte))
		if count != 1:
			raise Exception("serial.write() returned a count of %s when 1 was expected" % count)
