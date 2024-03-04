import RPi.GPIO as GPIO
import time
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
lock = Servo(12, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)
door = Servo(13, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000, pin_factory=factory)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
# print "HC-SR04 mesafe sensoru"
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
lock.min()
servo.min()

while True:
    GPIO.output(TRIG, False)
#     print "Olculuyor..."
    time.sleep(0.5)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()
    while GPIO.input(ECHO)==1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
 
    if distance > 2 and distance < 20:
        print("There is someone at the door")
        print("The door is opening")
        sleep(2)
        lock.max()
        for i in range(0, 180):
            door.value = math.sin(math.radians(i))
            sleep(0.01)
        sleep(5)
        print("The door is closing")
        sleep(2)
        for i in range(180, 360):
            door.value = math.sin(math.radians(i))
            sleep(0.01)
        lock.min()
        sleep(5)
        lock.value = None;
        door.value = None;
        break
    else:
        print("The door is secure")

