#Sekiro

import cv2, numpy, os, winsound, ctypes
from PIL import ImageGrab, Image
from time import sleep, time

#plays a sound, set to false to disable
PLAYSOUND = True
#prints deaths after death, set to false to disable
PRINTDEATH = True

os.chdir(os.path.dirname(os.path.abspath(__file__)))

user32 = ctypes.windll.user32

h, w = int(user32.GetSystemMetrics(0) / 1920), int(user32.GetSystemMetrics(1) / 1080)

left, upper, right, lower = (795 * w, 310 * h, 1130 * w, 700 * h)

original = Image.open("SekiroDeath.png")

original.thumbnail((h * 1920, w * 1080))
    
original = numpy.asarray(original.crop((left, upper, right, lower)).convert("RGB"))

oR, oG, oB = cv2.split(original)

original = cv2.merge((oR, oG, oB))

low = numpy.array([147, 34, 34], dtype="uint16")
    
up = numpy.array([182, 42, 42], dtype='uint16')

orMask = cv2.inRange(original, low, up)

dTime = time()

#Image.new("RGB", (1920, 1080), (182, 42, 42)).show()

try:
    deaths = open("deaths.txt", 'r')
    
except:
    deaths = open("deaths.txt", 'w')
    deaths.write("0")
    deaths.close()
    deaths = open("deaths.txt", 'r')
    
totDeaths = int(deaths.read())
deaths.close()

while True:
    retry = 1
    while retry == 1:
        try:
            curImage = numpy.asarray(ImageGrab.grab((left,upper,right,lower)))
            retry = 0
        except:
            pass
        
    r, g, b = cv2.split(curImage)
    
    curImage = cv2.merge((r, g, b))
    
    redMask = cv2.inRange(curImage, low, up)
    
    difference = cv2.subtract(orMask, redMask)
    
    difference2 = cv2.subtract(redMask, orMask)
    
    if cv2.countNonZero(difference) <= 10000 and cv2.countNonZero(difference2) <= 10000 and time() - dTime > 1:
        dTime = time()
        totDeaths += 1
        deaths = open("deaths.txt", 'w')
        deaths.write(str(totDeaths))
        deaths.close()
        if PRINTDEATH:
            print('died')
        if PLAYSOUND:
            winsound.PlaySound("yes.wav", winsound.SND_ASYNC)
        
    sleep(5/1000)