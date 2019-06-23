from machine import Pin, TouchPad
from micropython import const
import time
import _thread

_touch_threshold  = const(700)
key_class_lock = _thread.allocate_lock()
class key_class:
	def __init__(self, key1, key2, key3, key4, touch_key):
		self.__key1 = Pin(key1, Pin.IN, Pin.PULL_UP)     # key1
		self.__key2 = Pin(key2, Pin.IN, Pin.PULL_UP)     # key2
		self.__key3 = Pin(key3, Pin.IN, Pin.PULL_UP)     # key3
		self.__key4 = Pin(key4, Pin.IN, Pin.PULL_UP)     # key4
		self.__touch_key = TouchPad(Pin(touch_key))

		self.__key1_val = 0
		self.__key2_val = 0
		self.__key3_val = 0
		self.__key4_val = 0
		self.__touch_key_val = 0

	def get_key_val(self):
		with key_class_lock:
			val_tuple=(self.__key1_val,self.__key2_val,self.__key3_val,self.__key4_val,self.__touch_key_val)
		return val_tuple

	def key_thread(self):
		while True:
			with key_class_lock:
				if(0 == self.__key1.value()):
					self.__key1_val = 1
				else:
					self.__key1_val = 0

				if(0 == self.__key2.value()):
					self.__key2_val = 1
				else:
					self.__key2_val = 0

				if(0 == self.__key3.value()):
					self.__key3_val = 1
				else:
					self.__key3_val = 0

				if(0 == self.__key4.value()):
					self.__key4_val = 1
				else:
					self.__key4_val = 0

				val = self.__touch_key.read()
				if(val <= _touch_threshold):
					self.__touch_key_val = 1
				else:
					self.__touch_key_val = 0
			time.sleep(0.1)