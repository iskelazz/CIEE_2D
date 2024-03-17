import pygame
import random
import os
from pygame.sprite import Sprite
from config import Config

class Hole(Sprite):
	def __init__(self, x,y):
		super().__init__()
		#cambiar sprite
		self.image = pygame.image.load(os.path.join(Config.GRAPHICS_DIR, 'flame_left.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		
		adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
		screen.blit(self.image, adjusted_position)