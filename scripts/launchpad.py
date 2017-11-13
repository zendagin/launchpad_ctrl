import pygame.midi
import rospy

def findDevices():
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
		self.connect()
		#pygame.midi.init()

	def connect(self):
		ret = findDevices()
		self.in_id = ret['input']
		self.out_id = ret['output']
		self.midi_input = pygame.midi.Input(self.in_id)
		self.midi_output = pygame.midi.Output(self.out_id)
		self.ledOff()
		#flush
		rospy.sleep(0.1)
		while(self.midi_input.poll()):
			self.midi_input.read(1)

	def disconnect(self):
		self.ledOff()
		self.midi_input.close()
		self.midi_output.close()
		pygame.midi.quit()

	def ledOff(self):
		self.midi_output.write_sys_ex(0,[0xf0,0x00,0x20,0x29,0x02,0x18,0x0e,0x00,0xf7])

	def scrollText(self, color, loop, text):
		msg = [0xf0,0x00,0x20,0x29,0x02,0x18,0x14]
		msg = msg + [color,loop]+[ord(c) for c in text]+[0xf7]
		self.midi_output.write_sys_ex(0, msg)

def parseKeyEvent(keyNum, keydown):
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

def xyToKey(x,y):
	if(y==8):
		return x + 104
	else:
		return (x*10) + (y+1)
