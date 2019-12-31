

class BaseWindow:
	fps = 5
	def checkEvents(self,ev):
		pass

	def draw(self):
		pass

	def update(self):
		pass

class Window:
	current = BaseWindow()
	name="BaseWindow"

	@classmethod
	def setWindow(cls,a):
		cls.current = a

	@classmethod
	def setWindowName(cls,name):
		cls.name = name

