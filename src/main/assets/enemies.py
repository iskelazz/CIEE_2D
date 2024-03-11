import pygame, os
from pygame.sprite import Sprite
from pygame.math import Vector2
from config import GRAPHICS_DIR
from resources.gestorRecursos import GestorRecursos

cell_size = 40
cell_number = 20

class Enemie(Sprite):
    
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 4
    
    def __init__(self, x, y,imageFile, coordFile, numImages):
        super().__init__()
        self.x = x*cell_size
        self.y = y*cell_size
        

        self.image = None
        self.sheet = GestorRecursos.CargarImagen(imageFile,-1)
        self.sheet = self.sheet.convert_alpha()
        data = GestorRecursos.CargarArchivoCoordenadas(coordFile)
        data = data.split()
        self.spriteNum = 0
        cont = 0
        self.spriteList = []
        for postura in range(1, numImages+1):
            self.spriteList.append(pygame.Rect((int(data[cont]), int(data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
            cont += 4
        self.animDelay = 5
        self.animTime = 0
        self.rect = pygame.Rect(self.x,self.y,self.spriteList[self.spriteNum][2],self.spriteList[self.spriteNum][3])
        self.updateAnim()

    def updateAnim(self):
        self.animTime -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.animTime < 0):
            self.animTime = self.animDelay
            # Si ha pasado, actualizamos la postura
            self.spriteNum += 1
            if self.spriteNum >= len(self.spriteList):
                self.spriteNum = 0
            if self.spriteNum < 0:
                self.spriteNum = len(self.spriteList)-1
            self.image = self.sheet.subsurface(self.spriteList[self.spriteNum])

     
    def update(self):
        self.updateAnim()
        
                
            
    def draw(self, screen, camera_offset):
        adjusted_position = (self.rect.x - camera_offset.x, 
                            self.rect.y - camera_offset.y)
        
        screen.blit(self.image, adjusted_position)
        
        
class Murcielago(Enemie):
    def __init__(self, x, y, speed):

        fullpath = [(8, 'right'), (8, 'down'), (8, 'left'), (8, 'up')]
        self.speed = speed
        self.velx = 0
        self.vely = 0
        #self.rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
        

        self.fullpath = fullpath
        self.path_cont = 0
        self.path = fullpath[0]
        self.plenght = (self.path[0] - 1) * cell_size
        self.direction = self.path[1]
        self.animation_cont = 0

        super().__init__(x, y,'bat.png','batCoord.txt',5)
       
    def update_path(self): 
        self.path_cont += 1
        path_index = (self.path_cont % len(self.fullpath))
        self.path = self.fullpath[path_index]
        self.plenght = (self.path[0] - 1) * cell_size
        self.direction = self.path[1]
    
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
     

    def handle_collision(self,segment,snake,game):
        snake.reduce_body()
        game.score.trap_collision()
        if len(snake.body) < 1 or game.score.score < 0:
            game.screen_manager.change_state('GAME_OVER') 

    def update(self):
        super().update()
        self.move(self.velx, self.vely)
         
        
    
    
        
        
        
        
        
   
                
            
        
        