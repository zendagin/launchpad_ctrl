#!/usr/bin/env python
import rospy
from launchpad_ctrl.msg import LaunchpadKey
from basic_mode import *



def callback(data):
	global current_mode, current_mode_number
	if(data.y == 8 and data.x >= 4):
		mode_number = data.x - 4
		if(mode_number != current_mode_number):
			current_mode = mode[mode_number]
			current_mode.start()
	else:
		current_mode.execute(data)
    
def listener():

	global modes, current_mode, current_mode_number
	modes = [BasicMode(0)]
	current_mode = modes[0]
	current_mode_number = 0

	rospy.init_node('launchpad_manager', anonymous=True)

	rospy.Subscriber("launchpad_key_event", LaunchpadKey, callback)

	current_mode.start()

	# spin() simply keeps python from exiting until this node is stopped
	rospy.spin()

if __name__ == '__main__':
    listener()
