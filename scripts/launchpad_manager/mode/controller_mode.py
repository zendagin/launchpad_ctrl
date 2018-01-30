#!/usr/bin/env python
import random
import rospy
import os.path
from graphic.layers import *
from basic_mode import *
from std_msgs.msg import Empty
from launchpad_ctrl.msg import *
from ui_element.node_group import  *
import pickle
import os.path

class ControllerMode(BasicMode):

  def __init__(self, modeNum):
    super(ControllerMode, self).__init__(modeNum)
    self.rgb = False
    if os.path.isfile('ui_groups.pkl'):
      self.loadGroups()
    else:
      self.nodeGroups = []
      self.addGroup(NodeGroup(
        [(7,0),(6,0)],
        1,
        name="Loading",
        colorLayer= self.colors.layers[self.colors.addLayer()],
        keyDown="controller.methods.test"
      ))
      self.addGroup(NodeGroup(
        [(5,0)],
        2,
        name="Start Zone",
        colorLayer= self.colors.layers[self.colors.addLayer()],
        keyDown="controller.methods.test"
      ))
      self.addGroup(NodeGroup(
        [(4,0),(4,1)],
        3,
        colorLayer= self.colors.layers[self.colors.addLayer()],
        keyDown="controller.methods.test"
      ))
      self.addGroup(NodeGroup(
        [(3,0),(3, 1)],
        4,
        colorLayer= self.colors.layers[self.colors.addLayer()],
        keyDown="controller.methods.test"
      ))
      self.addGroup(NodeGroup(
        [(2,0),(2, 1)],
        5,
        colorLayer= self.colors.layers[self.colors.addLayer()],
        keyDown="controller.methods.test"
      ))
      self.addGroup(NodeGroup(
        [(1,0),(1, 1)],
        6,
        colorLayer= self.colors.layers[self.colors.addLayer()],
        keyDown="controller.methods.test"
      ))



  def addGroup(self, group):
      self.nodeGroups.append(group)
      self.nodeGroups.sort(key=lambda x: x.layerNumber, reverse=True)
      self.saveGroups()

  def saveGroups(self):
      with open('ui_groups.pkl', 'wb') as output:
          pickle.dump(self.nodeGroups, output, pickle.HIGHEST_PROTOCOL)

  def loadGroups(self):
      with open('ui_groups.pkl', 'rb') as input:
          self.nodeGroups = pickle.load(input)

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
    super(ControllerMode, self).updateColor()
    self.sendFlash()

  def printAll(self):
    self.colors.render()
    super(ControllerMode, self).printAll()
    self.sendFlash()

  def __exit__(self, exc_type, exc_value, traceback):
    pass

  def execute(self, e):
      for group in self.nodeGroups:
          if group.contains(e.x, e.y):
            if e.keydown:
              group.keyDown(self.nodeGroups)
            else:
              group.keyUp(self.nodeGroups)
            self.updateColor()
            break



