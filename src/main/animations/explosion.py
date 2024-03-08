import pygame
import os
from config import GRAPHICS_DIR
 
explosion_path = os.path.join(GRAPHICS_DIR, 'explosion_sprite')

class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.images = []
        self.load_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=position)
        self.animation_speed = 0.2  # Ajusta este valor según necesites
        self.current_frame = 0

    def load_images(self):
        for i in range(1, 6):  # Asume que tienes 5 imágenes
            self.images = [pygame.image.load(os.path.join(explosion_path, f'expl_0{i}.png')).convert_alpha() for i in range(1, 6)]

    def update(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.images):
            self.kill()  # Elimina la explosión una vez que la animación ha terminado
        else:
            self.index = int(self.current_frame)
            self.image = self.images[self.index]
        

    def draw(self, screen, camera_offset):
        adjusted_position = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        screen.blit(self.image, adjusted_position)