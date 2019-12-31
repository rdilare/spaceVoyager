import pygame
from math import sin, cos, atan2, pi
import random

pygame.init()



class Enemy:
	def __init__(self):
		self.size = size = random.randint(15,25)
		self.pos = (x,y) = (random.randint(0,400),random.randint(0,600))
		self.points = []
		self.color = (0,200,0)
		self.vel = (random.randint(-5,5),random.randint(-5,5))

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


		self.generate_points()

	def generate_points(self):
		points = []
		x,y = self.pos
		size = self.size
		n = random.randint(8,10)  # random no. of vertices for polygon
		for i in range(n):
			xi = x + size*cos(2*pi*i/n) + random.random()*10	#random shape of polygons
			yi = y + size*sin(2*pi*i/n) + random.random()*10

			points.append((int(xi), int(yi)))
		self.points = points


	def update(self):

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
		self.speed = 15
		self.color = (0,0,0)

	def update(self):
		x,y = self.pos
		ang = self.angle
		x+=self.speed*cos(ang)
		y+=self.speed*sin(ang)
		self.pos = (int(x),int(y))

	def draw(self,surf):
		pygame.draw.circle(surf,self.color, self.pos, 2)

	def exceeds_boundary(self):
		x,y = self.pos
		return x>460 or x<-60 or y>660 or y<-60



class Player:
	def __init__(self):
		self.pos = (50,80)
		self.angle = 0
		self.vel = (0,0)
		self.omega = 0
		self.radius = 10
		self.color = (0,150,200)

		self.bullets = []

		self.setVel(0,0)


	def draw(self,surf):
		x,y = self.pos
		ang = self.angle
		length = 12
		tip_x = x+length*cos(ang)
		tip_y = y+length*sin(ang)

		pygame.draw.circle(surf,self.color, (x,y), self.radius)
		pygame.draw.line(surf,(0,0,0), (x,y), (int(tip_x), int(tip_y)), 3)
		pygame.draw.circle(surf, (200,0,0), (x,y), 4)

		for bullet in self.bullets:
			bullet.draw(surf)
		

	def update(self):
		x,y = self.pos
		ang = self.angle
		x+=self.vel[0]
		y+=self.vel[1]
		ang+=self.omega
		self.pos = (x,y)
		self.angle = ang

		mouse = pygame.mouse.get_pos()
		a = (atan2(mouse[1]-y, mouse[0]-x) + 2*pi)%(2*pi)

		# self.setAng(a)
		self.setOmega(-1*(ang-a))

		for bullet in self.bullets:
			bullet.update()

		i=0
		while i!=len(self.bullets):					# deleting bullets that exceed the boundary
			if self.bullets[i].exceeds_boundary():
				b = self.bullets[i]
				self.bullets.remove(b)
			else:
				i+=1


		if(pygame.key.get_pressed()[pygame.K_w]):
			self.setVel(0,-1)
		if(pygame.key.get_pressed()[pygame.K_s]):
			self.setVel(0,1)
		if(pygame.key.get_pressed()[pygame.K_a]):
			self.setVel(-1,0)
		if(pygame.key.get_pressed()[pygame.K_d]):
			self.setVel(1,0)


	def setVel(self,x,y):
		_x,_y = self.vel
		_x=max(-3,min(_x+x,3))
		_y=max(-3,min(_y+y,3))
		self.vel = (_x,_y)
	def setOmega(self,omega):
		self.omega = omega

	def setPos(self,x,y):
		self.pos = (x,y)

	def setAng(self,ang):
		self.angle = ang

	def fire(self):
		self.bullets.append(Bullet(*self.pos, self.angle))

	def stop(self):
		pass

	def resume(self):
		pass

	def restart(self):
		pass

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
