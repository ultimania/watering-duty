#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import math

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
SENSOR_THRESHOLD = 17000

PIN = 4

values = [0] * 100

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(PIN, GPIO.OUT)
	GPIO.output(PIN, GPIO.HIGH)

def loop():
	while True:
		maxValue = 0
		# read some times to avoid pulse value
		for i in range(100):
			values[i] = adc.read_adc(0, gain = GAIN)
			if values[i] > maxValue:
				maxValue = values[i]
		print("maxValue == " + str(maxValue))
		# if dry
		if (maxValue) > SENSOR_THRESHOLD:
			GPIO.output(PIN, GPIO.LOW)
			print("Pump is ON")
		# if not dry
		else:
			GPIO.output(PIN, GPIO.HIGH)
			print("Pump is OFF")
		time.sleep(0.5)

def destroy():
	GPIO.setup(PIN, GPIO.IN)
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
