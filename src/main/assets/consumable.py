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
    
    def randomize(self, snake_body, area, other_consumables_positions=None):
        # Desempaquetar el área en sus componentes
        area_x, area_y, area_width, area_height = area

        # Calcular límites del área en términos de celdas
        area_left = area_x
        area_top = area_y
        area_right = area_x + area_width
        area_bottom = area_y + area_height

        # Generar posiciones disponibles dentro del área definida
        available_positions = set((x, y) for x in range(area_left, area_right) 
                                  for y in range(area_top, area_bottom))

        # Excluir posiciones ocupadas por la serpiente y otros elementos
        snake_positions = {(int(pos.x), int(pos.y)) for pos in snake_body}
        available_positions -= snake_positions
        available_positions -= self.staticPositions
        #available_positions -= other_consumables_positions

        if available_positions:
            new_position = random.choice(list(available_positions))
            self.rect.x = new_position[0] * CELL_SIZE
            self.rect.y = new_position[1] * CELL_SIZE
            return True
        else:
            # No hay posiciones disponibles en el área dada
            return False

    def draw(self, screen, camera_offset):
        # Ajusta la posición de la manzana por el desplazamiento de la cámara
        adjusted_position = (self.rect.x - camera_offset.x, self.rect.y - camera_offset.y)
        screen.blit(self.image, adjusted_position)