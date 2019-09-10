class GameStats():
	'''跟踪游戏的统计信息'''
	def __init__(self,ai_settings):
		'''初始化统计信息'''
		self.ai_settings=ai_settings
		self.game_active=False

		#初始化方法
		self.reset_stats()

		#最高得分
		self.high_score = 0
		
	def reset_stats(self):
		'''初始化在游戏期间可能变化的统计信息'''
		#剩余飞船数量
		self.ships_left = self.ai_settings.ship_limit
		#得分信息
		self.score = 0
		#等级信息
		self.level = 1


