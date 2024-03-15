from assets.staticObjects.StaticGameObject import StaticGameObject
import pygame
cell_size = 40
cell_number = 20
#objeto estatico para el cambio de nivel
class HoleStatic(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager, tail_collide, snake_state, explosion):
        screen_manager.current_state().next_level()

    def occupied_positions(self): 
        return self.position