import RPi.GPIO as GPIO
import time
import numpy as np
import cv2
import pyaudio
import wave

chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 5
filename = "audio.wav"


cap = cv2.VideoCapture(0)
width = 640
height = 480
cap.set(3, width)
cap.set(4, height)
# width = int(cap.get(3))
# height = int(cap.get(4))

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = 23
ECHO = 24
print("HC-SR04 mesafe sensoru")
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

while True:
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
        print("There is someone at the door")
        
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)              
        frames = []
        
        writer = cv2.VideoWriter('video.wav',
                cv.VideoWriter_fourcc(*'DIVX'),
                20,(width,height))
        
        for i in range(0, int(fs / chunk *seconds)):
            ret, frame = cap.read()
            writer.write(frame)
            cv2.imshow('Deneme', frame)
            
            data = stream.read(chunk)
            frames.append(data)
            
            # if cv2.waitKey(1) == ord('q'):
                # break
        
        cap.release()
        writer.release()
        cv2.destroyAllWindows()
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()
        break
        
    else:
        print ("The door is secure")