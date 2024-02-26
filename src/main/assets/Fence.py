import pygame
import os
from pygame.math import Vector2
from pygame.sprite import Sprite
from config import GRAPHICS_DIR

cell_size = 40
cell_number = 20

class Fence(Sprite):
    def __init__(self, position, orientation='horizontal'):
        super().__init__()
        # Selecciona el sprite basado en la orientación
        original_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'stone_wall.png')).convert_alpha()
        scaled_image = pygame.transform.scale(original_image, (cell_size, cell_size))
        if orientation == 'vertical':
            scaled_image = pygame.transform.rotate(scaled_image, 90)
        self.image = scaled_image
        self.rect = self.image.get_rect(topleft=(position.x * cell_size, position.y * cell_size))

    @staticmethod
    def create_fences():
        fences = pygame.sprite.Group()
    # Crear muros en la columna 3, desde la fila 3 hasta la fila 8 (vertical)
        for row in range(2, 9):
            fences.add(Fence(Vector2(2, row), 'vertical'))
    # Crear muros en la fila 13, desde la columna 2 hasta la columna 12 (horizontal)
        for column in range(2, 13):
            fences.add(Fence(Vector2(column, 12), 'horizontal'))
    
        return fences