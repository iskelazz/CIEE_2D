import pygame
import random
import os
from pygame.math import Vector2
from pygame.sprite import Sprite
from config import GRAPHICS_DIR

cell_size = 40
cell_number = 20

class RedApple(Sprite):
	def __init__(self, staticPositions):
		super().__init__()
		
		self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'apple.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.staticPositions = staticPositions()

	def randomize(self, snake_body):
		available_positions = set((x, y) for x in range(cell_number) for y in range(cell_number))
			# Excluir posiciones ocupadas por la serpiente
		for pos in snake_body:
			available_positions.discard((pos.x, pos.y))
			
			# Excluir posiciones ocupadas por objetos estáticos
		available_positions -= self.staticPositions

		if available_positions:
			new_position = random.choice(list(available_positions))
			self.rect.x = new_position[0] * cell_size
			self.rect.y = new_position[1] * cell_size