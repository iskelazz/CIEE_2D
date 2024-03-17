from assets.door import Door
import pygame
import os
from config import Config

#Objeto para el cambio de nivel, Sprite temporal
class PointsDoor(Door):
	def __init__(self, x,y,vertical,score,openscore, use_text=True):
		super().__init__(x,y,vertical)
		self.score=score
		self.openscore = openscore
		self.font = pygame.font.Font(os.path.join(Config.FONTS_DIR, 'Another_.ttf'), 20)
		self.use_text = use_text

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la manzana por el desplazamiento de la cámara
		if self.closed==True:
			adjusted_position = (self.rect.x - camera_offset.x, 
								self.rect.y - camera_offset.y)
			screen.blit(self.image, adjusted_position)

			#Texto indicativo de los puntos
			if self.use_text:
				text = f"{self.openscore}"  # Calcula los puntos que faltan
				text_surface = self.font.render(text, True, (255, 255, 255))  # Crea una superficie de texto en blanco
				text_rect = text_surface.get_rect(center=(self.rect.x + Config.CELL_SIZE/2 - camera_offset.x, 
								self.rect.y + Config.CELL_SIZE/2 - camera_offset.y))  # Posiciona el texto justo arriba de la puerta
				screen.blit(text_surface, text_rect)        
		else: pass
	
	def update(self):
		if self.score.score>=self.openscore:
			super().open()
		else: pass


