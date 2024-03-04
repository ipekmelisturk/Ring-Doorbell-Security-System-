from imutils.video import VideoStream
from imutils.video import FPS
import RPi.GPIO as GPIO
import time
import os
#import face_recognition
import imutils
import pickle
import cv2
import subprocess
# from face_rec_func import face_rec_func

def face_rec_func(vs, data):
    #Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "unknown"
    #Determine faces from encodings.pickle file model created from train_model.py
    # encodingsP = "encodings.pickle"

    # # load the known faces and embeddings along with OpenCV's Haar
    # # cascade for face detection
    # print("[INFO] loading encodings + face detector...")
    # data = pickle.loads(open(encodingsP, "rb").read())

    # # initialize the video stream and allow the camera sensor to warm up
    # # Set the ser to the followng
    # # src = 0 : for the build in single web cam, could be your laptop webcam
    # # src = 2 : I had to set it to 2 inorder to use the USB webcam attached to my laptop
    # vs = VideoStream(src=0,framerate=10).start()
    # #vs = VideoStream(usePiCamera=True).start()
    # time.sleep(2.0)

    # start the FPS counter
    fps = FPS().start()
    condition = 0
    # loop over frames from the video file stream
    while condition < 3:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)
        # Detect the fce boxes
        boxes = face_recognition.face_locations(frame)
        condition += 1
        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(frame, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                encoding)
            name = "Unknown" #if face is not recognized, then print Unknown

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                #If someone in your dataset is identified, print their name on the screen
                if currentname != name:
                    currentname = name
                    print(currentname)

            # update the list of names
            names.append(name)

        # # loop over the recognized faces
        # for ((top, right, bottom, left), name) in zip(boxes, names):
            # # draw the predicted face name on the image - color is in BGR
            # cv2.rectangle(frame, (left, top), (right, bottom),
                # (0, 255, 225), 2)
            # y = top - 15 if top - 15 > 15 else top + 15
            # cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                # .8, (0, 255, 255), 2)

        # display the image to our screen
        # cv2.imshow("Facial Recognition is Running", frame)
        #key = cv2.waitKey(1) & 0xFF

        # # quit when 'q' key is pressed
        if currentname != "unknown":
            break

        # update the FPS counter
        fps.update()

    # stop the timer and display FPS information
    fps.stop()
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

    # do a bit of cleanup
    cv2.destroyAllWindows()
    # vs.stop()

    return currentname
####################################################################
# Button Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Distance Sensor Setup
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

# Camera Setup
vs = VideoStream(src=0,framerate=10).start()
time.sleep(2.0)
encodingsP = "encodings.pickle"
data = pickle.loads(open(encodingsP, "rb").read())

cmd1 = "bluetoothctl connect $(bluetoothctl paired-devices | awk '{print $2}' | sed -n 1p) && bluetoothctl trust $(bluetoothctl paired-devices | awk '{print $2}' | sed -n 1p)"
cmd2 = "python3 two_servos_2.py"
cmd3 = "ffmpeg -threads 2 -itsoffset -0.6 -use_wallclock_as_timestamps 1 -thread_queue_size 16 -probesize 32 -analyzeduration 0 -fflags nobuffer -flags low_delay -f v4l2 -framerate 5 -video_size 240x192 -i /dev/video0 -f alsa -i hw:2,0 -c:a libopus -c:v vp8 -crf 18.0 -preset veryfast -b:a 10k -b:v 10k -f webm - | nc -l -p 1373"
cmd4 = "ls -A /home/pi/rpiserver"
cmd5 = "rm /home/pi/rpiserver/manageDoor.txt"
temp = 1
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
    
    if temp % 4 == 0:
        print("hi")
        output = str(subprocess.check_output(['ls', '-A', '/home/pi/rpiserver']))
        if "manageDoor.txt" in output:
            os.system(cmd2)
            os.system(cmd5)
            print("ezik")        
        print("melis")
    
    if distance > 2 and distance < 20:
        print("There is someone at the door")#,distance - 0.5,"cm"
        str_name = face_rec_func(vs, data)
        if str_name != "unknown":
            os.system(cmd2)
            str_name = "unknown"
        else:
            print ("Notification is sent")
            # burada yayın başlayacak
            vs.stop()
            vs.stream.release()
            os.system(cmd3)
            vs = VideoStream(src=0,framerate=10).start()
                        
    else:
        print ("The door is secure")
        temp += 1
        
        
