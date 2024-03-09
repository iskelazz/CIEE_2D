import pygame, os
from pygame.sprite import Sprite
from pygame.math import Vector2
from config import GRAPHICS_DIR
cell_size = 40
cell_number = 20

class Enemie(Sprite):
    
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 5
    
    def __init__(self, x, y, speed, fullpath):
        
        self.x = x*cell_size
        self.y = y*cell_size
        self.speed = speed
        self.velx = 0
        self.vely = 0
        self.rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
        
        self.fullpath = fullpath
        self.path_cont = 0
        self.path = fullpath[0]
        self.plenght = (self.path[0] - 1) * cell_size
        self.direction = self.path[1]
        
        self.sprites = None
        self.image = None
        self.animation_cont = 0
        
    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

        
    def move_left(self, vel):
        self.vely = 0
        self.velx = -vel
        if self.direction != 'left':
            self.direction == 'left'
            self.animation_cont = 0
        
    def move_right(self, vel):
        self.vely = 0
        self.velx = vel
        if self.direction != 'right':
            self.direction == 'right'
            self.animation_cont = 0
            
    def move_up(self, vel):
        self.velx = 0
        self.vely = -vel
        if self.direction != 'up':
            self.direction == 'up'
            self.animation_cont = 0
            
    def move_down(self, vel):
        self.velx = 0
        self.vely = vel
        if self.direction != 'down':
            self.direction == 'down'
            self.animation_cont = 0     
     
    def update(self):
        self.move(self.velx, self.vely)
        
    def update_path(self):
        return 0
        
    def handle_move(self):
        if self.direction == 'right':
            self.move_right(self.speed)
            if self.rect.x >= self.x + self.plenght: 
                self.x += self.plenght
                self.update_path()
                
        elif self.direction == 'left':
            self.move_left(self.speed)
            if self.rect.x <= self.x - self.plenght: 
                self.x -= self.plenght
                self.update_path()
                
        
        elif self.direction == 'up':
            self.move_up(self.speed)
            if self.rect.y <= self.y - self.plenght: 
                self.y -= self.plenght
                self.update_path()
                      
        
        elif self.direction == 'down':
            self.move_down(self.speed)
            if self.rect.y >= self.y + self.plenght: 
                self.y += self.plenght
                self.update_path()
                     
            
    def draw(self, screen, camera_offset):
        adjusted_position = (self.rect.x - camera_offset.x, 
                            self.rect.y - camera_offset.y)
        adjusted_rect=self.rect.copy()
        adjusted_rect.x=adjusted_position[0]
        adjusted_rect.y=adjusted_position[1]
        
        pygame.draw.rect(screen, self.COLOR, adjusted_rect)
        
        
class Murcielago(Enemie):
    def __init__(self, x, y, speed):
        fullpath = [(8, 'right'), (8, 'down'), (8, 'left'), (8, 'up')]
        super().__init__(x, y, speed, fullpath)
       
    def update_path(self): 
        self.path_cont += 1
        path_index = (self.path_cont % len(self.fullpath))
        self.path = self.fullpath[path_index]
        self.plenght = (self.path[0] - 1) * cell_size
        self.direction = self.path[1]
    
    
        
        
        
        
        
   
                
            
        
        