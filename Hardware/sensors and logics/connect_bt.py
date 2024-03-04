import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
cmd1 = 'bluetoothctl connect $(bluetoothctl paired devices | awk '{print $2}' | sed -n 1p)'

while True:
    input_state = GPIO.input(11)
    if input_state:
        os.system(cmd1)
        time.sleep(0.2)
        print("connected")
        
    print("amanın")