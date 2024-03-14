import pygame

import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE

cell_number = 20  # temporal

class Consumable(Sprite):
    def __init__(self, image_path):
        super().__init__()
        original_image = pygame.image.load(os.path.join(GRAPHICS_DIR, image_path)).convert_alpha()
        self.image = pygame.transform.scale(original_image, (CELL_SIZE, CELL_SIZE))
        self.rect = self.image.get_rect()
    
    
    def draw(self, screen, camera_offset):
        # Ajusta la posición de la manzana por el desplazamiento de la cámara
        adjusted_position = (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y)
        screen.blit(self.image, adjusted_position)