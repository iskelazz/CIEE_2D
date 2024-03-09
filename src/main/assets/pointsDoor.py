import pygame
import random
import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE
from assets.door import Door

cell_size = 40
cell_number = 20
#Objeto para el cambio de nivel, Sprite temporal
class PointsDoor(Door):
	def __init__(self, x,y,vertical,score):
		super().__init__(x,y,vertical)
		self.score=score

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		if self.closed==True:
			adjusted_position = (self.rect.x - camera_offset.x, 
								self.rect.y - camera_offset.y)
			screen.blit(self.image, adjusted_position)    
		else: pass
	
	def update(self):
		if self.score.score>300:
			super().open()
		else: pass

