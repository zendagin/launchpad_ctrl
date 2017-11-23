#!/usr/bin/env python

def calWithAlpha(old, new, a):
	result = new * a + (1 - a) * old
	if(result > 1):
		result = 1
	return result

class Layer:
	def __init__(self, maxX, maxY):
		self.colors = [[0 for x in range(0,maxX)] for y in range(0,maxY)]
		for x in range(0,maxX):
			for y in range(0,maxY):
				self.colors[x][y] = (0.0, 0.0, 0.0, 0.0)#rgba 0 to 1

	def setColor(self,x,y,r,g,b,a = 1):
		self.colors[x][y] = (r,g,b,a)

	def getColor(self, x, y):
		return self.colors[x][y]


class Layers:
	def toActualValue(self, value):
		return int(round(value * self.maxValue))

	def printAll(self):
		xs = []
		ys = []
		rs = []
		gs = []
		bs = []
		for x in range(0,9):
			for y in range(0,9):
				(r,g,b)=self.colors[x][y]
				xs.append(x)
				ys.append(y)
				rs.append(r)
				gs.append(g)
				bs.append(b)

	def __init__(self, layerNumber, maxX, maxY, maxValue = 63):
		self.maxX = maxX
		self.maxY = maxY
		self.maxValue = maxValue
		self.layerNumber = layerNumber
		self.layers = []
		for l in range(0,layerNumber):
			self.layers.append(Layer(maxX,maxY))
		self.cache = [[0 for x in range(0,maxX)] for y in range(0,maxY)]
		for x in range(0,maxX):
			for y in range(0,maxY):
				self.cache[x][y] = (0, 0, 0)
		self.changed = False

	def addLayer(self):
		self.layerNumber += 1
		self.layers.append(Layer(self.x,self.y))

	def removeLayer(self):
		if(self.layerNumber > 0):
			self.layerNumber -= 1
			del self.layers[-1]
		else:
			print("Error: trying to remove layer from empty stack")

	def setColor(self, l, x, y, r, g, b, a = 1):
		if(self.layerNumber > l):
			self.layers[l].setColor(x, y, r, g, b, a)
			self.changed = True
		else:
			print("Error: out of bound, trying to access layer {} but there is only {}".format(l, layerNumber))

	def getColor(self, x, y):
		(r,g,b) = (0.0,0.0,0.0)
		for l in self.layers:
			(lr, lg, lb, la) = l.getColor(x,y)
			r = calWithAlpha(r, lr, la)
			g = calWithAlpha(g, lg, la)
			b = calWithAlpha(b, lb, la)
		return (self.toActualValue(r), self.toActualValue(g), self.toActualValue(b))
		
	def getAllColor(self):
		if(self.changed):
			for x in range(0,self.maxX):
				for y in range(0,self.maxY):
					self.cache[x][y] = self.getColor(x,y)
			self.changed = False
		return self.cache
		
