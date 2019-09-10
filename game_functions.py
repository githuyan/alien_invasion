import pygame
import sys
from random import randint
from time import sleep
from bullet import Bullet
from alien import Alien
from ship import Ship

def check_keydown_events(event,ship,ai_settings,screen,
                                                bullets,aliens,stats,sb):
	'''响应按键'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right=True
		# ~ print('RIGHT')           #检测右键是否响应
	elif event.key == pygame.K_LEFT:
		ship.moving_left=True
	elif event.key == pygame.K_UP:
		ship.moving_up=True
	elif event.key == pygame.K_DOWN:
		ship.moving_down=True

	#空格键开火
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings,screen,ship,bullets)
	# 'q' 键停止游戏
	elif event.key == pygame.K_q:
		sys.exit()
	# 'p' 键开始游戏
	elif event.key == pygame.K_p:
		start_game(aliens,bullets,ai_settings,screen,ship,stats,sb)
		
def check_keyup_events(event,ship):
	'''响应松键'''
	if event.key == pygame.K_RIGHT:
		ship.moving_right=False
	elif event.key == pygame.K_LEFT:
		ship.moving_left=False
	elif event.key == pygame.K_UP:
		ship.moving_up=False
	elif event.key == pygame.K_DOWN:
		ship.moving_down=False
	
		
def start_game(aliens,bullets,ai_settings,screen,ship,stats,sb):
	'''仅当游戏不活跃时 按键 p 开始游戏'''
	if not stats.game_active:
		#在游戏活跃时 隐藏光标
		pygame.mouse.set_visible(False)
		
		#使游戏开始处于活跃
		stats.reset_stats()
		stats.game_active = True
		
		#清空外星人和子弹
		bullets.empty()
		aliens.empty()
		
		#创建新的外星人，并测试外星人和飞船的碰撞
		create_fleet(aliens,ai_settings,screen,ship)
		ship_hit(aliens,bullets,ai_settings,screen,ship,stats,sb)
				
def check_events(ship,ai_settings,screen,bullets,stats,play_button,aliens,sb):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ship,ai_settings,screen,bullets,
			                                              aliens,stats,sb)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship)
			
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos()
			check_paly_button(mouse_x,mouse_y,stats,play_button,
			                    bullets,aliens,ai_settings,screen,ship,sb)
			
def check_paly_button(mouse_x,mouse_y,stats,play_button,bullets,
                                       aliens,ai_settings,screen,ship,sb):
	'''仅在玩家单击play按钮 且游戏不活跃时，开始游戏'''
	
	click_button = play_button.rect.collidepoint(mouse_x,mouse_y)
	if click_button and not stats.game_active:

		#在游戏活跃时 隐藏光标
		pygame.mouse.set_visible(False)
		
		#使游戏开始处于活跃
		stats.reset_stats()
		stats.game_active = True
		
		#清空外星人和子弹
		bullets.empty()
		aliens.empty()
		
		#创建新的外星人，并测试外星人和飞船的碰撞
		create_fleet(aliens,ai_settings,screen,ship)
		ship_hit(aliens,bullets,ai_settings,screen,ship,stats,sb)
		
def update_bullets(bullets,aliens,ai_settings,screen,ship,stats,sb):
	'''更新子弹的位置，并删除已消失的子弹'''
	#更新子弹的位置
	bullets.update()

	#删除已消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.y <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collision(aliens,ai_settings,screen,ship,bullets,stats,sb)

def check_bullet_alien_collision(aliens,ai_settings,screen,ship,bullets,stats,sb):
	'''检查子弹与外星人的碰撞'''
	#检查是否有子弹击中外星人，如果是，则清除子弹和外星人
	# ~ collisions = pygame.sprite.groupcollide(bullets,aliens,True True)
	collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()

			#更新最高得分
			check_high_score(stats, sb)

	if len(aliens) == 0:
		#加快游戏节奏，清除所有子弹，并创造一群新的外星人
		ai_settings.increase_speed()
		bullets.empty()
		create_fleet(aliens,ai_settings,screen,ship)

		#等级提高
		stats.level += 1
		sb.prep_level()

		
def check_aliens_bottom(aliens,bullets,ai_settings,screen,ship,stats,sb):
	'''检测外星人是否到达屏幕底部'''
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(aliens,bullets,ai_settings,screen,ship,stats,sb)
			break
		
def ship_hit(aliens,bullets,ai_settings,screen,ship,stats,sb):
	'''检查外星人与飞船的碰撞'''
	if stats.ships_left > 0:
		stats.ships_left -= 1

		#更新飞船数量
		sb.prep_ships()
		
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
		
		#创建一群新的外星人，并把飞船放到底部中央
		create_fleet(aliens,ai_settings,screen,ship)
		ship.center_ship()
		
		#清空后暂停
		sleep(0.5)	
	else:
		stats.game_active = False
		#在重开另一局游戏时显现光标
		pygame.mouse.set_visible(True)
		#在重开另一局游戏时重置游戏速度
		ai_settings.initialize_dynamic_settings()
		#重置等级信息
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		#重置飞船数量
		sb.prep_ships()

def fire_bullet(ai_settings,screen,ship,bullets):
	#如果没有到达限制就发射一颗子弹
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet=Bullet(ai_settings,screen,ship)
		bullets.add(new_bullet)
		
def get_number_aliens_x(ai_settings,alien_width):
	'''计算每行外星人'''
	available_space_x=ai_settings.screen_width-2*alien_width
	number_aliens_x=int(available_space_x/(2*alien_width))
	return number_aliens_x

def get_number_rows(ship_height,ai_settings,alien_height):
	'''计算每列外星人'''
	available_space_y=ai_settings.screen_height-2*alien_height-ship_height
	number_rows=int(available_space_y/(2*alien_height))
	return number_rows

def create_alien(aliens,ai_settings,screen,alien_number,row_number):
	'''创造每一个外星人'''
	alien=Alien(ai_settings,screen)
	alien_width=alien.rect.x
	alien_height=alien.rect.y
	alien.rect.x=alien_width+2*alien_width*alien_number
	alien.rect.y=alien_height+2*alien_height*row_number
	aliens.add(alien)
	
def create_fleet(aliens,ai_settings,screen,ship):
	'''创建每一行外星人'''
	alien=Alien(ai_settings,screen)
	number_aliens_x=get_number_aliens_x(ai_settings,alien.rect.width)
	number_rows=get_number_rows(ship.rect.height,ai_settings,alien.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(aliens,ai_settings,screen,alien_number,row_number)

def check_fleet_edges(aliens,ai_settings):
	'''若外星人到达边缘，则采取措施'''
	for alien in aliens.sprites():
		if alien.check_edges():
				change_fleet_direction(aliens,ai_settings)
				break
		
def change_fleet_direction(aliens,ai_settings):
	'''下移并改变外星人舰队方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def update_aliens(aliens,ai_settings,bullets,screen,ship,stats,sb):
	'''外星人若到达边缘，则调整方向'''
	check_fleet_edges(aliens,ai_settings)
	
	aliens.update()
	# for alien in aliens.sprites():
	# 	alien.update()

	#检查外星人与飞船的碰撞，是则重开一局
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(aliens,bullets,ai_settings,screen,ship,stats,sb)
	#检查外星人是否到达底部，是则重开一局
	check_aliens_bottom(aliens,bullets,ai_settings,screen,ship,stats,sb)

def check_high_score(stats,sb):
	'''检查是否是最高得分'''
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
	
def update_screen(ai_settings,screen,ship,aliens,bullets,play_button,stats,sb):
	'''更新屏幕上的图像，并切换到新屏幕'''
		
	#每次循环都重绘屏幕
	screen.fill(ai_settings.bg_color)

	#更新并绘制记分牌
	sb.show_score()

	#在飞船和外星人后面绘制子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	#使飞船绘制在屏幕上
	ship.blitme()
	
	#使外星人绘制到屏幕上
	aliens.draw(screen)
	
	#如果游戏处于非活跃状态，就绘制play按钮
	if not stats.game_active:
		play_button.draw_button()

	#让最近绘制的屏幕可见
	pygame.display.flip()