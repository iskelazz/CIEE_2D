import pygame, os
from pygame.sprite import Sprite
from pygame.math import Vector2
from assets.trackPiece import TrackPiece
from config import GRAPHICS_DIR
cell_size = 40
cell_number = 20

class SawTrap(Sprite):
    COLOR = (255, 0, 0)
    VEL = 2
    ANIMATION_DELAY = 5
    
    def __init__(self, x, y, lenght, orientation):
        super().__init__()
        self.x = x*cell_size
        self.y = y*cell_size
        self.velx = 0
        self.vely = 0
        self.lenght = (lenght-1)*cell_size
        self.orientation = orientation
        
        self.rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
        self.sprites = self.load_images()
        self.image = self.sprites[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_cont = 0
        
        if orientation == 'horizontal':
            self.direction = 'right'
        elif orientation == 'vertical':
            self.direction = 'down'
            
        self.trackPiece = TrackPiece.create_pieces(x, y, lenght, orientation)
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        
    def move_left(self, vel):
        self.velx = -vel
        if self.direction != 'left':
            self.direction == 'left'
            self.animation_cont = 0
        
    def move_right(self, vel):
        self.velx = vel
        if self.direction != 'right':
            self.direction == 'right'
            self.animation_cont = 0
            
    def move_up(self, vel):
        self.vely = -vel
        if self.direction != 'up':
            self.direction == 'up'
            self.animation_cont = 0
            
    def move_down(self, vel):
        self.vely = vel
        if self.direction != 'down':
            self.direction == 'down'
            self.animation_cont = 0
            
    def animate_saw(self):
        self.move(self.velx, self.vely)
        sprites = self.sprites
        sprite_index = (self.animation_cont // self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]      
        self.animation_cont += 1
        
        self.mask = pygame.mask.from_surface(self.image)
        
        if self.animation_cont // self.ANIMATION_DELAY > len(sprites):
            self.animation_cont = 0
        
    def handle_move(self):
        
        if self.orientation == 'horizontal':
            
            if self.direction == 'right':
                self.move_right(self.VEL)
                if self.rect.x == self.x + self.lenght: self.direction = 'left'     
            elif self.direction == 'left':
                self.move_left(self.VEL)
                if self.rect.x == self.x : self.direction = 'right'        
        
        elif self.orientation == 'vertical':
            
            if self.direction == 'up':
                self.move_up(self.VEL)
            elif self.direction == 'down':
                self.move_down(self.VEL)
                
            if self.rect.y >= self.y + self.lenght: self.direction = 'up'
            if self.rect.y <= self.y : self.direction = 'down'
            
    def load_images(self):
       
       
        images = [
            pygame.image.load(os.path.join(GRAPHICS_DIR, 'rotating_saw_01.png')).convert_alpha(),
            pygame.image.load(os.path.join(GRAPHICS_DIR, 'rotating_saw_02.png')).convert_alpha(),
            pygame.image.load(os.path.join(GRAPHICS_DIR, 'rotating_saw_03.png')).convert_alpha(),
            pygame.image.load(os.path.join(GRAPHICS_DIR, 'rotating_saw_04.png')).convert_alpha(),
            pygame.image.load(os.path.join(GRAPHICS_DIR, 'rotating_saw_05.png')).convert_alpha(),
        ]
        
        saw_images = []
        
        for image in images:
            image = pygame.transform.scale(image, (cell_size, cell_size))
            if self.orientation == 'vertical':
                saw_images.append(pygame.transform.rotate(image, 270))
            elif self.orientation == 'horizontal':
                saw_images.append(image)       
                
        return saw_images
    
    def get_coordinates(self):
        coordinates = Vector2(self.rect.x, self.rect.y)
        return coordinates
            
    def draw(self, win, camera_offset):
        self.trackPiece.draw(win, camera_offset)
        adjusted_position = (self.rect.x - camera_offset.x, 
                             self.rect.y - camera_offset.y)
        win.blit(self.image, adjusted_position)
        
        
        
             
            
        

        
        
    
        
        