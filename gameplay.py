

# from app import scoresWindow

import pygame, sys

from layout import Button, Menu
from handleScore import getScore, saveScore
from objects import *
from window import BaseWindow, Window

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
		self.score = 0
		self.fps = 15
		self.enemy_count = 15
		self.paused = False
		self.debries = []
		self.player_alive = True

		self._objects = [Player()]
		player = self._objects[0]

		for i in range(self.enemy_count):
			self._objects.append(Enemy())

		self.pauseButton = Button((w//2+160-80,550),(80,40), "Pause",self.stop)
		self.mainMenuButton = Button((w//2-160,550),(80,40), "Menu",changetoMainMenu)
		self.pause_menu = Menu((w//2-40,h//2-(20)*2),(80,40),["Resume","Menu"],[self.resume,changetoMainMenu])
		self.restart_menu = Menu((w//2-40,h//2-(20)*2),(80,40),["restart","Menu"],[self.restart,changetoMainMenu])


		allowedEvent()

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



		if self.paused and self.player_alive:
			self.pause_menu.checkEvents()
		elif not self.player_alive:
			self.restart_menu.checkEvents()
		

	def update(self):

		i = 0
		while i!=self.enemy_count:
			enemy = self._objects[i+1]
			player = self._objects[0]
			if enemy.exceeds_boundary():
				self._objects.remove(enemy)
				self._objects.append(Enemy())
			elif player.hit(enemy):
				enemy.damage()
				if enemy.get_life()==0: 			# checking if enemy dies
					for i in range(20):
						self.debries.append(Enemy(enemy.get_pos(),4,color=(200,100,50)))
					self._objects.remove(enemy)
					self._objects.append(Enemy())
					self.score+=1
					player.increaseScore(1)
					break;
				i+=1
			else:
				i+=1



		i=0
		while i!=len(self.debries):
			deb = self.debries[i]
			if deb.exceeds_boundary():
				self.debries.remove(deb)
			else:
				i+=1


		player = self._objects[0]
		player.update()

#-----------------------------------checking playes's collision with enemies and boundaries-----------------------

		if player.isCollide(self._objects[1:]) or player.exceeds_boundary():
			self.player_alive = False
			self.stop()

		for o in self._objects:
			o.update()
		for deb in self.debries:
			deb.update()



	def draw(self,surf):
		w,h = self.size
		snake = self._objects[0]
		surf.blit(self.bg,(0,0))

		for o in self._objects:
			o.draw(surf)

		for deb in self.debries:
			deb.draw(surf)

		# pygame.draw.rect(surf,(180,230,120),pygame.Rect((0,498), (400,600-498)))
		# pygame.draw.line(surf,(50,50,50),(0,498),(400,498),1)

		self.pauseButton.draw(surf)
		self.mainMenuButton.draw(surf)



		if self.paused and self.player_alive:
			self.pause_menu.draw(surf)
		elif not self.player_alive:
			self.restart_menu.draw(surf)


		printText(surf,(0,0),"SCORE: {}".format(self.score))
		printText(surf,(250,0),"HIGHSCORE: {}".format(self.highScore))



	def resume(self):
		self.paused = False

		for o in self._objects:
			o.resume()

		for deb in self.debries:
			deb.resume()

	def stop(self):
		self.paused = True

		for o in self._objects:
			o.stop()

		for deb in self.debries:
			deb.stop()

	def restart(self):
		self.__init__()
