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
		controller = Controller (["start", "du", "dd", "L1", "R1", "L2", "R2", "select", "O"], 
                                 ["launch", "inc_speed", "dec_speed", "slow_left", "slow_right", "fast_left", "fast_right", "takeover", "kill"], (0, 255), (-1, 1))
		#controller = Controller (["X1", "Y1", "X2", "Y2"])

		print "wating for controller to init"  
		while(controller.get_values() == {}):
			sleep(.1)
		print "done"
		speed = 0
		lat = 0
		print "running!"
		while True:
			control_packet = controller.get_values()
			if(control_packet == {}):
				print "dropped control signal: all"

			try:
				if (control_packet["kill"] > -1):
					print "toggling reset"
					sleep(1)
				if (control_packet["launch"] > button_threshold):
					print "launching!"
					sleep(1)
				
				if (control_packet["takeover"] > button_threshold):
					print "takeover"
					sleep(1)
					break

								
				speed += self.hysteresis(control_packet["inc_speed"]-control_packet["dec_speed"])
				
				
				lat += self.hysteresis(control_packet["fast_left"] - control_packet["fast_right"])

				lat += (self.hysteresis(control_packet["slow_left"] - control_packet["slow_right"]) / 2)

				if (speed > 20):
					speed = 20

				else:
					if (speed < 0):
						speed = 0 

				if (lat > 10):
					lat = 10

				else:
					if (lat < -10):
						lat = -10

				print "speed = %s  lateral position = %s" %(speed, lat)

				
			except KeyError, e:
				print "dropped control signal: ", e


			sleep (.1)
		print "exiting xbox controller"

if __name__ == '__main__':
	controller = xboxcontroller()

	controller.run()
