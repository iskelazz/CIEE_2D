from assets.staticObjects.StaticGameObject import StaticGameObject
import pygame

class Fence(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager,tail_collide, explosion):
        screen_manager.change_state('GAME_OVER')

    def occupied_positions(self): 
        return self.position