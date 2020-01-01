import pygame
from math import sin, cos, atan2, pi, sqrt
import random

from handleScore import saveScore

pygame.init()


def dist(x1,y1,x2,y2):
	return sqrt((x1-x2)**2 + (y1-y2)**2)

class Enemy:
	def __init__(self,pos=None,size=20,color=(0,200,0)):
		self.size = random.randint(size-3,size+3)
		self.pos = (x,y) = (random.randint(0,400),random.randint(0,600))
		self.points = []
		self.color = color
		self.vel = (random.randint(-6,6),random.randint(-6,6))
		self.life = 3
		self.isstop = False

		if self.vel[0]==0 and self.vel[1]==0:
			self.vel = (1,1)

		sides = ["top","right","bottom","left"]
		side = random.randint(0,3)
		if sides[side] == "top":
			self.pos = (x,y) = (random.randint(0,400),-60)
		elif sides[side] == "right":
			self.pos = (x,y) = (460,random.randint(0,600))
		elif sides[side] == "bottom":
			self.pos = (x,y) = (random.randint(0,400),660)
		elif sides[side] == "left":
			self.pos = (x,y) = (-60,random.randint(0,600))

		if pos:
			self.pos = pos


		self.generate_points()

	def generate_points(self):
		points = []
		x,y = self.pos
		size = self.size
		n = random.randint(8,10)  # random no. of vertices for polygon
		for i in range(n):
			xi = x + size*cos(2*pi*i/n) + random.random()*size*.5	#random shape of polygons
			yi = y + size*sin(2*pi*i/n) + random.random()*size*.5

			points.append((int(xi), int(yi)))
		self.points = points


	def update(self):

		if not self.isstop:
			x,y = self.pos
			x += self.vel[0]
			y += self.vel[1]
			self.pos = (x,y)
			points = []
			for i,j in self.points:
				i += self.vel[0]
				j += self.vel[1]
				points.append((int(i), int(j)))
			self.points = points

	def draw(self,surf):
		pygame.draw.polygon(surf,self.color, self.points, 0)
		# pygame.draw.circle(surf,self.color, self.pos, self.size, 1)

	def exceeds_boundary(self):
		x,y = self.pos
		return x>460 or x<-60 or y>660 or y<-60

	def get_pos(self):
		return self.pos

	def get_size(self):
		return self.size

	def get_life(self):
		return self.life

	def damage(self):
		self.life -= 1

	def stop(self):
		self.isstop = True

	def resume(self):
		self.isstop = False




	def checkEvents(self,ev):
		# if ev.type == pygame.KEYDOWN:
		# 	if ev.key == pygame.K_SPACE:
		# 		self.fire()
		# 	elif ev.key == pygame.K_s:
		# 		if(pygame.key.get_pressed()[pygame.K_s]):
		# 			self.setVel(0,1)
		# 	elif ev.key == pygame.K_d:
		# 		self.setVel(1,0)
		# 	elif ev.key == pygame.K_a:
		# 		self.setVel(-1,0)
			
		# 	self.turned =True
		pass




class Bullet:
	def __init__(self,x,y,ang):
		self.pos = (x,y)
		self.angle = ang
		self.speed = 10
		self.color = (0,0,0)
		self.isstop = False

	def update(self):

		if not self.isstop:
			x,y = self.pos
			ang = self.angle
			x+=self.speed*cos(ang)
			y+=self.speed*sin(ang)
			self.pos = (int(x), int(y))

	def draw(self,surf):
		pygame.draw.circle(surf,self.color, self.pos, 2)

	def exceeds_boundary(self):
		x,y = self.pos
		return x>460 or x<-60 or y>660 or y<-60

	def get_pos(self):
		return self.pos

	def stop(self):
		self.isstop = True

	def resume(self):
		self.isstop = False



class Player:
	def __init__(self):
		self.pos = (100,200)
		self.angle = 0
		self.vel = (0,0)
		self.acc =  (0,0)
		self.omega = 0
		self.size = 10
		self.color = (0,150,200)
		self.isstop = False
		self.score = 0

		self.bullets = []

		self.setVel(0,0)


	def draw(self,surf):
		x,y = self.pos
		ang = self.angle
		length = 12
		tip_x = x+length*cos(ang)
		tip_y = y+length*sin(ang)

		pygame.draw.circle(surf,self.color, (x,y), self.size)
		pygame.draw.line(surf,(0,0,0), (x,y), (int(tip_x), int(tip_y)), 3)
		pygame.draw.circle(surf, (200,0,0), (x,y), 4)

		for bullet in self.bullets:
			bullet.draw(surf)
		

	def update(self):

		if not self.isstop:
			x,y = self.pos
			ang = self.angle
			x+=self.vel[0] + self.acc[0]
			y+=self.vel[1] + self.acc[1]
			ang+=self.omega
			self.pos = (int(x), int(y))
			self.angle = ang

			mouse = pygame.mouse.get_pos()
			a = (atan2(mouse[1]-y, mouse[0]-x) + 2*pi)%(2*pi)

			# self.setAng(a)
			self.setOmega(-1*(ang-a))

			for bullet in self.bullets:
				bullet.update()

			i=0
			while i!=len(self.bullets):					# deleting bullets that exceed the boundaries
				if self.bullets[i].exceeds_boundary():
					b = self.bullets[i]
					self.bullets.remove(b)
				else:
					i+=1


			s = .12
			if(pygame.key.get_pressed()[pygame.K_w]):
				self.setVel(0,-s)
			if(pygame.key.get_pressed()[pygame.K_s]):
				self.setVel(0,s)
			if(pygame.key.get_pressed()[pygame.K_a]):
				self.setVel(-s,0)
			if(pygame.key.get_pressed()[pygame.K_d]):
				self.setVel(s,0)


	def setVel(self,x,y):
		_x,_y = self.acc = self.vel
		_x=max(-3,min(_x+x,3))
		_y=max(-3,min(_y+y,3))
		self.vel = (_x,_y)
	def setOmega(self,omega):
		self.omega = omega

	def get_pos(self):
		return self.pos

	def get_size(self):
		return self.size

	def setAng(self,ang):
		self.angle = ang


	def increaseScore(self,score):
		self.score+=score


	def fire(self):
		self.bullets.append(Bullet(*self.pos, self.angle))

	def hit(self,enemy):
		enemy_x,enemy_y = enemy.get_pos()
		enemy_size = enemy.get_size()
		for b in self.bullets:
			bx, by = b.get_pos()
			if dist(bx,by,enemy_x,enemy_y)<enemy_size:
				self.bullets.remove(b)
				return True
		return False

	def isCollide(self, enemies):
		x,y = self.get_pos()
		size = self.get_size()
		for e in enemies:
			e_x, e_y = e.get_pos()
			e_size = e.get_size()
			if dist(x,y,e_x,e_y)<size+e_size:
				self.isdead = True
				return True

	def exceeds_boundary(self):
		x,y = self.get_pos()
		s  = self.get_size()
		if x+s>400 or x-s<0 or y+s>600 or y-s<0:
			self.isdead = True
			return True


	def stop(self):
		self.isstop = True

	def resume(self):
		self.isstop = False


	def checkEvents(self,ev):
		if ev.type == pygame.KEYDOWN:
			if ev.key == pygame.K_SPACE:
				self.fire()
		# 	elif ev.key == pygame.K_s:
		# 		if(pygame.key.get_pressed()[pygame.K_s]):
		# 			self.setVel(0,1)
		# 	elif ev.key == pygame.K_d:
		# 		self.setVel(1,0)
		# 	elif ev.key == pygame.K_a:
		# 		self.setVel(-1,0)
			
		# 	self.turned =True
		pass

	def __del__(self):
		saveScore(self.score)
