import RPi.GPIO as GPIO
import time

servoPIN_1 = 4
servoPIN_2 = 17
servoPIN_3 = 22
servoPIN_4 = 10

plist = (4, 17, 22, 10)
GPIO.setmode(GPIO.BCM)
for pin in plist:
    GPIO.setup(pin, GPIO.OUT)

p1 = GPIO.PWM(servoPIN_1, 50)
p2 = GPIO.PWM(servoPIN_2, 50)
p3 = GPIO.PWM(servoPIN_3, 50)
p4 = GPIO.PWM(servoPIN_4, 50)

waves = [p1, p2, p3, p4]
for wave in waves:
    wave.start(7.5)
    time.sleep(0.5)


global lastDegree
lastDegree = 0

def rotateDegreeBasic(p, degree):
    global lastDegree
    print(degree, lastDegree)
    print("rotate {}".format(degree))    
    if lastDegree < degree:
        step = 5
    else:
        step = -5
    for i in range(lastDegree, degree, step):
        cycle = 7.5 + (i / 90.0) * 5
        p.ChangeDutyCycle(cycle)
        time.sleep(0.05)

    time.sleep(0.2)
    lastDegree = degree




