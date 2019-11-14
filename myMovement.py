import kinematics
import time
from math import pi
from math import *
import RPi.GPIO as GPIO

servoPIN_1 = 4
servoPIN_2 = 17
servoPIN_3 = 22
servoPIN_4 = 10

class meArm():
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.plist = [servoPIN_1, servoPIN_2, servoPIN_3, servoPIN_4]
		for pin in self.plist:
			GPIO.setup(pin, GPIO.OUT)

		p1 = GPIO.PWM(servoPIN_1, 50)
		p2 = GPIO.PWM(servoPIN_2, 50)
		p3 = GPIO.PWM(servoPIN_3, 50)
		p4 = GPIO.PWM(servoPIN_4, 50)

		self.servoPWM = {}
		self.servoPWM["base"] = p1
		self.servoPWM["shoulder"] = p2
		self.servoPWM["elbow"] = p3
		self.servoPWM["gripper"] = p4

		print("Init Servo")
		for p in self.servoPWM.values():
			p.start(7.5)
			time.sleep(0.5)
		print("Fin init")

		self.baseAngle = 0
		self.shoulderAngle = 0
		self.elbowAngle = 0

	def rad2deg(self, angle):
		return (angle / pi) * 180.0

	def rotateDegreeBasic(self, pName, degree):
		cycleLen = 7.5 + (degree / 90.0) * 5
		if cycleLen > 12.5 or cycleLen < 2.5:
			return False
		self.servoPWM[pName].ChangeDutyCycle(cycleLen)
		return True

	def rotateDegree(self, pName, degree, lastDegree):
		cycleLen = 7.5 + (degree / 90.0) * 5
		if cycleLen > 12.5 or cycleLen < 2.5:
			return False
		if lastDegree < degree:
			step = -5
		if lastDegree > degree:
			step = 5
		for deg in range(degree, lastDegree, step):
			cycleLen = 7.5 + (deg / 90.0) * 5
			self.servoPWM[pName].ChangeDutyCycle(cycleLen)
		time.sleep(0.2)	
		return True
			
	def gotoPoint(self, x, y, z):
		tempBaseAngle = self.rad2deg(atan(x/y))
		distance = sqrt(pow(x, 2) + pow(y, 2))

		shoulderGrad = asin((distance + 80)/ 80)
		tempShoulderAngle = self.rad2deg(shoulderGrad)
		baseHeight = 80 * cos(shoulderGrad) + 68

		elbowGrad = asin((z - baseHeight) / 80)
		tempElbowAngle = self.rad2deg(elbowGrad)

		print("Angles: {}, {}, {}".format(tempBaseAngle, tempElbowAngle, tempShoulderAngle))
		if self.rotateDegree("base", tempBaseAngle, self.baseAngle):
			self.baseAngle = tempBaseAngle
		
		if self.rotateDegree("shoulder", tempShoulderAngle, self.shoulderAngle):
			self.shoulderAngle = tempShoulderAngle

		if self.rotateDegree("elbow", tempElbowAngle, self.elbowAngle):
			self.elbowAngle = tempElbowAngle

		
	def openGripper(self):
		"""Open the gripper, dropping whatever is being carried"""
		self.rotateDegreeBasic("gripper", 20)
		time.sleep(0.3)
		
	def closeGripper(self):
		"""Close the gripper, grabbing onto anything that might be there"""
		self.rotateDegreeBasic("gripper", 70)
		time.sleep(0.3)

	def getPos(self):
		"""Returns the current position of the gripper"""
		return [self.baseAngle, self.outreach, self.heightAdj]
