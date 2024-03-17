from pygame.sprite import Sprite
from config import Config

class StaticGameObject(Sprite):
    def __init__(self, sprite, position):
        super().__init__()
        self.image = sprite
        self.position = position
        self.rect = self.image.get_rect(topleft=(position[0] * Config.CELL_SIZE, position[1] * Config.CELL_SIZE))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        pass  

    def handle_collision(self, screen_manager, tail_collide, snake_state, explosion):
        pass

    def occupied_positions(self): 
        pass