import pygame
import os
from pygame.sprite import Sprite
from config import Config

#Objeto para el cambio de nivel, Sprite temporal
class Door(Sprite):
	def __init__(self, x,y,vertical):
		super().__init__()
		if vertical:
			self.image = pygame.image.load(os.path.join(Config.GRAPHICS_DIR, 'fence_ver.png')).convert_alpha()
		else:
			self.image = pygame.image.load(os.path.join(Config.GRAPHICS_DIR, 'fence_hor.png')).convert_alpha()
		self.rect = self.image.get_rect()
		self.rect.x=x
		self.rect.y=y
		self.closed=True
		
		self.open_door_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'door_open.wav'))

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		if self.closed==True:
			adjusted_position = (self.rect.x - camera_offset.x, 
								self.rect.y - camera_offset.y)
			screen.blit(self.image, adjusted_position)

		else: pass

	def open(self):
		if self.closed:
			self.open_door_sound.play()
			self.closed=False
	
	def close(self):
		if not self.closed:
			self.closed=True
	
	def handle_collision(self,segment,snake,game):
		if self.closed==True:
			game.screen_manager.push_state('GAME_OVER')
		else: pass

		