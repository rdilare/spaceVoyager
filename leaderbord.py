import pygame, sys

import handleScore


from window import BaseWindow, Window
# from mainMenu import MainMenu
from layout import Button

pygame.init()


def changetoMainMenu():
	Window.setWindowName("MainMenu")


class LeaderBoard(BaseWindow):
	def __init__(self):
		super().__init__()

		self.data = handleScore.getScore()

		self.size = (w,h) = (400,600)
		self.bg = self.getScoreSurface()
		self.clock = pygame.time.Clock()

		self.backButton = Button((w//2+160-80,500),(80,40), "Back", action=changetoMainMenu)


	def getScoreSurface(self):
		font = pygame.font.SysFont("comicsansms", 25)

		surf = pygame.Surface((400,600))
		surf.fill((100,50,190))


		sr_title = font.render("Sr.", True, (0,0,0))
		date_title = font.render("DATE", True, (0,0,0))
		score_title = font.render("SCORE", True, (0,0,0))

		surf.blit(sr_title,(50,200))
		surf.blit(date_title,(90,200))
		surf.blit(score_title,(260,200))

		j=1
		for i in self.data:
			sr = font.render(str(j)+".", True, (255,255,0))
			date = font.render(str(i["date"]), True, (255,255,0))
			score = font.render(str(i["score"]), True, (255,255,0))

			surf.blit(sr,(50,200+j*20))
			surf.blit(date,(90,200+j*20))
			surf.blit(score,(260,200+j*20))
			j+=1

		return surf

	def checkEvents(self,ev):
		self.backButton.checkEvents()

	def draw(self,surf):

		surf.blit(self.bg,(0,0))
		self.backButton.draw(surf)


