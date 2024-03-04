# from gpiozero import Button
# 
# button = Button(17)
# button.wait_for_press()
# print("Button is Berkin")
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
    input_state = GPIO.input(11)
    if input_state:
        print("Button pressed")
        time.sleep(0.2)