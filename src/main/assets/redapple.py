from phases.AreaManager import AreaManager
import os
from assets.consumable import Consumable 
from config import GRAPHICS_DIR, CELL_SIZE

cell_number = 20 #temporal
 
class RedApple(Consumable):
	def __init__(self, staticPositions):
		super().__init__(os.path.join(GRAPHICS_DIR, 'apple.png'), staticPositions)
	
	def handle_collision(self,segment,snake,game):
		area_manager = AreaManager()
		self.randomize(snake.body,area_manager.coords(area_manager.get_area_tag_by_object(self)))
		snake.add_block()
		game.score.eat_red_apple()
