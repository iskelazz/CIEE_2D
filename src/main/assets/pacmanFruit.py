from assets.consumable import Consumable 
from assets.snake.pacmanState import PacmanState

from config import CELL_SIZE

 
class PacmanFruit(Consumable):
    def __init__(self, x,y):
        super().__init__('cherry.png')
        self.rect.x=x*CELL_SIZE
        self.rect.y=y*CELL_SIZE
    
    def handle_collision(self,segment,snake,game):
        self.kill()
        snake.set_state(PacmanState(snake))
