from assets.staticObjects.StaticGameObject import StaticGameObject
import pygame
import os
from config import Config

class Pit(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)
        self.fall_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'pit_fall.mp3'))
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager, full_body_contact, snake_state, explosion):
        if full_body_contact:
            screen_manager.push_state('GAME_OVER')
            self.fall_sound.play()
        else: pass

    def occupied_positions(self): 
        return self.position