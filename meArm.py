import kinematics
import time
from math import pi
import RPi.GPIO as GPIO


servoPIN_1 = 4
servoPIN_2 = 17
servoPIN_3 = 22
servoPIN_4 = 10

class meArm():
	def __init__(self, sweepMinBase = 145, sweepMaxBase = 49, angleMinBase = -pi/4, angleMaxBase = pi/4,
				sweepMinShoulder = 118, sweepMaxShoulder = 22, angleMinShoulder = pi/4, angleMaxShoulder = 3*pi/4,
				sweepMinElbow = 144, sweepMaxElbow = 36, angleMinElbow = pi/4, angleMaxElbow = -pi/4,
				 sweepMinGripper = 75, sweepMaxGripper = 115, angleMinGripper = pi/2, angleMaxGripper = 0):
		"""Constructor for meArm - can use as default arm=meArm(), or supply calibration data for servos."""
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

		self.x = 1
		self.y = 1
		self.z = 1

		self.servoInfo = {}
		self.servoInfo["base"] = self.setupServo(sweepMinBase, sweepMaxBase, angleMinBase, angleMaxBase)
		self.servoInfo["shoulder"] = self.setupServo(sweepMinShoulder, sweepMaxShoulder, angleMinShoulder, angleMaxShoulder)
		self.servoInfo["elbow"] = self.setupServo(sweepMinElbow, sweepMaxElbow, angleMinElbow, angleMaxElbow)
		self.servoInfo["gripper"] = self.setupServo(sweepMinGripper, sweepMaxGripper, angleMinGripper, angleMaxGripper)

	def setupServo(self, n_min, n_max, a_min, a_max):
		"""Calculate servo calibration record to place in self.servoInfo"""
		rec = {}
		n_range = n_max - n_min
		a_range = a_max - a_min
		if a_range == 0:
			return
		gain = n_range / a_range
		zero = n_min - gain * a_min
		rec["gain"] = gain
		rec["zero"] = zero
		rec["min"] = n_min
		rec["max"] = n_max
		return rec
		

	def angle2pwm(self, servo, angle):
		"""Work out pulse length to use to achieve a given requested angle taking into account stored calibration data"""
		#ret = 150 + int(0.5 + (self.servoInfo[servo]["zero"] + self.servoInfo[servo]["gain"] * angle) * 450 / 180)
		# #return ret
		degree = self.rad2deg(angle)
		return 7.5 + (degree / 90.0) * 5

	def rad2deg(self, angle):
		return (angle / pi) * 180.0

	def goDirectlyTo(self, tarx, tary, tarz):
		angles = [0,0,0]
		print("From {},{},{}".format(self.x, self.y, self.z))
		print("goto=> {},{},{}".format(tarx, tary, tarz))
		print(kinematics.cart2polar(tary, tarx))
		if kinematics.solve(tarx, tary, tarz, angles):
			radBase = angles[0]
			radShoulder = angles[1]
			radElbow = angles[2]
			
			print("base=> {},{},{}".format(self.rad2deg(radBase), self.rad2deg(radShoulder), self.rad2deg(radElbow)))
			print("pwms=> {},{},{}".format(pwm_out_base, pwm_out_elbow, pwm_out_shoulder))
			pwm_out_base = self.angle2pwm("base", radBase)
			self.servoPWM["base"].ChangeDutyCycle(pwm_out_base)
			
			pwm_out_shoulder = self.angle2pwm("shoulder", radShoulder)
			self.servoPWM["shoulder"].ChangeDutyCycle(pwm_out_shoulder)

			pwm_out_elbow = self.angle2pwm("elbow", radElbow)
			self.servoPWM["elbow"].ChangeDutyCycle(pwm_out_elbow)

			self.x = tarx
			self.y = tary
			self.z = tarz
			
			
	def gotoPoint(self, x, y, z):
		"""Travel in a straight line from current position to a requested position"""
		x0 = self.x
		y0 = self.y
		z0 = self.z
		dist = kinematics.distance(x0, y0, z0, x, y, z)
		step = 10
		i = 0
		while i < dist:
			self.goDirectlyTo(x0 + (x - x0) * i / dist, y0 + (y - y0) * i / dist, z0 + (z - z0) * i / dist)
			time.sleep(0.05)
			i += step
		self.goDirectlyTo(x, y, z)
		time.sleep(0.05)
		
	def openGripper(self):
		"""Open the gripper, dropping whatever is being carried"""
		pwm_out_gripper = self.angle2pwm("gripper", pi/4.0)
		print(pwm_out_gripper)
		self.servoPWM["gripper"].ChangeDutyCycle(pwm_out_gripper)
		time.sleep(0.3)
		
	def closeGripper(self):
		"""Close the gripper, grabbing onto anything that might be there"""
		pwm_out_gripper = self.angle2pwm("gripper", pi/2.0)
		print(pwm_out_gripper)
		self.servoPWM["gripper"].ChangeDutyCycle(pwm_out_gripper)
		time.sleep(0.3)

	def isReachable(self, x, y, z):
		"""Returns True if the point is (theoretically) reachable by the gripper"""
		radBase = 0
		radShoulder = 0
		radElbow = 0
		return kinematics.solve(x, y, z, radBase, radShoulder, radElbow)

	def getPos(self):
		"""Returns the current position of the gripper"""
		return [self.x, self.y, self.z]
