#!/usr/bin/python

import serial
import mido
import sys
import RPi.GPIO as GPIO
from mido.ports import BaseIOPort
import signal
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")

file_handler = logging.FileHandler("/home/pi/usbmidi.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

GPIO.setmode(GPIO.BCM) # refer to pins by their name on the board
GPIO.setup(5, GPIO.OUT)
GPIO.output(5, GPIO.LOW)

serial_name = '/dev/serial0'
baudrate = 31250

devices = [name for name in mido.get_input_names() if "through" not in name.lower()]
if not devices:
    logger.info('no devices found, goodbye!')
    sys.exit(1)

device = devices[0]

class SerialPort(BaseIOPort):

    def _open(self, **kwargs): 
        self.port = serial.Serial(
            port=serial_name, 
            baudrate=baudrate, 
            parity=serial.PARITY_NONE, 
            stopbits=serial.STOPBITS_ONE, 
            bytesize=serial.EIGHTBITS,
        )

    def _send(self, message): 
        command, note, velocity = message.bytes()
        self.port.write(message.bin())

    def _close(self):
        self.port.close()

usb_port = None
serial_port = None

def handle_usb_disconnect(sig, frame):
    logger.info("received signal, terminating")
    if serial_port is not None:
        serial_port.close()
    if usb_port is not None:
        usb_port.close()
    GPIO.output(5, GPIO.LOW)
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_usb_disconnect)
signal.signal(signal.SIGINT, handle_usb_disconnect)

try:
    usb_port = mido.open_input(device)
    serial_port = SerialPort()
    logger.info('listening to messages from %s', device)
    GPIO.output(5, GPIO.HIGH)
    for msg in usb_port: # blocks
        serial_port.send(msg)
finally:
    GPIO.output(5, GPIO.LOW)

