from assets.staticObjects.StaticGameObject import StaticGameObject
from animations.explosion import Explosion
from config import CELL_SIZE

class BreakableFence(StaticGameObject):
    def __init__(self, sprite, position):
        super().__init__(sprite, position)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        pass  

    def handle_collision(self, screen_manager,tail_collide,explosion):
        position_in_pixels = self.rect.center
        new_explosion = Explosion(position_in_pixels)
        explosion.add(new_explosion)
        self.kill()

    def occupied_positions(self): 
        return self.position