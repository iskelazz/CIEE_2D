import pygame
import random
import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE

cell_size = 40
cell_number = 20

class Hole(Sprite):
	def __init__(self, x,y):
		super().__init__()
		
		self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'wall_sprite.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
    
	



	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		
		adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
		screen.blit(self.image, adjusted_position)