import pygame

import os
from pygame.sprite import Sprite
from config import Config

#Objeto para el cambio de nivel, Sprite temporal
class Key(Sprite):
	def __init__(self, x,y,doors):
		super().__init__()
		#cambiar sprite
		original_image = pygame.image.load(os.path.join(Config.GRAPHICS_DIR, 'key.png')).convert_alpha()
		self.image = pygame.transform.scale(original_image, (Config.CELL_SIZE, Config.CELL_SIZE))
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.picked=False
		self.doors=doors

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		if self.picked==False:
			adjusted_position = (self.rect.x - camera_offset.x, 
								self.rect.y - camera_offset.y)
			screen.blit(self.image, adjusted_position)
		else: pass
	def pick_up(self):
		self.picked=True
		for door in self.doors:  # Abrir todas las puertas en la lista
			door.open()
	
	def handle_collision(self,segment,snake,game):
		self.pick_up()