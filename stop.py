#!/usr/bin/python

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) # refer to pins by their name on the board
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)

import os
os.system('pkill -f usbmidi.py')
