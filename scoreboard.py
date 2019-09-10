import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    '''显示得分信息'''
    def __init__(self,ai_settings,screen,stats):
        '''初始化得分显示的属性'''

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.ai_settings = ai_settings

        #显示得分时使用的字体设置
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,48)

        #准备初始得分图像,最高得分图像,登记图像,剩余飞船图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''将得分转换为一幅渲染的图像'''

        rounded_score = round(self.stats.score,-1)
        score_str = "{:,}".format(rounded_score)

        #创建得分图像
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)

        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_top = 20

    def prep_high_score(self):
        '''将最高得分转换为一幅渲染的图像'''
        high_score = round(self.stats.high_score,-1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str,True,self.text_color,self.ai_settings.bg_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.top = 20
        self.high_score_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        '''将等级转换为一幅渲染的图像'''
        prep_level = str(self.stats.level)
        self.level_image = self.font.render(prep_level,True,self.text_color,self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = self.score_rect.bottom + 20
        self.level_rect.right = self.screen_rect.right - 20

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.screen,self.ai_settings)
            ship.rect.top = 20
            ship.rect.left = 10 + ship.rect.width * ship_number
            self.ships.add(ship)

    def show_score(self):
        '''绘制图形'''
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.high_score_image,self.high_score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)