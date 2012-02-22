import ctypes
from ctypes.wintypes import *

keys = ['F', 'G', 'H', 'J', 'K', 'L']

class KeyListener():
	def __init__(self, numOutputs):
		print 'KeyListener initialized with %s keys being listened' % numOutputs
		self.keys = globals()['keys'][:numOutputs]
		
	def getOutputs(self):
		result = []
		user32 = ctypes.windll.user32
		for key in self.keys:
			user32.GetAsyncKeyState.restype = WORD
			user32.GetAsyncKeyState.argtypes = [ctypes.c_char]
			down = user32.GetAsyncKeyState(key)
			result.append(1 if down else 0)
		
		return result