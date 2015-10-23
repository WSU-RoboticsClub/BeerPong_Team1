#!/usr/bin/python


from xboxdrv.xboxdrv_parser import Controller
from time import sleep
#from sys import exit
#import signal


class xboxcontroller():
	def __init__(self):
		pass

	def hysteresis(self, value, threshold = .1):
		if (abs(value) > threshold):
			return value
		else: return 0

	def run(self):
		global running
		button_threshold = -0.5

		# Get input from the two analog sticks as yaw, throttle, roll, and pitch. Take the (0 - 255) input value and
		# map it to a (-1 - 1) range.
		controller = Controller (["L2", "R2", "R1", "L1", "start", "du", "dd"], ["yawLeftSlow", "yawRightSlow", "yawRightFast", "yawLeftFast", "Launch", "speedUp", "speedDown"])
		#controller = Controller (["X1", "Y1", "X2", "Y2"])

		print "wating for controller to init"
		while(controller.get_values() == {}):
			sleep(.1)
		print "done"

		print "running!"
		speedCounter = 0
                position = 0
                while True:
                
			control_packet = controller.get_values()
			if(control_packet == {}):
				print "dropped control signal: all"

			try:
				if (control_packet["yawLeftSlow"] > 5):
					print "going left slowly"
                                        position -= 1
                                        print position
					sleep(1)
                                if (control_packet["yawLeftFast"] > 200):
					print "going left fast"
                                        position -= 3
                                        print position
					sleep(1)
                                if (control_packet["yawRightSlow"] > 5):
					print "going right slowly"
                                        position += 1
                                        print position
					sleep(1)
                                if (control_packet["yawRightFast"] > 200):
					print "going right fast"
                                        position += 3
                                        print position
					sleep(1)
                                if (control_packet["Launch"] > 200):
					print "Launched"
					sleep(1)
                                if (control_packet["speedUp"] > 200):
					print "Speed up "
                                        if (speedCounter < 20):
                                                speedCounter += 1
                                                print speedCounter
					sleep(1)
                                if (control_packet["speedDown"] > 5):
					print "Speed down " 
                                        if (speedCounter > 0):
                                                speedCounter -= 1
                                                print speedCounter
					sleep(1)

				#yls = self.hysteresis(-control_packet["pitch"])
				#ylf = self.hysteresis(-control_packet["roll"])
				#yrs = self.hysteresis(-control_packet["yaw"])
				#yrf = self.hysteresis(-control_packet["pitch"])
				#launc = self.hysteresis(-control_packet["roll"])
				#speedu = self.hysteresis(-control_packet["yaw"])
				#speedd = self.hysteresis(-control_packet["pitch"])

				#print "left slow=%s left fast=%s rightslow=%s rightfast=%s Launch=%s speedingup=%s speedingdown=%s" %(yls, ylf, yrs, yrf, launc, speedu, speedd)
			except KeyError, e:
				print "dropped control signal: ", e


			sleep (.1)
		print "exiting xbox controller"

if __name__ == '__main__':
	controller = xboxcontroller()

	controller.run()
