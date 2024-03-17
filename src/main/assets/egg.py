from phases.AreaManager import AreaManager
from assets.consumable import Consumable 
from config import Config

cell_number = 20 #temporal
 
class Egg(Consumable):
    def __init__(self, x, y):
        super().__init__('egg.png')
        self.rect.x = x * Config.CELL_SIZE
        self.rect.y = y * Config.CELL_SIZE
    

    def handle_collision(self,segment,snake,game):
        area_manager = AreaManager()
        snake.retrieved_eggs +=1
        self.kill()