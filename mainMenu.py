
import pygame, sys

from layout import Menu
from window import Window
from window import BaseWindow

pygame.init()


def quit():
	pygame.quit()
	sys.exit()

def changetoPlay():
	Window.setWindowName("GamePlay")

def changetoScores():
	Window.setWindowName("LeaderBoard")


class MainMenu(BaseWindow):
	def __init__(self):
		super().__init__()
		self.size = (w,h) = (400,600)
		self.bg = pygame.Surface((w,h))
		self.bg.fill((0,150,100))
		self.menu = Menu((w//2-40,h//2-(20)*4),(80,40),["Play","Scores","Quit"],[changetoPlay,changetoScores,quit])
		self.clock = pygame.time.Clock()

	def checkEvents(self,ev):
		if ev.type == pygame.QUIT:
			quit()
		if ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_ESCAPE:
				# running = False
				quit()

		self.menu.checkEvents()

	def draw(self,surf):
		surf.blit(self.bg,(0,0))
		self.menu.draw(surf)




