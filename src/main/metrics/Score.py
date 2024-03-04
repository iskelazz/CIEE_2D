import pygame
import os
from config import FONTS_DIR

#Se encarga de la puntuación 
class Score:
    def __init__(self, screen, screen_width):
        self.score = 0 
        self.SCORE_PER_APPLE = 100
        self.SCORE_PER_ROTTEN = 1000
        self.screen = screen
        self.screen_width = screen_width

    def draw_score(self):
        """Pinta la puntuación en el extremo superior izquierdo de la pantalla"""    
        font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 64)  
        score_surface = font.render(f'{self.score:06d}', True, pygame.Color('white'))
        score_rect = score_surface.get_rect(topright=(self.screen_width - 20, 20)) 
        self.screen.blit(score_surface, score_rect)
    
    def eat_red_apple(self):
        """Si la serpiente come una manzana roja, aumenta la puntuacion en 100"""
        self.score += self.SCORE_PER_APPLE

    def eat_rotten_apple(self):
        """Si la serpiente come una manzana podrida, disminuye la puntuacion en 1000"""
        self.score -= self.SCORE_PER_ROTTEN
