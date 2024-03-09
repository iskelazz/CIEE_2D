import pygame
import random
import os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR, CELL_SIZE

cell_number = 20  # temporal

class Consumable(Sprite):
    def __init__(self, image_path, staticPositions):
        super().__init__()

        self.image = pygame.image.load(os.path.join(GRAPHICS_DIR, image_path)).convert_alpha()
        self.rect = self.image.get_rect()
        self.staticPositions = staticPositions()
    
    def randomize(self, snake_body):
        available_positions = set((x, y) for x in range(cell_number) for y in range(cell_number))
        # Excluir posiciones ocupadas por la serpiente
        for pos in snake_body:
            available_positions.discard((pos.x, pos.y))
        
        # Excluir posiciones ocupadas por objetos estáticos
        available_positions -= self.staticPositions

        if available_positions:
            new_position = random.choice(list(available_positions))
            self.rect.x = new_position[0] * CELL_SIZE
            self.rect.y = new_position[1] * CELL_SIZE

    def draw(self, screen, camera_offset):
        # Ajusta la posición de la manzana por el desplazamiento de la cámara
        adjusted_position = (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y)
        screen.blit(self.image, adjusted_position)