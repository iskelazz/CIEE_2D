import pygame
import os
from pygame.sprite import Sprite
from assets.consumable import Consumable 
from config import Config
 
class GoldenApple(Consumable):
	def __init__(self, x, y):
		super().__init__('golden_apple.png')
		self.rect.x=x*Config.CELL_SIZE
		self.rect.y=y*Config.CELL_SIZE
	

	def handle_collision(self,segment,snake,game):
		self.kill()
		game.score.eat_golden_apple()
