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
    reversed(value)
    for y in range(0, 8):
      if y < len(value):
        d = value[y]
        if d == '.':
          self.point[num] = y + 1
        else:
          c = {
            '0': 0,
            '1': 10,
            '2': 4,
            '3': 9,
            '4': 12,
            '5': 17,
            '6': 49,
            '7': 54,
            '8': 118,
            '9': 3
          }[d]
          self.setColor(0, num, 7-y, c)
      else:
        self.setColor(0, num, 7-y, 0)

