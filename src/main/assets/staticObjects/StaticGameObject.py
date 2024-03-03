from pygame.sprite import Sprite

cell_size = 40
cell_number = 20

class StaticGameObject(Sprite):
    def __init__(self, sprite, position):
        super().__init__()
        self.image = sprite
        self.position = position
        self.rect = self.image.get_rect(topleft=(position[0] * cell_size, position[1] * cell_size))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def update(self):
        pass  

    def handle_collision(self, screen_manager,tail_collide):
        # Implementación base que puede ser sobreescrita
        pass

    def occupied_positions(self): 
        pass