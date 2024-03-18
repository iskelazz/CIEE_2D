import pygame,os
from assets.staticObjects.StaticGameObject import StaticGameObject
from animations.explosion import Explosion
from assets.snake.fastState import FastState
from config import Config
class BreakableFence(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)
        self.collision_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'stone_break.wav'))
    
    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager, tail_collide, snake_state, explosion):
        if isinstance(snake_state, FastState):
            position_in_pixels = self.rect.center
            new_explosion = Explosion(position_in_pixels)
            explosion.add(new_explosion)
            self.kill()
            self.collision_sound.play()
        else:
            screen_manager.push_state('GAME_OVER')

    def occupied_positions(self): 
        return self.position