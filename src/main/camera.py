import pygame
from pygame.math import Vector2
from config import Config

class Camera:
    def __init__(self, follow_strategy):
        self.offset = Vector2(0, 0)
        self.follow_strategy = follow_strategy

    def update(self, target):
        self.offset = self.follow_strategy.get_offset(target, self.offset)

class FollowStrategy:
    def get_offset(self, target):
        raise NotImplementedError
#Patron estrategia para decidir como se va mover la camara
class FollowSnake(FollowStrategy):
    def get_offset(self, snake, offset):
        # Coordenadas objetivo basadas en la posición de la cabeza de la serpiente
        target_x = snake.segments.sprites()[0].rect.centerx - Config.SCREEN_WIDTH / 2
        target_y = snake.segments.sprites()[0].rect.centery - Config.SCREEN_HEIGHT / 2

        # Interpolar entre la posición actual de la cámara y el objetivo
        # El factor de lerp determina qué tan "suave" o "rápido" es el movimiento de la cámara
        # Un valor más bajo resultará en un movimiento más suave
        lerp_factor = 0.1
        new_camera_x = offset.x + (target_x - offset.x) * lerp_factor
        new_camera_y = offset.y + (target_y - offset.y) * lerp_factor
        # Actualizar la posición de la cámara
        return Vector2(new_camera_x, new_camera_y)

class MoveByBlocks(FollowStrategy):
    def get_offset(self, snake, offset):
        # Estrategia para que la camara se mueva por bloques
        # Obtener la posición del centro de la cabeza de la serpiente
        snake_head_position = snake.segments.sprites()[0].rect.center

        # Calcular en qué "bloque" de la cámara está basado en la posición de la cabeza de la serpiente
        block_x = int(snake_head_position[0] // Config.SCREEN_WIDTH)
        block_y = int(snake_head_position[1] // Config.SCREEN_HEIGHT)

        # Calcular el desplazamiento de la cámara para centrar ese bloque
        camera_x = block_x * Config.SCREEN_WIDTH
        camera_y = block_y * Config.SCREEN_HEIGHT

        return Vector2(camera_x, camera_y)