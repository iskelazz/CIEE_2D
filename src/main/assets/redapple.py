import pygame

RED = (255, 0, 0)
FRUIT_SIZE = 20

class RedApple():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def effect(self, snake):
        # Implementa el efecto de la fruta roja en la serpiente
        snake.grow()  # Aumenta la longitud de la serpiente

    def update(self):
        # Implementa la lógica de actualización de la fruta si es necesario
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, FRUIT_SIZE, FRUIT_SIZE))