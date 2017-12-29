#!/usr/bin/env python
import rospy
from std_msgs.msg import Empty, UInt8
from launchpad_ctrl.msg import *

import pygame.event
import pygame.midi
import random

import sys
import select
from launchpad import *


def colorOne(m):
  key = xyToKey(m.x, m.y)
  lp.lightOne(key, m.c)

def color(m):
  for index, data in enumerate(m.x):
    c = LaunchpadColorOne(m.x[index], m.y[index], m.c[index])
    colorOne(c)

def colorRow(m):
  lp.lightOne(m.row, m.c)

def colorColumn(m):
  lp.lightColumn(m.column, m.c)

def colorAll(m):
  lp.lightAll(m.data)#TODO

def flash(m):
  key = xyToKey(m.x, m.y)
  lp.flash(key, m.c)

def colorOneRGB(m):
  key = xyToKey(m.x, m.y)
  lp.lightOneRGB(key, m.r, m.g, m.b)

def colorRGB(m):
  for index, data in enumerate(m.x):
    c = LaunchpadColorOneRGB(m.x[index], m.y[index], m.r[index], m.g[index], m.b[index])
    colorOneRGB(c)

def clear(m):
  lp.ledOff()


def main():
  pygame.init()
  rospy.init_node('launchpad', anonymous=True)
  pub = rospy.Publisher("launchpad_key_event", LaunchpadKey, queue_size=10)
  rospy.Subscriber("launchpad_color_change_one", LaunchpadColorOne, colorOne)
  rospy.Subscriber("launchpad_color_change", LaunchpadColor, color)

  rospy.Subscriber("launchpad_color_row", LaunchpadRow, colorRow)
  rospy.Subscriber("launchpad_color_column", LaunchpadColumn, colorColumn)
  rospy.Subscriber("launchpad_color_all", UInt8, colorAll)
  rospy.Subscriber("launchpad_color_flash", LaunchpadFlash, flash)

  rospy.Subscriber("launchpad_color_change_one_rgb", LaunchpadColorOneRGB, colorOneRGB)
  rospy.Subscriber("launchpad_color_change_rgb", LaunchpadColorRGB, colorRGB)
  rospy.Subscriber("launchpad_clear", Empty, clear)

  global lp
  lp = Launchpad()
  midi_input = lp.midi_input
  midi_output = lp.midi_output

  lp.presetMode(0);
  while not rospy.is_shutdown():
    # break when keyboard 'enter' pressed
    i, o, e = select.select([sys.stdin], [], [], 0)
    out = False
    for s in i:
      if s == sys.stdin:
        input = sys.stdin.readline()
        out = True
    if (out):
      break
    # read launchpad input
    if not midi_input.poll():
      continue

    msg, timestamp = midi_input.read(1)[0]
    # midi_output.note_on(msg[1],(msg[1]/10-1)*8+(msg[1]%10-1)+64)
    # midi_output.write_short(0x90,msg[1],r)
    # lp.lightOne(msg[1],0,50,0)
    e = parseKeyEvent(msg[1], msg[2])
    print("%s" % msg)
    pub.publish(parseKeyEvent(msg[1], msg[2]))

  # for i in range(64):
  #	midi_output.write_short(0x90,(i%8)+11+10*(i/8),i)
  #	midi_output.write_short(0x91,(i%8)+11+10*(i/8),i+64)

  # print Bye Bye
  lp.scrollText(0x4b, False, "Bye Bye")

  while not midi_input.poll():
    continue
  lp.disconnect()


if __name__ == "__main__":
  main()
