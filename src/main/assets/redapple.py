import pygame
import random
import os
from pygame.math import Vector2
from pygame.sprite import Sprite
from config import GRAPHICS_DIR

cell_size = 40
cell_number = 20

class RedApple(Sprite):
	def __init__(self):
		super().__init__()
		
		self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'apple.png')).convert_alpha()
		self.rect = self.image.get_rect()

	def randomize(self, walls, snake_body):
		while True:
			new_position = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
            # Verifica si la nueva posición no está ocupada por la serpiente o un muro
			if not any(new_position == Vector2(wall.rect.x / cell_size, wall.rect.y / cell_size) for wall in walls) and \
				new_position not in snake_body:
					self.rect.x = new_position.x * cell_size
					self.rect.y = new_position.y * cell_size
					break