import pygame

import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE, SOUNDS_DIR

#Objeto para el cambio de nivel, Sprite temporal
class Key(Sprite):
	def __init__(self, x,y,doors):
		super().__init__()
		#cambiar sprite
		original_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'key.png')).convert_alpha()
		self.image = pygame.transform.scale(original_image, (CELL_SIZE, CELL_SIZE))
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.picked=False
		self.doors=doors
		self.open_door_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'door_open.wav'))

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
		self.open_door_sound.play()
		self.pick_up()