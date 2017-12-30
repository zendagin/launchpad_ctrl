from graphic.layers import *


class PidView(Layers):

  def __init__(self):
    super(PidView, self).__init__(1, 9, 9, False)
    self.values = []
    self.point = []
    for l in range(0, 8):
      self.values.append("")
      self.point.append(8)

  def setValue(self, num, value):
    self.point[num] = 8
    self.values[num] = value
    y = 0
    value = value[::-1]#reverse
    for i in range(0, 9):
      if i < len(value):
        d = value[i]
        if d == '.':
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
            '8': 118,
            '9': 3
          }[d]
          self.setColor(0, num, 7-y, c)
          y += 1
      else:
        self.setColor(0, num, 7-y, 0)
        y += 1

  def getFlash(self):
    flash = []
    for i in range(0, 8):
      if self.point[i] < 8:
        y = 8 - self.point[i]
        flash.append((i, y))
    return flash

