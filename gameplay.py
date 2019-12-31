

# from app import scoresWindow

import pygame, sys

from layout import Button, Menu
from objects import *
from window import BaseWindow, Window
from handleScore import getScore

pygame.init()
pygame.mixer.init()



def allowedEvent():
    pygame.event.set_blocked(pygame.ACTIVEEVENT)
    # pygame.event.set_blocked(pygame.KEYDOWN)
    pygame.event.set_blocked(pygame.KEYUP)
    # pygame.event.set_blocked(pygame.MOUSEMOTION)
    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
    # pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
    pygame.event.set_blocked(pygame.JOYAXISMOTION)
    pygame.event.set_blocked(pygame.JOYBALLMOTION)
    pygame.event.set_blocked(pygame.JOYHATMOTION)
    pygame.event.set_blocked(pygame.JOYBUTTONUP)
    pygame.event.set_blocked(pygame.JOYBUTTONDOWN)
    pygame.event.set_blocked(pygame.VIDEORESIZE)
    pygame.event.set_blocked(pygame.VIDEOEXPOSE)
    pygame.event.set_blocked(pygame.USEREVENT)

    # pygame.event.set_blocked(3)




def printText(surf,pos,text):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render(str(text), True, (10,10,10))
    surf.blit(text,pos)




def changetoMainMenu():
	Window.setWindowName("MainMenu")

class GamePlay(BaseWindow):
	def __init__(self):
		super().__init__()
		self.size = (w,h) = (400,600)
		self.bg = pygame.Surface((w,h))
		self.bg.fill((200,250,150))
		self.clock = pygame.time.Clock()
		self.highScore = getScore()[0]["score"]
		self.fps = 15
		self.enemy_count = 20

		self._objects = [Player()]
		player = self._objects[0]

		for i in range(self.enemy_count):
			self._objects.append(Enemy())

		self.pauseButton = Button((w//2+160-80,550),(80,40), "Pause",player.stop)
		self.mainMenuButton = Button((w//2-160,550),(80,40), "Menu",changetoMainMenu)
		self.pause_menu = Menu((w//2-40,h//2-(20)*2),(80,40),["Resume","Menu"],[player.resume,changetoMainMenu])
		self.restart_menu = Menu((w//2-40,h//2-(20)*2),(80,40),["restart","Menu"],[player.restart,changetoMainMenu])
		self.music = pygame.mixer.Sound('sounds/TS - Beat Y.ogg')
		self.music.play(loops=-1, maxtime=0, fade_ms=1000)


		allowedEvent()
	def __del__(self):
		self.music.stop()

	def quit(self):
		pygame.quit()
		sys.exit()

	def checkEvents(self,ev):
		if ev.type == pygame.QUIT:
			quit()
		if ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_ESCAPE:
				# running = False
				quit()

		for o in self._objects:
			o.checkEvents(ev)

		self.pauseButton.checkEvents()
		self.mainMenuButton.checkEvents()

		# snake = self._objects[0]
		# if snake.isstop and not snake.isdead:
		# 	self.pause_menu.checkEvents()
		# elif snake.isdead:
		# 	self.restart_menu.checkEvents()
		# else :
		# 	pygame.mixer.unpause()

		

	def update(self):

		for i in range(self.enemy_count):
			enemy = self._objects[i+1]
			if enemy.exceeds_boundary():
				self._objects.remove(enemy)
				self._objects.append(Enemy())

		player = self._objects[0]
		player.update()

		for o in self._objects:
			o.update()

	def draw(self,surf):
		w,h = self.size
		snake = self._objects[0]
		surf.blit(self.bg,(0,0))

		for o in self._objects:
			o.draw(surf)

		# pygame.draw.rect(surf,(180,230,120),pygame.Rect((0,498), (400,600-498)))
		# pygame.draw.line(surf,(50,50,50),(0,498),(400,498),1)

		self.pauseButton.draw(surf)
		self.mainMenuButton.draw(surf)

		# if snake.isstop and not snake.isdead:
		# 	color = pygame.Color(80, 30, 150, a=10)
		# 	color.a=0
		# 	# pygame.draw.rect(surf,color,pygame.Rect((w//2-140,h//2-(50)*2), (400,600-498)))
		# 	self.pause_menu.draw(surf)
		# elif snake.isdead:
		# 	self.restart_menu.draw(surf)

		# printText(surf,(0,0),"SCORE: {}".format(snake.score))
		printText(surf,(250,0),"HIGHSCORE: {}".format(self.highScore))

