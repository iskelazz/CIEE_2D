import pygame
import random
import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE

cell_size = 40
cell_number = 20
#Objeto para el cambio de nivel, Sprite temporal
class Key(Sprite):
	def __init__(self, x,y,door):
		super().__init__()
		#cambiar sprite
		self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'key.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.picked=False
		self.door=door

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		if self.picked==False:
			adjusted_position = (self.rect.x - camera_offset.x, 
								self.rect.y - camera_offset.y)
			screen.blit(self.image, adjusted_position)
		else: pass
	def pick_up(self):
		self.picked=True
		self.door.open()
	
	def handle_collision(self,segment,snake,game):
		self.pick_up()