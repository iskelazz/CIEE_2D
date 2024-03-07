import pygame, os
from pygame.sprite import Sprite
from config import GRAPHICS_DIR
from pygame.math import Vector2

cell_size = 40
cell_number = 20

class FloorTrap(Sprite):
    
    ANIMATION_DELAY = 9
    
    def __init__(self, spriteSheet, position, widht, height):
        super().__init__()
        self.sprites = self.cargar_sprite_sheets(spriteSheet, widht, height)
        self.image = self.sprites[0]
        self.rect = self.rect = pygame.Rect(position.x*cell_size, position.y*cell_size, cell_size, cell_size)
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
       
        
    def cargar_sprite_sheets(self, name, width, height):
        
        fullname = os.path.join(GRAPHICS_DIR, name)
        sprite_sheet= pygame.image.load(fullname).convert_alpha()
        
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i*width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale(surface, (cell_size, cell_size))) 
            
        return sprites
    
    def animate_trap(self):
        sprites = self.sprites
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]        
        self.animation_count += 1
        
        self.mask = pygame.mask.from_surface(self.image)
        
        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0
            
    def draw(self, win, camera_offset):
        
        adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
        win.blit(self.image, adjusted_position)
        
    def is_on(self):
        
        if (self.image == self.sprites[7] or self.image == self.sprites[8] or self.image == self.sprites[9]):
            print('ON')
            return True
        else:
            print('OFF')
            return False
            
   
    
class FireTrap(FloorTrap):
    def __init__(self, position):
        super().__init__('Fire_Trap.png', position, 32, 40)
        
class SpikeTrap(FloorTrap):
    def __init__(self, position):
        super().__init__('Spike_Trap.png', position, 32, 32)
        
        
    
    
        
        
     
     

     
    
     
       
     
  