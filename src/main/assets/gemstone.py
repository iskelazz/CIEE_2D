import pygame
from assets.snake.fastState import FastState
import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE

#Objeto para el cambio de nivel, Sprite temporal
class Gemstone(Sprite):
	def __init__(self, x,y):
		super().__init__()
		#cambiar sprite
		self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'gemstone.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x=x*CELL_SIZE
		self.rect.y=y*CELL_SIZE

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la gema por el desplazamiento de la cámara
		
		adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
		screen.blit(self.image, adjusted_position)

	def handle_collision(self,segment,snake,game):
		self.kill()
		snake.set_state(FastState(snake))