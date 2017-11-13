#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from launchpad_ctrl.msg import LaunchpadKey

import pygame.event
import pygame.midi
import random

import sys
import select

def find_devices():
	pygame.midi.init()
	n_devices = pygame.midi.get_count()
	target_name = "Launchpad MK2 MIDI 1"
	ret = {'input':-1,'output':-1}
	
	for d in range(n_devices):
		di = pygame.midi.get_device_info(d)
		print("Device %d: %s"%(d,str(di)))
		if di[1] == target_name and di[2] == 1:
			# Input side
			print("Found target input device")
			ret['input'] = d
		elif di[1] == target_name and di[3] == 1:
			# Output side
			print("Found target output device")
			ret['output'] = d
	print(ret)
	#pygame.midi.quit()
	return ret
	

class Launchpad:
	def __init__(self):
		ret = find_devices()
		self.in_id = ret['input']
		self.out_id = ret['output']
		self.connect()
		#pygame.midi.init()

	def connect(self):
		self.midi_input = pygame.midi.Input(self.in_id)
		self.midi_output = pygame.midi.Output(self.out_id)
		self.led_off()
		#flush
		rospy.sleep(0.1)
		while(self.midi_input.poll()):
			self.midi_input.read(1)

	def disconnect(self):
		self.led_off()
		self.midi_input.close()
		self.midi_output.close()

	def led_off(self):
		self.midi_output.write_sys_ex(0,'\xf0\x00\x20\x29\x02\x18\x0e\x00\xf7')

def parse_key_event(keyNum, keydown):
	event = LaunchpadKey()
	event.type = 'square'
	if(keydown == 0):
		event.keydown = False
	else:
		event.keydown = True
	if(keyNum >= 104):
		event.y = 8
		event.x = keyNum - 104
		event.type = {
			104: 'UP',
			105: 'DOWN',
			106: 'LEFT',
			107: 'RIGHT',
			108: 'SESSION',
			109: 'USER_1',
			110: 'USER_2',
			111: 'MIXER'
		}[keyNum]
	else:
		event.x = keyNum/10 - 1
		event.y = keyNum%10 - 1
	if(event.y == 8):
		event.type = {
			0: 'RECORD_ARM',
			1: 'SOLO',
			2: 'MUTE',
			3: 'STOP',
			4: 'SEND_B',
			5: 'SEND_A',
			6: 'PAN',
			7: 'VOLUME'
		}[event.x]
	return event

#main
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
	pub.publish(parse_key_event(msg[1], msg[2]))


for i in range(64):
	midi_output.write_short(0x90,(i%8)+11+10*(i/8),i)
	midi_output.write_short(0x91,(i%8)+11+10*(i/8),i+64)
rospy.sleep(2)
lp.disconnect()

#if __name__ == "__main__":
#	main()
