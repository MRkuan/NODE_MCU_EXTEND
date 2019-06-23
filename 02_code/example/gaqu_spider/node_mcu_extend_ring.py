from machine import Pin, PWM
import _thread
import time

# semp = _thread.allocate_semephare()
ring_lock = _thread.allocate_lock()
class ring_class:
	def __init__(self,ring_io):
		self.__ring_io = ring_io
		self.__ring_pwm = None
		self.__timeout = 1	
		self.__freq = 1
		self.__start_flag = False	
	def start_ring(self,freq = 1,timeout = 10):
		self.__freq = 1
		self.__timeout = timeout
		self.__start_flag = True
		# semp.post()

	def stop_ring(self):
		with ring_lock:
			if self.__ring_pwm :
				self.__ring_pwm.deinit() 
				self.__ring_pwm = None
				self.__start_flag = False
	
	def ring_thread(self):
		while True:
			# semp.pend()
			if(self.__start_flag == True):
				with ring_lock:
					self.__ring_pwm = PWM(Pin(self.__ring_io), self.__freq)
				time.sleep(self.__timeout)
				self.stop_ring()