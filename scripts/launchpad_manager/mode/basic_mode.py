#!/usr/bin/env python
import random
import rospy
from std_msgs.msg import Empty
from launchpad_ctrl.msg import *
from graphic.layers import *

import sys


class BasicMode(object):
  def setSingleColor(self, x, y, r, g, b):
    if (x < 0 or y < 0 or x > 9 or y > 9 or (x == 8 and y > 3)):
      return -1
    self.colors.setColor(0, x, y, r, g, b)
    return 0

  def setAndChangeSingleColor(self, x, y, r, g, b):
    if (x < 0 or y < 0 or x > 9 or y > 9 or (x == 8 and y > 3)):
      return -1
    self.colors.setColor(0, x, y, r, g, b)
    (r, g, b) = self.colors.getColor(x, y)
    self.changeColorOne.publish(LaunchpadColorOne(x, y, r, g, b))
    return 0

  def setColumn(self, y, r, g, b, a, includeFunction, layer=0):
    maxX = 9;
    if (includeFunction == False):
      maxX = 8;
    for x in range(0, maxX):
      self.colors.setColor(layer, x, y, r, g, b, a)

  def setRow(self, x, r, g, b, a, includeFunction, layer=0):
    maxY = 9;
    if (includeFunction == False):
      maxY = 8;
    for y in range(0, maxY):
      self.colors.setColor(layer, x, y, r, g, b, a)

  def addL(self):
    self.colors.addLayer()
    self.setRow(4, 0, 0, 1, 0.5, False, 1)

  def printAll(self):
    xs = []
    ys = []
    rs = []
    gs = []
    bs = []
    colors = self.colors.getAllColor()
    for x in range(0, 9):
      for y in range(0, 9):
        (r, g, b) = colors[x][y]
        xs.append(x)
        ys.append(y)
        rs.append(r)
        gs.append(g)
        bs.append(b)
        sys.stdout.write(" {} {} {} ".format(r, g, b))
      print('\n')
    self.changeColor.publish(LaunchpadColor(xs, ys, rs, gs, bs))

  def __init__(self, modeNum):
    self.modeNum = modeNum
    self.clear = rospy.Publisher("launchpad_clear", Empty, queue_size=10)
    self.changeColor = rospy.Publisher("launchpad_color_change", LaunchpadColor, queue_size=10)
    self.changeColorOne = rospy.Publisher("launchpad_color_change_one", LaunchpadColorOne, queue_size=10)
    self.colors = Layers(1, 9, 9, 63)
    for x in range(0, 9):
      for y in range(0, 9):
        self.colors.setColor(0, x, y, 0, 1, 0)
    self.colors.setColor(0, 8, modeNum + 4, 0, 1, 0.6)

    self.addL()

  def start(self):
    self.printAll()

  def pause(self):
    pass

  def execute(self, e):
    r = random.random()
    print(e.x, e.y)
    self.setAndChangeSingleColor(e.x, e.y, r, 1, r)
    self.setAndChangeSingleColor(e.x + 1, e.y, r, 1, r)
    self.setAndChangeSingleColor(e.x - 1, e.y, r, 1, r)
