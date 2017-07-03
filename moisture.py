#!/usr/bin/python
import time.sleep as sleep
import os
import RPi.GPIO as GPIO
#import pinlist
#pL = pinlist.getPins(itemNumber)


first = 21 # test pins
second = 20 # test pins

# change these as desired - they're the pins connected from the
# SPI port on the ADC 
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25

DEBUG = 1
# set up the SPI interface pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)


def takeRead(anPin,top,bottom):
	#set pins as output if not already
	GPIO.output(top, GPIO.OUT)
	GPIO.output(bottom, GPIO.OUT)
	#clear existing output
	GPIO.output(top, False)
	GPIO.output(bottom, False)
	#drive current through voltage divider
	#low = false
	#high = true
	GPIO.ouput(top, False)
	GPIO.output(bottom, True)
	#wait for capacitance
	sleep(1000)
	#read analog
	readadc(anPin, SPICLK, SPIMOSI, SPIMISO, SPICS)
	#reverse current
	GPIO.ouput(top, True)
	GPIO.output(bottom, False)
	return readadc

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

print takeRead(0,first,second) #return analog number, value of moisture

# air = 0
# damp = 250
# wet = 300+
