from assets.snake.fastState import FastState
from assets.consumable import Consumable 
from config import Config

#Objeto para el cambio de nivel, Sprite temporal
class Gemstone(Consumable):
	def __init__(self, x,y):
		super().__init__('gemstone.png')
		#cambiar sprite
		self.rect.x=x*Config.CELL_SIZE
		self.rect.y=y*Config.CELL_SIZE

	def draw(self, screen, camera_offset):
		# Ajusta la posición de la gema por el desplazamiento de la cámara
		
		adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
		screen.blit(self.image, adjusted_position)

	def handle_collision(self,segment,snake,game):
		self.kill()
		snake.set_state(FastState(snake))