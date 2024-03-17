import pygame
from pygame.math import Vector2
from config import SCREEN_HEIGHT, SCREEN_WIDTH

class Camera:
    def __init__(self, follow_strategy):
        self.offset = Vector2(0, 0)
        self.follow_strategy = follow_strategy

    def update(self, target):
        self.offset = self.follow_strategy.get_offset(target)

class FollowStrategy:
    def get_offset(self, target):
        raise NotImplementedError
#Patron estrategia para decidir como se va mover la camara
class FollowSnake(FollowStrategy):
    def get_offset(self, snake):
        # Coordenadas objetivo basadas en la posición de la cabeza de la serpiente
        target_x = snake.segments.sprites()[0].rect.centerx - SCREEN_WIDTH / 2
        target_y = snake.segments.sprites()[0].rect.centery - SCREEN_HEIGHT / 2

        # Interpolar entre la posición actual de la cámara y el objetivo
        # El factor de lerp determina qué tan "suave" o "rápido" es el movimiento de la cámara
        # Un valor más bajo resultará en un movimiento más suave
        lerp_factor = 0.1
        new_camera_x = self.camera_offset.x + (target_x - self.camera_offset.x) * lerp_factor
        new_camera_y = self.camera_offset.y + (target_y - self.camera_offset.y) * lerp_factor
        # Actualizar la posición de la cámara
        return Vector2(new_camera_x, new_camera_y)

class MoveByBlocks(FollowStrategy):
    def get_offset(self, snake):
        # Estrategia para que la camara se mueva por bloques
        # Obtener la posición del centro de la cabeza de la serpiente
        snake_head_position = snake.segments.sprites()[0].rect.center

        # Calcular en qué "bloque" de la cámara está basado en la posición de la cabeza de la serpiente
        block_x = int(snake_head_position[0] // SCREEN_WIDTH)
        block_y = int(snake_head_position[1] // SCREEN_HEIGHT)

        # Calcular el desplazamiento de la cámara para centrar ese bloque
        camera_x = block_x * SCREEN_WIDTH
        camera_y = block_y * SCREEN_HEIGHT

        return Vector2(camera_x, camera_y)