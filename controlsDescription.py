import pygame

from window import BaseWindow, Window
from layout import Button

pygame.init()



def changetoMainMenu():
	Window.setWindowName("MainMenu")


class ControlsDescription(BaseWindow):
	def __init__(self):
		super().__init__()

		self.size = (w,h) = (400,600)
		self.bg = self.getTextSurface()
		self.clock = pygame.time.Clock()

		self.backButton = Button((w//2+160-80,500),(80,40), "Back", action=changetoMainMenu)


	def getTextSurface(self):
		font = pygame.font.SysFont("comicsansms", 25)

		surf = pygame.Surface((400,600))
		surf.fill((0,150,100))


		left = font.render("a : LEFT", True, (255,255,0))
		right = font.render("d : RIGHT", True, (255,255,0))
		up = font.render("w : UP", True, (255,255,0))
		down = font.render("s : DOWN", True, (255,255,0))
		fire = font.render("space : FIRE", True, (255,255,0))
		aim = font.render("mouse : AIM", True, (255,255,0))

		surf.blit(left,(150,200))
		surf.blit(right,(150,220))
		surf.blit(up,(150,240))
		surf.blit(down,(150,260))
		surf.blit(fire,(150,280))
		surf.blit(aim,(150,300))


		return surf

	def checkEvents(self,ev):
		self.backButton.checkEvents()

	def draw(self,surf):

		surf.blit(self.bg,(0,0))
		self.backButton.draw(surf)


