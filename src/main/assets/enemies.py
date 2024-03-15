import pygame, os

import random
from pygame.sprite import Sprite
from pygame.math import Vector2
from config import GRAPHICS_DIR
from resources.gestorRecursos import GestorRecursos
from assets.snake.pacmanState import PacmanState

from assets.floorTraps import SpikeTrap

cell_size = 40
cell_number = 20

class Enemie(Sprite):
    
    COLOR = (255, 0, 0)
    ANIMATION_DELAY = 4
    
    def __init__(self, x, y,imageFile, coordFile, numImages,scale=None):
        super().__init__()
        self.x = x*cell_size
        self.y = y*cell_size

        self.scale = scale
        self.image = None
        self.sheet = GestorRecursos.CargarImagen(imageFile,-1)
        self.sheet = self.sheet.convert_alpha()
        data = GestorRecursos.CargarArchivoCoordenadas(coordFile)
        data = data.split()
        
        self.animationNum = 0
        self.spriteNum = 0
        cont = 0
        self.animationList = []
        for line in range(0, len(numImages)):
            self.animationList.append([])
            tmp = self.animationList[line]
            for animation in range(1, numImages[line]+1):
                tmp.append(pygame.Rect((int(data[cont]), int(data[cont+1])), (int(data[cont+2]), int(data[cont+3]))))
                cont += 4

        self.animDelay = 5
        self.animTime = 0
        if scale:
            self.rect = pygame.Rect(self.x,self.y,self.animationList[self.animationNum][self.spriteNum][2]*self.scale,self.animationList[self.animationNum][self.spriteNum][3]*self.scale)
        else:
            self.rect = pygame.Rect(self.x,self.y,self.animationList[self.animationNum][self.spriteNum][2],self.animationList[self.animationNum][self.spriteNum][3])
        
        self.updateAnim(self.scale)

    def updateAnim(self, scale):
        self.animTime -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.animTime < 0):
            self.animTime = self.animDelay
            # Si ha pasado, actualizamos la postura
            self.spriteNum += 1
            if self.spriteNum >= len(self.animationList[self.animationNum]):
                self.spriteNum = 0
            if self.spriteNum < 0:
                self.spriteNum = len(self.animationList[self.animationNum])-1
            
            if scale:
                image = self.sheet.subsurface(self.animationList[self.animationNum][self.spriteNum])
                self.image = pygame.transform.scale_by(image, (scale, scale))
            else:self.image = self.sheet.subsurface(self.animationList[self.animationNum][self.spriteNum])
     
    def update(self):
        self.updateAnim(self.scale)
        
                
            
    def draw(self, screen, camera_offset):
        adjusted_position = (self.rect.x - camera_offset.x, 
                            self.rect.y - camera_offset.y)
        
        screen.blit(self.image, adjusted_position)
        
        
class Murcielago(Enemie):
    def __init__(self, x, y, path_right, path_down, path_left, path_up, speed):

        fullpath = [(path_right, 'right'), (path_down, 'down'), (path_left, 'left'), (path_up, 'up')]
        self.speed = speed
        self.velx = 0
        self.vely = 0
        
        self.dead=False
        #self.rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
        

        self.fullpath = fullpath
        self.path_cont = 0
        self.path = fullpath[0]
        self.plenght = (self.path[0] - 1) * cell_size
        self.direction = self.path[1]
        self.animation_cont = 0

        super().__init__(x, y,'bat.png','batCoord.txt',[5])
       
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
        if isinstance(snake.state, PacmanState):
            game.score.eat_red_apple()
            self.kill()
            self.dead=True
        else:
            snake.reduce_body()
            game.score.trap_collision()
            if len(snake.body) < 1 or game.score.score < 0:
                game.screen_manager.push_state('GAME_OVER') 

    def update(self):
        if self.dead==False:
            super().update()
            self.move(self.velx, self.vely)
    
    def draw(self,screen,offset):
        if self.dead==False:
            super().draw(screen,offset)
    
class Eagle(Enemie):
    def __init__(self):
        
        super().__init__(75, 20, 'eagle.png', 'eagleCoord.txt', [10, 6, 5],3)    
        self.last_attack_time=0
        self.flying=False
        self.attacking=False
        
        self.fly_prep_time=30
    def update(self,snake,current_time,enemy_group,trap_group):
        super().update()
        if self.flying==False:
            if current_time-self.last_attack_time>random.randint(3,10):
                self.last_attack_time=current_time
                attack=random.randint(0,snake.retrieved_eggs)
                if attack==0:
                    self.feather_attack(snake,enemy_group)
                elif attack==1:
                    self.trap_attack(snake,trap_group)
                elif attack==2 :
                    print("AY QUE VUELA AAAAAAAAAAAAAAAAAH")
                    self.flying=True
                    self.animationNum=1
                    self.attacking=True
                else:
                    self.feather_attack(snake)
                    self.fly_attack(snake)
                    if random.randint(1,3)==3:
                        print("AY QUE VUELA AAAAAAAAAAAAAAAAAH")
                        self.flying=True
                        self.animationNum=1
                        self.attacking=True
        #ataque volador
        else:
            if self.fly_prep_time>0:
                if (snake.body[0][1]-1)*cell_size<self.rect.y and (snake.body[0][1]+1)*cell_size>self.rect.y:
                    yStep=0
                else:
                    if (snake.body[0][1]-2)*cell_size>self.rect.y:
                        yStep=25
                    else: yStep=-25         
                self.fly_prep_time-=1
                self.move(0,yStep)
            else :
                self.animationNum=2
                self.move(-30,0)
                if self.rect.x<0:
                    self.fly_prep_time=30
                    self.animationNum=0
                    self.rect.x=75*cell_size
                    self.flying=False
                    self.last_attack_time=current_time
                    self.attacking=False

    def move(self,xStep,yStep):
        self.rect.x+=xStep
        self.rect.y+=yStep
        #print(self.rect.y)
        
        pass    
    def draw(self, screen, camera_offset):
        adjusted_position = (self.rect.x - camera_offset.x, 
                            self.rect.y - camera_offset.y)
        
        screen.blit(pygame.transform.flip(self.image, True, False), adjusted_position)

    def trap_attack(self,snake,trap_group):
        trampa=SpikeTrap(snake.body[0]+snake.direction*5)
        trap_group.add(trampa)
        print("TRAMPA AAAAAAAAAAAAAAAAAH")
    
    def feather_attack(self,snake,enemy_group):
        pluma=Feather(self.rect.x,self.rect.y,snake,6)
        enemy_group.add(pluma)

        print("PLUMAAAAAAA AAAAAAAAAAAAAAAAAH")

    def handle_collision(self,snake,game):
        if self.attacking==True:
            snake.reduce_body()
        else :game.screen_manager.change_state('INTRO')


class Feather(Enemie):
    def __init__(self,x,y,snake,speed=4):
        self.x=x/cell_size
        self.y=y/cell_size
        super().__init__(self.x, self.y, 'feather.png', 'feather_coord.txt', [4],3)  
        self.xMove=snake.body[0][0]*cell_size-self.x
        self.yMove=snake.body[0][1]*cell_size-self.y
        
        self.total_steps=(abs(self.xMove)+abs(self.yMove))/speed
        self.xStep=self.xMove/self.total_steps
        self.yStep=self.yMove/self.total_steps
        

    def handle_move(self):
        if self.rect.x<0 or self.rect.y<0:
            self.kill()
        self.rect.x+=self.xStep
        self.rect.y+=self.yStep
    
    def handle_collision(self,segment,snake,game):
        self.kill()
        snake.reduce_body()
   
                
            
        
        