from graphic.layers import *


class PidEdit(Layers):

  def __init__(self, str = "", c = 17):
    super(PidEdit, self).__init__(1, 9, 9, False)
    self.value = ""
    self.pixels = [[0 for x in range(0, 5)]]
    self.shift = 0
    self.shiftPixel = 0
    self.c = c
    if str != "":
      self.setValue(str)

  def setValue(self, value):
    self.pixels = [[0 for x in range(0, 5)]]
    for d in value:
      self.addDigit(d)
    self.value = value

  def addDigit(self, d):
    self.shift = 0
    self.shiftPixel = 0
    if len(self.pixels) != 0:
      self.pixels.append([0, 0, 0, 0, 0])
    if d == '.':
      self.pixels.append([0, 0, 0, 0, 1])
    if d == '0':
      self.pixels.append([0, 1, 1, 1, 0])
      self.pixels.append([1, 0, 0, 0, 1])
      self.pixels.append([1, 0, 0, 0, 1])
      self.pixels.append([0, 1, 1, 1, 0])
    if d == '1':
      self.pixels.append([1, 0, 0, 0, 1])
      self.pixels.append([1, 1, 1, 1, 1])
      self.pixels.append([0, 0, 0, 0, 1])
    if d == '2':
      self.pixels.append([1, 0, 0, 1, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([0, 1, 0, 0, 1])
    if d == '3':
      self.pixels.append([1, 0, 0, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([0, 1, 0, 1, 0])
    if d == '4':
      self.pixels.append([1, 1, 1, 1, 0])
      self.pixels.append([0, 0, 0, 1, 0])
      self.pixels.append([1, 1, 1, 1, 1])
      self.pixels.append([0, 0, 0, 1, 0])
    if d == '5':
      self.pixels.append([1, 1, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 0, 1, 0])
    if d == '6':
      self.pixels.append([0, 1, 1, 1, 0])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([0, 0, 0, 1, 0])
    if d == '7':
      self.pixels.append([1, 0, 0, 0, 0])
      self.pixels.append([1, 0, 0, 1, 1])
      self.pixels.append([1, 0, 1, 0, 0])
      self.pixels.append([1, 1, 0, 0, 0])
    if d == '8':
      self.pixels.append([0, 1, 0, 1, 0])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([0, 1, 0, 1, 0])
    if d == '9':
      self.pixels.append([0, 1, 0, 0, 0])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([1, 0, 1, 0, 1])
      self.pixels.append([0, 1, 1, 1, 0])
    self.value = self.value + d

  def render(self):
      for y in range(0, 8):
        pos = len(self.pixels) - self.shiftPixel + y - 7 - 1
        if len(self.pixels) > pos and pos >= 0:
          refrence = self.pixels[pos]
        else:
          refrence = [0, 0, 0, 0, 0]
        for x in range(0, 5):
          c = self.c * refrence[x]
          if self.getColor(7-x,y) != c:
            self.setColor(0, 7-x, y, c)

  def shiftLeft(self, offset = 1):
    for i in range(0, offset):
      if len(self.pixels) - self.shiftPixel > 8:
        widthDict = {
          '.': 3,
          '1': 5
        }
        pos = len(self.value) - self.shift
        width = widthDict.get(self.value[pos], 6)
        self.shiftPixel += width
        self.shift += 1
      else:
        break

  def shiftRight(self, offset = 1):
    for i in range(0, offset):
      if self.shift > 0:
        self.shift -= 1
        widthDict = {
          '.': 3,
          '1': 5
        }
        pos = len(self.value) - self.shift
        width = widthDict.get(self.value[pos], 6)
        self.shiftPixel -= width
      else:
        break

  def pop(self):
    l = len(self.value)
    if l != 0:
      self.shift = 0
      self.shiftPixel = 0
      self.setValue(self.value[:l-1])