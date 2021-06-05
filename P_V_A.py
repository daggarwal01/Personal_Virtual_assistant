import speech_recognition as sr
import time
from time import ctime
import face_recognition
import cv2
import pyttsx3
import glob
import sys
import os
import webbrowser
from nltk.tokenize import word_tokenize


# Command executing database
cmds= { "Chrome":"webbrowser.get('firefox').open('https://www.google.com')","Notepad": "os.system('gedit')","rhythmbox":"os.system('rhythmbox')","default":"Try again, your voice isn't clear"}

# Prompting features
available_cmd=["1. Open chrome","2. Open Notepad","3. Open rhythmbox", "4. Exit-to terminate chat_bot"]


video_capture = cv2.VideoCapture(0)


#globally defining the variable frame which capture the image for both the uses,
#old user verification and new user registration
global frame

#initializing the speech_recoginition module(globally)
r = sr.Recognizer()

#initializing the pyttsx3 module and setting talking speed of system
engine=pyttsx3.init()
engine.setProperty('rate',150)

images = [] #for storing the images from database
known_face_encodings = [] #for storing the face_encodings of database images
known_face_names = [] #for storing the name of the database images 
user_face_locations = [] # for storing the user's face locations
user_face_encoding = [] #for atoring the user's faces encodings

#Directory path where images are stored
dir=os.getcwd()
path=os.path.join(dir,"*.jpg")

#dividing the path in list of string,by removing the '/'
p=path.split('/')


########function for greeting with your name
def your_name(index):
    name = known_face_names[index]

    engine.say("hello "+name.split(".")[0]+", what can I do for you?")
    engine.runAndWait()
    return name
    

########function for recording the voice
def record_voice():
    with sr.Microphone() as source:
        print("Give any command from the list:")
        print('\n'.join(available_cmd))
        print("listening.....")
        r.adjust_for_ambient_noise(source)
        audio = r.record(source, duration=5)
        
    data = r.recognize_google(audio)
    print("You said: " + data)	
    return data

#######function for replying
def reply_box(d):
    fdata=word_tokenize(d)
    print(fdata)
    flag=0
    if 'exit' not in fdata:
        for i in cmds:
            if i in fdata:
                flag=1
                if i=="rhythmbox":
                    print("******************** If you want to continue, make sure your close rhythmbox **********************")
                exec(cmds[i])
        if flag ==0:
            print(cmds["default"])               
        
    else:
        sys.exit()

#######function for new registrations
def registration(name,frame):

    cv2.imwrite(name+'.jpg', frame)
    engine.say("thanks for registration "+name+", what can I do for you")
    print("thanks for registration "+name)
    engine.runAndWait()
    time.sleep(1)
   
#######capturing the image from the camera
def img_cap():
    
    while(True):
        
        # Capture the video frame by frame
        ret, frame = video_capture.read()
    
        # Display the resulting frame
        cv2.imshow('Enter Q to click your image for verification', frame)
        
        # the 'q' button is set as the quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    user_face_locations = face_recognition.face_locations(frame)
    user_face_encoding = face_recognition.face_encodings(frame, user_face_locations)
    chat_fun(user_face_encoding,frame)


######chat_bot executing function
def chat_fun(user_face_encoding,frame):

    print("Hello! I am your Personal Assistant.")

    try:

        # See if the face is a match from the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, user_face_encoding[0])
        #print(matches)

        # releasing the cap object
        video_capture.release()
        # Destroy all the windows
        cv2.destroyAllWindows()
        
        if True in matches:

            first_match_index = matches.index(True)
            name=your_name(first_match_index) #your_name function called for greeting
            
            while True:        
                try:   
                    reply_box(record_voice())#record_name function called in reply_box  function
                except sr.UnknownValueError or sr.WaitTimeoutError:
                    print("either you didn't say anthing or there was too much noise")
        else:
                
            engine.say("You are not authorised to use this chat bot,to continue using you have to register")
            engine.runAndWait()
            time.sleep(4)
            print("asking for registration")
            a=input("To register enter 'y' and then press enter"+'\n')
            
            if(a=='y'):

                new_name=input("pls insert your and then press enter"+'\n')
                registration(new_name,frame)   #record_voice())

                
                while True:        
                    try:
                        reply_box(record_voice())
                    except sr.UnknownValueError or sr.WaitTimeoutError:
                        print("either you didn't say anthing or there was too much noise")
            else:
                raise Exception("You cannot use this chat bot,program terminated with exit code 001")

    except IndexError:
        print("Make sure you are properly in front of camera and have proper lighting")
        img_cap()

################################################################################################

#getting the images from the image database folder
for im in glob.glob(path):

    a= cv2.imread(im)
    images.append(a)
    s=im.split('/') #spliting the image path for extracting the name of the image
    #print(s)

    #extracting the names from im path

    for i in s: # list 's' contains path of the images
        if i not in p: # list 'p' contains path to the directory where images are stored
            known_face_names.append(i)
#print(known_face_names)

#getting the face encodings of the images in database

for img in images:
    fen= face_recognition.face_encodings(img)[0]
    known_face_encodings.append(fen)
#print(known_face_encodings)
img_cap()
