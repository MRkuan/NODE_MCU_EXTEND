from machine import Pin, TouchPad
from micropython import const
import time
import _thread
import network
import socket
import ssl
current_hour_min_lock = _thread.allocate_lock()
gaqu_door_lock = _thread.allocate_lock()
class spider_class:
	def __init__(self):
		self.__hour = 0
		self.__min  = 0
		self.__door_state  = 0  # 0：规划中 1：空闲 2：在用 3：故障

	def __http_get(self, url):
		_, _, host, path = url.split('/', 3)
		addr = socket.getaddrinfo(host, 80)[0][-1]
		s = socket.socket()
		s.connect(addr)
		s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
		data = s.recv(512)
		s.close()
		return str(data, 'utf8')

	def get_current_hour_min(self):
		with current_hour_min_lock:
			val_tuple=(self.__hour,self.__min)
		return val_tuple

	def get_door_state(self):
		with gaqu_door_lock:
			var=self.__door_state
		return var

	def current_hour_min_thread(self):
		while True:
			try:
				str_s = self.__http_get('http://quan.suning.com/getSysTime.do')
				str_search = 'sysTime1'
				if (-1 == str_s.find(str_search)):
						print('no find sysTime1')
				else:
					nPos = str_s.index(str_search) + len('sysTime1') +2
					with current_hour_min_lock:
						self.__hour = int(str_s[nPos+9])*10 + int(str_s[nPos+10])
						self.__min = int(str_s[nPos+11])*10 + int(str_s[nPos+12])
				time.sleep(10)
			except:
				print('get thread time err')

	def gaqu_door_state_thread(self):
		while True:
			try:
				hour,min = self.get_current_hour_min()
				if ((hour>=20)and(hour<=21)):
					s = socket.socket()
					ai = socket.getaddrinfo("rest.ga-qu.com", 443)
					# print("Address infos:", ai)
					addr = ai[0][-1]
					# print("Connect address:", addr)
					s.connect(addr)
					s = ssl.wrap_socket(s)
					s.write(b"POST /api/infoOfCang HTTP/1.1\r\ncharset: utf-8\r\nAccept-Encoding: gzip\r\nreferer: https://servicewechat.com/wxe422d7571f00750b/30/page-frame.html\r\ncontent-type: application/x-www-form-urlencoded\r\nUser-Agent: Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36 MicroMessenger/6.7.3.1360(0x26070333) NetType/WIFI Language/zh_CN Process/appbrand0\r\nContent-Length: 48\r\nHost: rest.ga-qu.com\r\nConnection: Keep-Alive\r\n\r\nlongitude=119.415619&latitude=32.37545&range=10000")
					str_s = str(s.read(512), 'utf8')
					s.close()
					str_search = 'cangStatus'
					if (-1 == str_s.find(str_search)):
						print('no find cangStatus')
					else:
						nPos = str_s.index(str_search) + len('cangStatus') +2
						with gaqu_door_lock:
							self.__door_state = int(str_s[nPos])
					time.sleep(5)
				else:
					with gaqu_door_lock:
						self.__door_state = 0
					time.sleep(60)
			except:
				print('get door state err')
