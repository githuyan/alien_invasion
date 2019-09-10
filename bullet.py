import pygame
from pygame.sprite import Sprite
class Bullet(Sprite):
	'''创建一个描述子弹的类'''
	def __init__(self,ai_settings,screen,ship):
		super().__init__()
		self.screen=screen
		
		#在（0,0）处创建一个子弹，并将其移到合适的位置
		self.rect = pygame.Rect(0,0,ai_settings.bullet_width,\
		                            ai_settings.bullet_height)
		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top
		
		#存储子弹精确位置,颜色，速度
		self.y = float(self.rect.y)
		self.color = ai_settings.bullet_color
		self.speed_factor = ai_settings.bullet_speed_factor
		
	def update(self):
		'''向上移动子弹'''
		self.y -= self.speed_factor
		self.rect.y = self.y
		
	def draw_bullet(self):
		'''在屏幕上绘制子弹'''
		pygame.draw.rect(self.screen,self.color,self.rect)
		
		
		
