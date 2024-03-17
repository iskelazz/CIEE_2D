from phases.AreaManager import AreaManager
import os
from assets.apple import Apple 
from config import Config
 
class RedApple(Apple):
	def __init__(self, staticPositions):
		super().__init__(os.path.join(Config.GRAPHICS_DIR, 'apple.png'), staticPositions)
	
	def handle_collision(self,segment,snake,game):
		area_manager = AreaManager()
		self.randomize(snake.body,area_manager.coords(area_manager.get_area_tag_by_object(self)))
		snake.add_block()
		game.score.eat_red_apple()
		snake.red_apple_sound.play()
		
