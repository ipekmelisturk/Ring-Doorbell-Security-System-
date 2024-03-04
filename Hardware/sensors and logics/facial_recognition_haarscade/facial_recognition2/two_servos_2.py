import RPi.GPIO as GPIO
import time
import math
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
lock = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
door = Servo(13, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lock.min()
door.min()
    
print("The door is opening")
sleep(1)
lock.max()
sleep(2)
for i in range(270, 450):
    door.value = math.sin(math.radians(i))
    sleep(0.01)
sleep(5)
print("The door is closing")
sleep(2)
for i in range(90, 270):
    door.value = math.sin(math.radians(i))
    sleep(0.01)

sleep(2)
lock.min()
sleep(5)
lock.value = None;
door.value = None;
print("The door is secure")

