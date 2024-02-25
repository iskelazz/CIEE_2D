import random
from assets.redapple import RedApple

class Screen1fruits:

    def __init__(self, screen_width, screen_height):
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fruits = []
        # Agregar frutas a la pantalla
        self.spawn_fruits()

    def spawn_fruits(self):
        for _ in range(5):  # Generar 5 frutas inicialmente aleatorias
            x = random.randint(0,  self.screen_width - 10)
            y = random.randint(0, self.screen_height - 10)
            fruit = RedApple(x, y)
            self.fruits.append(fruit)

    def update(self):
        # Actualizar la lógica de las frutas en la pantalla
        for fruit in self.fruits:
            fruit.update()

    def render(self, screen):
        # Renderizar las frutas en la pantalla
        for fruit in self.fruits:
            fruit.draw(screen)