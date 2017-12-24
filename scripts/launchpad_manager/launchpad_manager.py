#!/usr/bin/env python
import rospy
from launchpad_ctrl.msg import LaunchpadKey
from basic_mode import *
from car_base_mode import *


def callback(data):
  global modes, current_mode, current_mode_number
  if (data.x == 8 and data.y >= 4):
    mode_number = data.y - 4
    if (mode_number != current_mode_number and mode_number < len(modes)):
      current_mode.pause()
      current_mode = modes[mode_number]
      current_mode_number = mode_number
      current_mode.start()
  else:
    current_mode.execute(data)


def listener():
  global modes, current_mode, current_mode_number
  modes = [CarBaseMode(0), BasicMode(1), BasicMode(2), BasicMode(3)]
  current_mode = modes[0]
  current_mode_number = 0

  rospy.init_node('launchpad_manager', anonymous=True)

  rospy.Subscriber("launchpad_key_event", LaunchpadKey, callback)

  current_mode.start()

  # spin() simply keeps python from exiting until this node is stopped
  rospy.spin()


if __name__ == '__main__':
  listener()
