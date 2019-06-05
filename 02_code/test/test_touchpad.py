from machine import Pin, SPI, TouchPad
import sh1106
import time

#1.first init spi
spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = sh1106.SH1106_SPI(128, 64, spi, Pin(27), Pin(26), Pin(5))

#2.close motor
p12 = Pin(12, Pin.OUT) #close motor
p12.off()

#3. init touch pad
t = TouchPad(Pin(32))

display.sleep(False)
display.rotate(True)


def loop_det():
	while True:
		val = t.read()
		print(val)
		display.fill(0)
		display.text('touchpad_val', 0, 0, 1)
		display.hline(0, 10, 128, 1)
		display.text(str(val), 0, 13, 1)
		display.show()
		time.sleep(1) 

loop_det()