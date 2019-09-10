import pygame
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from ship import Ship

def run_game():
	#初始化游戏，并创建一个屏幕对象
	pygame.init()                
	
	#创建一个设置实例
	ai_settings=Settings()
	
	# ~ ai_settings.screen_width=600    #修改实例
	# ~ ai_settings.screen_height=400
	ai_settings.alien_speed_factor=1
	ai_settings.ship_speed_factor=5
	ai_settings.bullet_speed_factor=5
	ai_settings.bullet_width=200

	#设置屏幕窗口尺寸和标题
	screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#创建一个子弹组,一个外星人组
	bullets=Group()
	aliens=Group()
	
	#创建一个飞船实例,,一个用于存储游戏统计信息的实例
	ship=Ship(screen,ai_settings)
	stats=GameStats(ai_settings)
	
	#创建一个按钮
	play_button=Button(ai_settings,screen,'Play')
	
	#创建外星人
	gf.create_fleet(aliens,ai_settings,screen,ship)

	# 创建一个记分牌
	sb = Scoreboard(ai_settings,screen,stats)
	
	#游戏主循环
	while True:
		gf.check_events(ship,ai_settings,screen,bullets,stats,play_button,aliens,sb)
		if stats.game_active :
			ship.update()
			gf.update_bullets(bullets,aliens,ai_settings,screen,ship,stats,sb)
			gf.update_aliens(aliens,ai_settings,bullets,screen,ship,stats,sb)
		gf.update_screen(ai_settings,screen,ship,aliens,bullets,play_button,stats,sb)
		
run_game()

