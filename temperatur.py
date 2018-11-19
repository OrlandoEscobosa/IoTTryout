#!/usr/bin/python3

import re, os
import RPi.GPIO as GPIO

# SensorId from /sys/bus/w1/devices
sensorid = "10-000802e78248"
sensorpath = "/sys/bus/w1/devices/%s/w1_slave" % sensorid

pin_led = 11

def read_temp(pfad):
    temp = None
    try:
        GPIO.output(pin_led, GPIO.LOW)
        datei = open(pfad, "r")
        zeile = datei.readline()
        if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", zeile):
            zeile = datei.readline()
            m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", zeile)
            if m:
                temp = float(m.group(2))/1000
        datei.close()
    except IOError:
        print( "Could not read the sensor" )
        GPIO.output(pin_led, GPIO.HIGH)
    return temp

def send_temp(temp):
    print( temp )

if __name__ == '__main__':
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_led, GPIO.OUT)

    temp = read_temp(sensorpath)

    if None != temp:
        send_temp(temp)
