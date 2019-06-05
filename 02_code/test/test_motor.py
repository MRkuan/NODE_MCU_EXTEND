from machine import Pin, PWM

pwm0 = PWM(Pin(12), freq=1) # create and configure in one go