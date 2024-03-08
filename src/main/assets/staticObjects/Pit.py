from assets.staticObjects.StaticGameObject import StaticGameObject
import pygame
cell_size = 40
cell_number = 20

class Pit(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager, tail_collide, snake_state, explosion):
        if tail_collide!=None:
            screen_manager.change_state('GAME_OVER')
        else: pass

    def occupied_positions(self): 
        return self.position