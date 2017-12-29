#!/usr/bin/env python
import random
import rospy
from graphic.layers import *
from basic_mode import *
from std_msgs.msg import Empty
from launchpad_ctrl.msg import *
from geometry_msgs.msg import Pose2D
from std_msgs.msg import UInt8


class CarBaseMode(BasicMode):

  def __init__(self, modeNum):
    super(CarBaseMode, self).__init__(modeNum)

    self.moveMode = rospy.Publisher("command/move_mode", UInt8, queue_size=10)
    self.twistTarget = rospy.Publisher("command/twistTarget", Pose2D, queue_size=10)
    for x in range(1, 8):
      for y in range(0, 7):
        self.colors.setColorRGB(0, x, y, 0.1, 0.4, 0.1)
    self.setRowRGB(4, 0.4, 1, 0.4, 1, False)
    self.setColumnRGB(3, 0.4, 1, 0.4, 1, False)

    self.setColumnRGB(7, 0.6, 0.6, 0.8, 1, False)
    self.setRowRGB(0, 0.6, 0.6, 0.8, 1, False)
    self.setRowRGB(8, 0, 1, 0, 1, True)
    self.setColumnRGB(7, 0.6, 0.6, 0.8, 1, False)
    self.setColumnRGB(8, 0, 1, 0, 1, False)
    self.colors.setColorRGB(0, 8, modeNum + 4, 0, 1, 0.6)

    self.linear_velocity_const = 0.2
    self.angular_velocity_const = 0.2
    self.mode = UInt8(0)
    self.msg = Pose2D(0, 0, 0)
    self.x_total_velocity = 0.0
    self.y_total_velocity = 0.0
    self.totalKeyDown = 0
    self.theta = 0

  def start(self):
    self.printAll()
    self.sendStop()

  def pause(self):
    self.sendStop()

  def __exit__(self, exc_type, exc_value, traceback):
    self.sendStop()

  def sendStop(self):
    self.x_total_velocity = 0
    self.y_total_velocity = 0
    self.theta = 0
    del self.msg
    self.msg = Pose2D(0, 0, 0)
    self.moveMode.publish(self.mode)
    self.twistTarget.publish(self.msg)

  def sendMsg(self):
    if (self.totalKeyDown != 0):
      self.msg.x = self.x_total_velocity * self.linear_velocity_const / self.totalKeyDown
      self.msg.y = self.y_total_velocity * self.linear_velocity_const / self.totalKeyDown
    else:
      self.msg.x = 0
      self.msg.y = 0
    self.msg.theta = self.theta * self.angular_velocity_const
    print(self.msg.x, self.msg.y, self.msg.theta)
    self.moveMode.publish(self.mode)
    self.twistTarget.publish(self.msg)

  def execute(self, e):
    if (e.x != 8 and e.x != 0 and e.y <= 6):
      i = -1
      if (e.keydown):
        i = 1
        self.totalKeyDown += 1
      else:
        if (self.totalKeyDown != 0):
          self.totalKeyDown -= 1
      self.x_total_velocity += (e.x - 4) * i
      self.y_total_velocity += (e.y - 3) * i
      self.sendMsg()

    if (e.x == 8 and e.y == 2):
      if (e.keydown):
        self.theta -= 1
      else:
        self.theta += 1
      self.sendMsg()

    if (e.x == 8 and e.y == 3):
      if (e.keydown):
        self.theta += 1
      else:
        self.theta -= 1
      self.sendMsg()
