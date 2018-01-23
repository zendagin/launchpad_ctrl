#!/usr/bin/env python
import random
import rospy
from std_msgs.msg import Empty, UInt8
from launchpad_ctrl.msg import *
from graphic.layers import *

import sys


class BasicMode(object):
  def setSingleColorRGB(self, x, y, r, g, b):
    if (x < 0 or y < 0 or x > 9 or y > 9 or (x == 8 and y > 3)):
      return -1
    self.colors.setColorRGB(0, x, y, r, g, b)
    return 0

  def setAndChangeSingleColorRGB(self, x, y, r, g, b):
    if (x < 0 or y < 0 or x > 9 or y > 9 or (x == 8 and y > 3)):
      return -1
    self.colors.setColorRGB(0, x, y, r, g, b)
    (r, g, b) = self.colors.getColorRGB(x, y)
    self.changeColorOneRGB.publish(LaunchpadColorOneRGB(x, y, r, g, b))
    return 0

  def setColumnRGB(self, y, r, g, b, a, includeFunction, layer=0):
    maxX = 9
    if (includeFunction == False):
      maxX = 8
    for x in range(0, maxX):
      self.colors.setColorRGB(layer, x, y, r, g, b, a)

  def setRowRGB(self, x, r, g, b, a, includeFunction, layer=0):
    maxY = 9
    if (includeFunction == False):
      maxY = 8
    for y in range(0, maxY):
      self.colors.setColorRGB(layer, x, y, r, g, b, a)

  def addL(self):
    self.colors.addLayer()

  def printAll(self):
    if self.colors.rgb:
      (xs, ys, rs, gs, bs) = self.colors.printAll()
      self.changeColorRGB.publish(LaunchpadColorRGB(xs, ys, rs, gs, bs))
    else:
      (xs, ys, cs) = self.colors.printAll()
      self.changeColor.publish(LaunchpadColor(xs, ys, cs))

  def updateColor(self):
    if self.colors.rgb:
      (xs, ys, rs, gs, bs) = self.colors.printChanged()
      self.changeColorRGB.publish(LaunchpadColorRGB(xs, ys, rs, gs, bs))
    else:
      (xs, ys, cs) = self.colors.printChanged()
      self.changeColor.publish(LaunchpadColor(xs, ys, cs))

  def __init__(self, modeNum):
    self.modeNum = modeNum
    self.clear = rospy.Publisher("launchpad_clear", Empty, queue_size=10)
    self.changeColor = rospy.Publisher("launchpad_color_change", LaunchpadColor, queue_size=10)
    self.changeColorOne = rospy.Publisher("launchpad_color_change_one", LaunchpadColorOne, queue_size=10)
    self.changeRow = rospy.Publisher("launchpad_color_row", LaunchpadRow, queue_size=10)
    self.changeColumn = rospy.Publisher("launchpad_color_column", LaunchpadColumn, queue_size=10)
    self.changeAll = rospy.Publisher("launchpad_color_all", UInt8, queue_size=10)
    self.flash = rospy.Publisher("launchpad_color_flash", LaunchpadFlash, queue_size=10)
    self.changeColorRGB = rospy.Publisher("launchpad_color_change_rgb", LaunchpadColorRGB, queue_size=10)
    self.changeColorOneRGB = rospy.Publisher("launchpad_color_change_one_rgb", LaunchpadColorOneRGB, queue_size=10)

    self.colors = Layers(1, 9, 9, 63)
    for x in range(0, 9):
      for y in range(0, 9):
        self.colors.setColorRGB(0, x, y, 0, 1, 0)
    self.colors.setColorRGB(0, 8, modeNum + 4, 0, 1, 0.6)

    self.addL()

  def start(self):
    #self.printAll()
    pass

  def pause(self):
    pass

  def execute(self, e):
    r = random.random()
    print(e.x, e.y)
    self.setAndChangeSingleColorRGB(e.x, e.y, r, 1, r)
    self.setAndChangeSingleColorRGB(e.x + 1, e.y, r, 1, r)
    self.setAndChangeSingleColorRGB(e.x - 1, e.y, r, 1, r)
