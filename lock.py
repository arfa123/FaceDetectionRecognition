import RPi.GPIO as GPIO
import time

def openLock():
    relay_pin = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin,GPIO.OUT)
    try:
        while True:
                #set low
            print ("Setting low - LED ON")
            GPIO.output (relay_pin,GPIO.LOW)
            time.sleep(2)
            #set high
            print ("Setting high - LED OFF")
            GPIO.output (relay_pin, GPIO.HIGH)
            time.sleep(2)
            break
    except KeyboardInterrupt:
        GPIO.cleanup()
        print ("Bye")