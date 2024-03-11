from phases.AreaManager import AreaManager
import random
import os
from assets.consumable import Consumable 
from config import GRAPHICS_DIR, CELL_SIZE

cell_number = 20 #temporal
 
class Apple(Consumable):
    def __init__(self,image_path, staticPositions):
        super().__init__(image_path)
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

    def handle_collision(self,segment,snake,game):
        area_manager = AreaManager()
        self.randomize(snake.body,area_manager.coords(area_manager.get_area_tag_by_object(self)))
        snake.add_block()
        game.score.eat_red_apple()