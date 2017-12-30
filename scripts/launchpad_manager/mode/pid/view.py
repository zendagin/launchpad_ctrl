from graphic.layers import *


class PidView(Layers):

  def __init__(self):
    super(PidView, self).__init__(1, 9, 9, False)
    self.values = []
    self.point = []
    self.shift = 0
    for l in range(0, 8):
      self.values.append("")
      self.point.append(8)

  def setValue(self, num, value):
    self.values[num] = value

  def render(self):
    for (num, value) in enumerate(self.values):
      self.point[num] = 8
      y = 0
      value = value[::-1]#reverse
      for i in range(self.shift, 9 + self.shift):
        if y >= 8:
          break
        if i < len(value):
          d = value[i]
          if d == '.':
            if y != 0:
              self.point[num] = y
          else:
            c = {
              '0': 0,
              '1': 62,
              '2': 4,
              '3': 9,
              '4': 73,
              '5': 17,
              '6': 49,
              '7': 54,
              '8': 117,
              '9': 3
            }[d]
            if self.getColor(num, 7-y) != c:
              self.setColor(0, num, 7-y, c)
            y += 1
        else:
          if self.getColor(num, 7-y) != 0:
            self.setColor(0, num, 7-y, 0)
          y += 1

  def getFlash(self):
    flash = []
    for i in range(0, 8):
      if self.point[i] < 8:
        y = 8 - self.point[i]
        flash.append((i, y))
    return flash

  def shiftTop(self):
    self.shift = max(self.maxLength()-8, 0)

  def shiftBottom(self):
    self.shift = 0

  def shiftRight(self):
    self.shift = max(self.shift - 1, 0)

  def shiftLeft(self):
    self.shift += 1
    self.adjustShift()

  def adjustShift(self):
    self.shift = min(self.shift, self.maxLength())

  def maxLength(self):
    maxL = 0
    for str in self.values:
      l = len(str)
      if "." in str:
        l -= 1
      maxL = max(maxL, l)
    return maxL

