from machine import Pin, SPI
import sh1106
import time
import network
import socket
import node_mcu_extend_key
import node_mcu_extend_spider
import node_mcu_extend_pic
import node_mcu_extend_ring
import _thread
import boot

p12 = Pin(12, Pin.OUT) #close motor
p12.off()

key_all = node_mcu_extend_key.key_class(15,4,16,17,32)
_thread.start_new_thread(key_all.key_thread, ())

spider_all = node_mcu_extend_spider.spider_class()
_thread.start_new_thread(spider_all.gaqu_door_state_thread, ())
_thread.start_new_thread(spider_all.current_hour_min_thread, ())

ring_all = node_mcu_extend_ring.ring_class(12)
_thread.start_new_thread(ring_all.ring_thread, ())

def show_time(hour,min):
	boot.display.fill(0)
	hour_high =  hour//10
	hour_low = hour%10
	min_high = min//10
	min_low =  min%10
	# print(hour_high,hour_low,min_high,min_low)
	boot.display.fill(0)
	boot.display.diplay_pic(12,16,12+16,16+32,node_mcu_extend_pic.num_pic[hour_high])
	boot.display.diplay_pic(12+16+6,16,12+16+16+6,16+32,node_mcu_extend_pic.num_pic[hour_low])
	boot.display.diplay_pic(12+16+16+6+6,16,12+16+16+16+6+6,16+32,node_mcu_extend_pic.point_pic)
	boot.display.diplay_pic(12+16+16+16+6+6+6,16,12+16+16+16+16+6+6+6,16+32,node_mcu_extend_pic.num_pic[min_high])
	boot.display.diplay_pic(12+16+16+16+16+6+6+6+6,16,12+16+16+16+16+16+6+6+6+6,16+32,node_mcu_extend_pic.num_pic[min_low])
	boot.display.show()

def show_door():
	boot.display.fill(0)
	boot.display.diplay_pic(32,0,32+64,64,node_mcu_extend_pic.treadmill_pic)
	boot.display.show()

while True:
	hour,min = spider_all.get_current_hour_min()

	door_state = spider_all.get_door_state()
	print("door_state:",door_state)
	if (1 == door_state) :
		show_door()
		# ring_all.start_ring()
	else:
		show_time(hour,min)
		# ring_all.stop_ring()

	time.sleep(1)
	pass
