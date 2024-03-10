import os
from config import GRAPHICS_DIR
from assets.consumable import Consumable 

class RottenApple(Consumable):
    def __init__(self, staticPositions):
        super().__init__(os.path.join(GRAPHICS_DIR, 'apple_rotten.png'), staticPositions)
    
    def handle_collision(self,segment,snake,game):
        if len(self.snake.body) > 1: # Asegurarse de que la serpiente no se reduzca por debajo de un tamaño mínimo
            self.randomize(snake.body)
            snake.reduce_body()
            game.score.score.eat_rotten_apple() 