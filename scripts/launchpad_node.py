#!/usr/bin/env python
import rospy
from launchpad_ctrl.msg import LaunchpadKey

import pygame.event
import pygame.midi
import random

import sys
import select
from launchpad import *

def main():
	pygame.init()
	rospy.init_node('launchpad', anonymous=True)
	pub = rospy.Publisher("launchpad_key_event", LaunchpadKey, queue_size = 10)


	lp = Launchpad()
	midi_input = lp.midi_input
	midi_output = lp.midi_output

	while not rospy.is_shutdown():
		#break when keyboard 'enter' pressed
		i,o,e = select.select([sys.stdin],[],[],0)
		out = False
		for s in i:
			if s == sys.stdin:
				input = sys.stdin.readline()
				out = True
		if(out):
			break
		#read launchpad input
		if not midi_input.poll():
			continue
	
		msg,timestamp = midi_input.read(1)[0]
		midi_output.note_on(msg[1],(msg[1]/10-1)*8+(msg[1]%10-1)+64)
		r = int(random.random() * 64)
		midi_output.write_short(0x90,msg[1],r)
		print("%s"%msg)
		pub.publish(parseKeyEvent(msg[1], msg[2]))


	#for i in range(64):
	#	midi_output.write_short(0x90,(i%8)+11+10*(i/8),i)
	#	midi_output.write_short(0x91,(i%8)+11+10*(i/8),i+64)

	#print Bye Bye
	lp.scrollText(0x4b,False,"Bye Bye")


	while not midi_input.poll():
		continue
	lp.disconnect()

if __name__ == "__main__":
	main()
