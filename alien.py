import pygame
from pygame.sprite import Sprite
class Alien(Sprite):
	'''创建一个描述外星人的类'''
	def __init__(self,ai_settings,screen):
		super().__init__()
		self.screen=screen
		self.ai_settings=ai_settings
		
		#导入外星人rect属性，并指定位置
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#设置第一个外星人初始位置
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#存储外星人准确位置
		self.x = float(self.rect.x)
		
	def blitme(self):
		'''在指定位置绘制外星人'''
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		'''向左或向右移动外星人'''
		# print(self.rect.x)
		self.rect.x += (self.ai_settings.alien_speed_factor
		                              *self.ai_settings.fleet_direction)
		# self.rect.x = self.x
		# print(self.rect.x)

	    
	def check_edges(self):
		'''判断外星人是否到达边缘，是则返回True'''
		screen_rect = self.screen.get_rect()
		if self.rect.left <=screen_rect.left:
			return True
		elif self.rect.right >=screen_rect.right:
			return True
	
	
