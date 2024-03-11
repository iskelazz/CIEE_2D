from phases.AreaManager import AreaManager
import pygame
import os
from pygame.sprite import Sprite
from assets.consumable import Consumable 
from assets.snake.pacmanState import PacmanState

from config import GRAPHICS_DIR, CELL_SIZE

cell_number = 20 #temporal
 
class PacmanFruit(Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'cherry.png')).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x=x*CELL_SIZE
        self.rect.y=y*CELL_SIZE
    def draw(self, screen, camera_offset):
        # Ajusta la posición de la manzana por el desplazamiento de la cámara
        
        adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
        screen.blit(self.image, adjusted_position)
    
    def handle_collision(self,segment,snake,game):
        self.kill()
        snake.set_state(PacmanState(snake))
