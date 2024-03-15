import pygame
import os
from assets.consumable import Consumable 
from assets.snake.pacmanState import PacmanState

from config import CELL_SIZE,SOUNDS_DIR

 
class PacmanFruit(Consumable):
    def __init__(self, x,y):
        super().__init__('cherry.png')
        self.rect.x=x*CELL_SIZE
        self.rect.y=y*CELL_SIZE
        self.pacman_fruit_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'pacman_fruit.mp3'))
    
    def handle_collision(self,segment,snake,game):
        self.pacman_fruit_sound.play()
        self.kill()
        snake.set_state(PacmanState(snake))


