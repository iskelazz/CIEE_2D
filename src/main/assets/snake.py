import pygame

FRUIT_SIZE = 20
GREEN = (0, 255, 0)

class Snake:

    def __init__(self, x, y):
        self.body = [(x, y)]
        self.length = 1
        self.direction = "RIGHT"
        self.change_to = self.direction

    def move(self):
        # Obtener la cabeza de la serpiente
        head = self.body[0]

        # Determinar la dirección del movimiento basada en el cambio solicitado
        if self.change_to == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        if self.change_to == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        if self.change_to == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        if self.change_to == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

        # Movimiento de la cabeza de la serpiente
        if self.direction == "UP":
            new_head = (head[0], head[1] - 10)
        if self.direction == "DOWN":
            new_head = (head[0], head[1] + 10)
        if self.direction == "LEFT":
            new_head = (head[0] - 10, head[1])
        if self.direction == "RIGHT":
            new_head = (head[0] + 10, head[1])

        # Agregar nueva cabeza a la serpiente
        self.body.insert(0, new_head)

        # Eliminar la cola si no ha crecido
        if len(self.body) > self.length:
            self.body.pop()

    def change_direction(self, direction):
        self.change_to = direction

    def grow(self):
        self.length += 1

    def effect(self, fruit):
        fruit.effect(self)

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, FRUIT_SIZE, FRUIT_SIZE))