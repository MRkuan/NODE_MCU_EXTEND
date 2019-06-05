from machine import Pin, SPI
import sh1106
import time

#1.first init spi
spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = sh1106.SH1106_SPI(128, 64, spi, Pin(27), Pin(26), Pin(5))

#2.close motor
p12 = Pin(12, Pin.OUT) #close motor
p12.off()

#3. init touch pad
key_1 = Pin(15, Pin.IN, Pin.PULL_UP)     # key1
key_2 = Pin(4, Pin.IN, Pin.PULL_UP)      # key2
key_3 = Pin(16, Pin.IN, Pin.PULL_UP)     # key3
key_4 = Pin(17, Pin.IN, Pin.PULL_UP)     # key4


display.sleep(False)
display.rotate(True)


def loop_det():
	while True:
		key_val_str = ''
		key_1_val = 0
		key_2_val = 0
		key_3_val = 0
		key_4_val = 0

		display.fill(0)
		display.text('k1  k2  k3  k4', 0, 0, 1)
		display.hline(0, 10, 128, 1)

		key_1_val = key_1.value()
		key_2_val = key_2.value()
		key_3_val = key_3.value()
		key_4_val = key_4.value()

		
		key_val_str = '{:d}   {:d}   {:d}   {:d}'.format(key_1_val, key_2_val, key_3_val, key_4_val)
		print (key_val_str)
		display.text(key_val_str, 0, 13, 1)
		display.show()
		time.sleep(0.1)

loop_det()