#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import Adafruit_ADS1x15
import math
import requests
import datetime
import json
import picamera
import base64

camera = picamera.PiCamera()
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1
SENSOR_THRESHOLD = 17000
DISCHARGE_SECONDS = 10
INTERVAL_SECONDS = 1800
POST_URL = "http://192.168.11.22:10024"
DIFF_JST_FROM_UTC = 9
IMAGE_FILE_PATH = "./image.jpg"

PIN = 4

values = [0] * 100


def setup():
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN, GPIO.OUT)
        GPIO.output(PIN, GPIO.HIGH)


def loop():
        while True:
                camera.capture(IMAGE_FILE_PATH)
                maxValue = 0
                # read some times to avoid pulse value
                for i in range(100):
                        values[i] = adc.read_adc(0, gain=GAIN)
                        if values[i] > maxValue:
                                maxValue = values[i]
                logger(
                        "info",
                        "read some times to avoid pulse value",
                        data={"Humidity": maxValue}
                )
                # if dry
                if (maxValue) > SENSOR_THRESHOLD:
                        post(postBuild(maxValue, 1))
                        GPIO.output(PIN, GPIO.LOW)
                        logger("info", "Pump OFF -> ON")
                        time.sleep(DISCHARGE_SECONDS)
                        GPIO.output(PIN, GPIO.HIGH)
                        logger("info", "Pump ON -> OFF")
                # if not dry
                else:
                        GPIO.output(PIN, GPIO.HIGH)
                        logger("info", "Pump keeps OFF")
                post(postBuild(maxValue, 0))
                time.sleep(INTERVAL_SECONDS)


def destroy():
        GPIO.setup(PIN, GPIO.IN)
        GPIO.cleanup()


def getNowTimestamp():
        return datetime.datetime.utcnow() + datetime.timedelta(hours=DIFF_JST_FROM_UTC)


def postBuild(humidity, action):
        with open(IMAGE_FILE_PATH, "rb") as image_file:
                data = base64.b64encode(image_file.read())

                return json.dumps({
                        'humidity': humidity,
                        'action': action,
                        'dischargeTime': 0 if action == 0 else DISCHARGE_SECONDS,
                        'threshold': SENSOR_THRESHOLD,
                        'createdAt': getNowTimestamp().strftime('%Y-%m-%dT%H:%M:%S+09:00'),
                        'image': data.decode('utf-8') 
                })

def post(data):
        response = requests.post(
                POST_URL, 
                data = data
        )

def logger(level, message, data = ""):
        print(getNowTimestamp().strftime('%Y-%m-%d %H:%M:%S') + ":[" + level + "] " + message + ":" + str(data))

if __name__ == '__main__':
        setup()
        try:
                loop()
        except KeyboardInterrupt:
                destroy()
