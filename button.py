import pygame.font
class Button():
	'''创建一个 play 按钮'''
	def __init__(self,ai_settings,screen,msg):
		#初始化属性
		self.screen = screen
		self.screen_rect=screen.get_rect()
		
		#设置按钮宽高，按钮颜色蓝，填充文本颜色红，字体=None,字号
		self.width,self.height =200,50
		self.button_color=38,63,229
		self.text_color=229,38,38
		self.font = pygame.font.SysFont(None,48)
		
		#获取按钮rect对象,并使其居中
		self.rect = pygame.Rect(0,0,self.width,self.height)
		
		# ~ self.rect.y = self.screen_rect.centerx
		# ~ self.rect.x = self.screen_rect.centery
		self.rect.center = self.screen_rect.center
		
		#按钮的标签只创建一次
		self.prep_msg(msg)
		
	def prep_msg(self,msg):
		'''将msg渲染为图像，并在按钮图形上居中'''
		self.msg_image = self.font.render(msg,True,self.text_color,self.button_color)
		#获取msg外接矩形
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
		
	def draw_button(self):
		'''绘制一个用颜色填充的按钮，在绘制文本'''
		self.screen.fill(self.button_color,self.rect)
		self.screen.blit(self.msg_image,self.msg_image_rect)
		
