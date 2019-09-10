import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	def __init__(self,screen,ai_settings):
		"""初始化飞船，并设置其初始位置"""
		#继承 Sprite 为了创建飞船组
		super().__init__()

		self.screen=screen
		self.ai_settings=ai_settings
		
		#加载飞船图像，并获取其外接矩形
		self.image=pygame.image.load('images/ship.bmp')
		
		self.rect=self.image.get_rect()
		self.screen_rect=self.screen.get_rect()
		
		#将每艘飞船放在底部中央
		self.rect.x=self.screen_rect.centerx #在屏幕矩形上的位置
		self.rect.y=self.screen_rect.height-50
		
		#在飞船的属性center 中存储小数值
		self.centerx = float(self.rect.centerx)
		self.centery = float(self.rect.centery)
		
		self.moving_right=False
		self.moving_left=False
		self.moving_up=False
		self.moving_down=False
	
	def update(self):
		'''持续移动'''
		#更新飞船的center,并限制飞船移动范围
		if self.centerx > self.ai_settings.screen_width-10:
			self.centerx -=1
		elif self.centerx < 10:
			self.centerx +=1
		elif self.centery > self.ai_settings.screen_height-10:
			self.centery -=1
		elif self.centery < 10:
			self.centery +=1
		else:
			if self.moving_right:
				self.centerx += self.ai_settings.ship_speed_factor
			elif self.moving_left:
				self.centerx -= self.ai_settings.ship_speed_factor
			elif self.moving_up:
				self.centery -=self.ai_settings.ship_speed_factor
			elif self.moving_down:
				self.centery +=self.ai_settings.ship_speed_factor
				
		#根据self.center 更新rect对象
		self.rect.centerx = self.centerx
		self.rect.centery = self.centery
		
	def center_ship(self):
		'''把飞船放到屏幕底部中央'''            #因为之前在飞船的属性center 中存储了精确值，之后又将
		self.centerx=self.screen_rect.centerx#self.rect.centerx=self.centerx,做了这个转换，
		self.centery=self.screen_rect.bottom-50 #而在主循环中单独更新了 ship.update()
		
	def blitme(self):
		"""在指定位置放置飞船"""
		self.screen.blit(self.image,self.rect)
		
