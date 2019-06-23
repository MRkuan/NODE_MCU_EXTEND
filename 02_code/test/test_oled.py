from machine import Pin, SPI
import sh1106
import time

spi = SPI(1, baudrate=1000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = sh1106.SH1106_SPI(128, 64, spi, Pin(27), Pin(26), Pin(5))

p12 = Pin(12, Pin.OUT) #close motor
p12.off()

display.sleep(False)
display.rotate(True)


display.fill(0)
display.text('NODE_MCU_EXTEND', 0, 0, 1)
display.text('V1.0', 0, 8, 1)
display.text('@micropython', 0, 64-8, 1)
display.show()

