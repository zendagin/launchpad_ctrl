#!/usr/bin/env python

def calWithAlpha(old, new, a):
  result = new * a + (1 - a) * old
  if (result > 1):
    result = 1
  return result


class Layer(object):
  def __init__(self, maxX, maxY, rgb):
    self.colors = [[0 for x in range(0, maxX)] for y in range(0, maxY)]
    for x in range(0, maxX):
      for y in range(0, maxY):
        if rgb:
          self.colors[x][y] = (0.0, 0.0, 0.0, 0.0)  # rgba 0 to 1
        else:
          self.colors[x][y] = 0

  def setColorRGB(self, x, y, r, g, b, a=1):
    self.colors[x][y] = (r, g, b, a)

  def setColor(self, x, y, c):
    self.colors[x][y] = c

  def getColor(self, x, y):
    return self.colors[x][y]


class Layers(object):
  def toActualValue(self, value):
    return int(round(value * self.maxValue))

  def printChanged(self):
    changed = self.getChangedColor()
    xs = []
    ys = []
    rs = []
    gs = []
    bs = []
    cs = []
    for i in range(0, len(changed)):
      if self.rgb:
        (x,y,(r, g, b)) = changed[i]
        rs.append(r)
        gs.append(g)
        bs.append(b)
      else:
        (x,y,c) = changed[i]
        cs.append(c)
      xs.append(x)
      ys.append(y)
    if self.rgb:
      return (xs, ys, rs, gs, bs)
    else:
      return (xs, ys, cs)

  def printAll(self):
    c = self.getAllColor()
    xs = []
    ys = []
    rs = []
    gs = []
    bs = []
    cs = []
    for x in range(0, 9):
      for y in range(0, 9):
        xs.append(x)
        ys.append(y)
        if self.rgb:
          (r, g, b) = c[x][y]
          rs.append(r)
          gs.append(g)
          bs.append(b)
        else:
          cs.append(c[x][y])
    if self.rgb:
      return (xs, ys, rs, gs, bs)
    else:
      return (xs, ys, cs)


  def __init__(self, layerNumber, maxX, maxY, rgb=True, maxValue=63):
    self.maxX = maxX
    self.maxY = maxY
    self.maxValue = maxValue
    self.rgb = rgb
    self.layerNumber = layerNumber
    self.layers = []
    for l in range(0, layerNumber):
      self.layers.append(Layer(maxX, maxY, rgb))
    self.cache = [[0 for x in range(0, maxX)] for y in range(0, maxY)]
    for x in range(0, maxX):
      for y in range(0, maxY):
        if rgb:
          self.cache[x][y] = (0, 0, 0)
        else:
          self.cache[x][y] = 0
    self.changed = []

  def addLayer(self):
    self.layerNumber += 1
    self.layers.append(Layer(self.maxX, self.maxY, self.rgb))
    return self.layerNumber - 1

  def removeLayer(self):
    if (self.layerNumber > 0):
      self.layerNumber -= 1
      del self.layers[-1]
    else:
      print("Error: trying to remove layer from empty stack")
    return self.layerNumber

  def setColor(self, l, x, y, c):
    if (self.layerNumber > l):
      self.layers[l].setColor(x, y, c)
      self.changed.append((x, y))
    else:
      print("Error: out of bound, trying to access layer {} but there is only {}".format(l, self.layerNumber))

  def setColorRGB(self, l, x, y, r, g, b, a=1):
    if (self.layerNumber > l):
      self.layers[l].setColorRGB(x, y, r, g, b, a)
      self.changed.append((x, y))
    else:
      print("Error: out of bound, trying to access layer {} but there is only {}".format(l, self.layerNumber))

  def getColor(self, x, y):
    for l in reversed(self.layers):
      c = l.getColor(x, y)
      if c!= 0:
        return c
    return 0

  def getColorRGB(self, x, y):
    (r, g, b) = (0.0, 0.0, 0.0)
    for l in self.layers:
      (lr, lg, lb, la) = l.getColor(x, y)
      r = calWithAlpha(r, lr, la)
      g = calWithAlpha(g, lg, la)
      b = calWithAlpha(b, lb, la)
    return (self.toActualValue(r), self.toActualValue(g), self.toActualValue(b))

  def getChangedColor(self):
    return self.updateCache()

  def getAllColor(self):
    self.updateCache()
    return self.cache

  def updateCache(self):
    r = []
    for x, y in self.changed:
      if self.rgb:
        c = self.getColorRGB(x, y)
      else:
        c = self.getColor(x, y)
      self.cache[x][y] = c
      r.append((x, y, c))
    self.changed = []
    return r

  def getFlash(self):
    pass