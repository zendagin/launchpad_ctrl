#!/usr/bin/env python
import random
import rospy
from std_msgs.msg import Empty
from launchpad_ctrl.msg import *

class BasicMode:
	def __init__(self, modeNum):
		self.modeNum = modeNum
		self.clear = rospy.Publisher("launchpad_clear", Empty, queue_size = 10)
		self.changeColor = rospy.Publisher("launchpad_color_change", LaunchpadColor, queue_size = 10)
		self.changeColorOne = rospy.Publisher("launchpad_color_change_one", LaunchpadColorOne, queue_size = 10)

	def start(self):
		self.clear.publish()
		xs = []
		ys = []
		rs = []
		gs = []
		bs = []
		for x in range(0,8):
			for y in range(0,8):
				xs.append(x)
				ys.append(y)
				rs.append(0)
				gs.append(63)
				bs.append(0)
		self.changeColor.publish(LaunchpadColor(xs,ys,rs,gs,bs))
		
	def execute(self, e):
		r = int(random.random() * 63)
		r2 = int(random.random() * r)
		r3 = int(random.random() * r)
		print(e.x)
		self.changeColor.publish(LaunchpadColor([e.x+1,e.x,e.x-1],[e.y,e.y,e.y],[r2,0,r2],[r,r,r],[r3,0,r3]))
