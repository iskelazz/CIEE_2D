from assets.staticObjects.StaticGameObject import StaticGameObject
import pygame
import os
from config import Config

class Fence(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)
        self.collision_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'collision.wav'))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager, tail_collide, snake_state, explosion):
        screen_manager.push_state('GAME_OVER')
        self.collision_sound.play()

    def occupied_positions(self): 
        return self.position