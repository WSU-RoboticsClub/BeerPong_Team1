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
		# map it to a (-1 - 1) range
		controller = Controller (["du", "dd", "start", "L1", "R1", "L2", "R2", "select"], ["speedUp", "speedDown", "launch", "lateralLeft", "lateralRight", "lateralLeftFast", "lateralRightFast", "allStop"], (0, 255), (-1, 1))
		#controller = Controller (["X1", "Y1", "X2", "Y2"])

		print "wating for controller to init"
		while(controller.get_values() == {}):
			sleep(.1)
		print "done"

		print "running!"
		while True:
			control_packet = controller.get_values()
			if(control_packet == {}):
				print "dropped control signal: all"

			try:
				if (control_packet["speedUp"] > button_threshold):
					print "Speeding up the motors"

				if (control_packet["speedDown"] > button_threshold):
					print "Slowing down the motors"

				if (control_packet["launch"] > -1):
					print "Firing!!"

				if (control_packet["lateralLeft"] > button_threshold):
					print "Moving left slowly"

				if (control_packet["lateralRight"] > button_threshold):
					print "Moving right slowly"

				if (control_packet["lateralLeftFast"] > button_threshold):
					print "Moving left quickly"

				if (control_packet["lateralRightFast"] > button_threshold):
					print "Moving right quickly"

				if (control_packet["allStop"] > button_threshold):
					print "Stopping!!!!!"

			except KeyError, e:
				print "dropped control signal: ", e


			sleep (.01)
		print "exiting xbox controller"

if __name__ == '__main__':
	controller = xboxcontroller()

	controller.run()
