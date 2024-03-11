import pygame
import os
from pygame.sprite import Sprite
from assets.consumable import Consumable 
from config import GRAPHICS_DIR, CELL_SIZE
 
class GoldenApple(Consumable):
	def __init__(self, x, y):
		super().__init__('golden_apple.png')
		self.rect.x=x*CELL_SIZE
		self.rect.y=y*CELL_SIZE
	

	def handle_collision(self,segment,snake,game):
		self.kill()
		game.score.eat_golden_apple()
