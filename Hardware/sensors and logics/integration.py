import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

cmd1 = "bluetoothctl connect $(bluetoothctl paired-devices | awk '{print $2}' | sed -n 1p)"

while True:
    input_state = GPIO.input(17)
        
    if input_state:
        os.system(cmd1)
        time.sleep(0.2)
        print("connected")
    
    GPIO.output(TRIG, False)
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
        print("There is someone at the door")#,distance - 0.5,"cm"
    else:
        print ("The door is secure")
