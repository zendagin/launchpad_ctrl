#!/usr/bin/env python
import random
import rospy
import os.path
from graphic.layers import *
from basic_mode import *
from std_msgs.msg import Empty
from launchpad_ctrl.msg import *
from pid.view import  *
from pid.edit import  *


class PIDMode(BasicMode):

  def __init__(self, modeNum):
    super(PIDMode, self).__init__(modeNum)

    self.rgb = False
    self.view = PidView()
    self.edit = PidEdit()
    self.editMode = False
    self.colors = self.view
    if os.path.isfile("saved_values.txt"):
      with open("saved_values.txt") as f:
        content = f.readlines()
        f.close()
      for (i, line) in enumerate(content):
        line = line[:len(line) - 1]#remove \n
        self.view.setValue(7-i, line)
    self.view.setValue(0, "0123456789")

    for x in range(0, 3):
      for y in range(0, 3):
        self.edit.setColor(0, x, 4+y, 114)
    self.edit.setColor(0, 0, 7, 114)
    self.edit.setColor(0, 1, 7, 122)
    self.edit.setColor(0, 2, 7, 5)
    self.edit.setColor(0, 0, 8, 3)

  def start(self):
    self.printAll()

  def sendFlash(self):
    if self.editMode == False:
      rospy.sleep(0.1)
      flashs = self.view.getFlash()
      for (x, y) in flashs:
        self.flash.publish(LaunchpadFlash(x, y, 23))

  def updateColor(self):
    self.colors.render()
    super(PIDMode, self).updateColor()
    self.sendFlash()

  def printAll(self):
    self.colors.render()
    super(PIDMode, self).printAll()
    self.sendFlash()

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def execute(self, e):
    if e.keydown == False:
      return
    if self.editMode == False and e.y == 8 and e.x != 0:
      self.editMode = True
      self.editingNum = e.x
      self.edit.setValue(self.view.values[e.x])
      self.colors = self.edit
      self.edit.render()
      self.printAll()
    if self.editMode == True:
      if e.x == 0 and e.y == 8:
        self.editMode = False
        str = self.edit.value
        if str[len(str)-1] == '.':
          str = str[:len(str)-1]
        self.edit.setValue(str)
        self.view.setValue(self.editingNum, str)
        with open("saved_values.txt", "w") as f:
          for i in range(0, 7):
            f.write(self.view.values[7-i]+"\n")
          f.close()
        self.colors = self.view
        self.printAll()
      if e.y == 7:
        if e.x == 0:
          self.edit.addDigit('0')
        if e.x == 1 and "." not in self.edit.value:
          self.edit.addDigit('.')
        if e.x == 2:
          self.edit.pop()
      if(e.y >= 4 and e.y < 7) and (e.x < 3):
        n = (6-e.y)*3+e.x
        self.edit.addDigit(chr(ord('1')+n))
      self.updateColor()
    if e.x == 8and e.y < 4:
      if e.type == "UP":
        self.colors.shiftTop()
      if e.type == "DOWN":
        self.colors.shiftBottom()
      if e.type == "LEFT":
        self.colors.shiftLeft()
      if e.type == "RIGHT":
        self.colors.shiftRight()
      self.updateColor()


