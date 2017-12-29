#!/usr/bin/env python
import random
import rospy
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

    for x in range(0, 3):
      for y in range(0, 3):
        self.edit.setColor(0, x, 4+y, 114)
    self.edit.setColor(0, 0, 7, 114)
    self.edit.setColor(0, 1, 7, 122)
    self.edit.setColor(0, 2, 7, 5)
    self.edit.setColor(0, 0, 8, 3)

  def start(self):
    self.printAll()

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def execute(self, e):
    if e.keydown == False:
      return
    if self.editMode == False and e.y == 8 and e.x != 8:
      self.editMode = True
      self.editingNum = e.x
      self.edit.setValue(self.view.values[e.x])
      self.colors = self.edit
      self.edit.render()
      self.printAll()
    if self.editMode == True:
      if e.x == 0 and e.y == 8:
        self.editMode = False
        self.view.setValue(self.editingNum, self.edit.value)
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
      self.edit.render()
      self.updateColor()


