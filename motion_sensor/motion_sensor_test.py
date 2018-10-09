#!/urs/bin/python
from time import sleep
import time
import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
GPIO.setup(23, GPIO.IN,pull_up_down=GPIO.PUD_UP)  # set a port/pin as an input  
#GPIO.setup(port_or_pin, GPIO.OUT) # set a port/pin as an output   
#GPIO.output(port_or_pin, 1)       # set an output port/pin value to 1/HIGH/True  
#GPIO.output(port_or_pin, 0)       # set an output port/pin value to 0/LOW/False

camera = PiCamera()
camera.resolution = (1024, 768)
camera.vflip = True
while True:
	i = GPIO.input(23)       # read status of pin/port and assign to variable i  
	print(i)
	print("Program is running \n")
	if (i == 0):
		filename = 'motion' +str(datetime.datetime.now()).split('.')[0]  + '.jpg'
		camera.capture(filename)
		print(str(datetime.datetime.now()).split('.')[0]+"motion detected!")
	sleep(0.1)
