from importlib import import_module
class NodeGroup(object):
  def __init__(self, coordinates, layerNumber, name = None, activeColor = 16, inactiveColor = 23, colorLayer = None , active = False, keyDown = None, keyUp = None):
    self.coordinates = coordinates
    self.layerNumber = layerNumber
    self.name = name
    self.activeColor = activeColor
    self.inactiveColor = inactiveColor
    self.active = active
    if colorLayer != None:
        self.setColorLayer(colorLayer)
    #keyDown and keyUp are string to the method, for example package.file.class.method
    if keyDown != None:
      self.keyDown = loadMethod(keyDown)
    if keyUp != None:
      self.keyUp = loadMethod(keyUp)

  def setColorLayer(self, layer):
    self.colorLayer = layer
    for (x, y) in self.coordinates:
        self.colorLayer.setColor(x,y,self.inactiveColor)

  def updateColor(self):
    if self.colorLayer != None:
      if self.active:
          self.color = self.activeColor
      else:
          self.color = self.inactiveColor

      for (x, y) in self.coordinates:
          self.colorLayer.setColor(x,y,self.color)



  def contains(self, x, y):
    for (X, Y) in self.coordinates:
        if(x == X) & (y == Y):
            return True
    return False

def loadMethod(path):
  p, m = path.rsplit('.', 1)

  mod = import_module(p)
  return getattr(mod, m)
