# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import network
from machine import Pin, SPI, PWM
import sh1106
import time

spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = sh1106.SH1106_SPI(128, 64, spi, Pin(27), Pin(26), Pin(5))

p12 = Pin(12, Pin.OUT) #close motor
p12.off()

display.sleep(False)
display.rotate(True)
display.fill(0)

def do_connect():
	sta_if = network.WLAN(network.STA_IF)
	if not sta_if.isconnected():
		print('connecting to network...')
		display.fill(0)
		display.text('connect to net...', 0, 0, 1)
		display.show()
		sta_if.active(True) 
		sta_if.connect('akuan', '13815805612')
		while not sta_if.isconnected():
			pass
	print('network config:', sta_if.ifconfig())
	display.fill(0)
	display.text('connect ok!!', 0, 16, 1)
	display.show()

do_connect()
p12.on()
time.sleep(0.1)
p12.off()