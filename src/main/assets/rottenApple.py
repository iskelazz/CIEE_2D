import os
from config import GRAPHICS_DIR
from assets.apple import Apple 
from phases.AreaManager import AreaManager

class RottenApple(Apple):
    def __init__(self, staticPositions):
        super().__init__(os.path.join(GRAPHICS_DIR, 'apple_rotten.png'), staticPositions)
    
    def handle_collision(self,segment,snake,game):
        if len(snake.body) <= 1 or game.score.score < 0:
                game.screen_manager.push_state('GAME_OVER') 
        else:
            area_manager = AreaManager()
            self.randomize(snake.body,area_manager.coords(area_manager.get_area_tag_by_object(self)))
            snake.reduce_body()
            game.score.eat_rotten_apple() 
            snake.rotten_apple_sound.play()