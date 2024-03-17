import pygame, os

import random
from pygame.sprite import Sprite
from pygame.math import Vector2
from config import GRAPHICS_DIR, SOUNDS_DIR
from resources.gestorRecursos import GestorRecursos
from assets.snake.pacmanState import PacmanState
import time
from assets.floorTraps import FireTrap

from config import SOUNDS_DIR

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
        self.current_time=0
        self.hit_cooldown=0.2
        self.hit_timer=0

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
            
    def invert_direction(self, direction):
        aux = None
        if (direction == 'down'): 
            aux = 'up'
        elif (direction == 'up'):
            aux = 'down'
        elif (direction == 'left'):
            aux = 'right'
        elif (direction == 'right'):
            aux = 'left'  
        return aux
        
    def update(self):
        self.current_time=pygame.time.get_ticks() / 1000.0  # Obtén el tiempo actual en segundos
        self.updateAnim(self.scale)
        
                 
    def draw(self, screen, camera_offset):
        adjusted_position = (self.rect.x - camera_offset.x, 
                            self.rect.y - camera_offset.y)
        
        screen.blit(self.image, adjusted_position)
    def handle_collision(self,segment,snake,game):
        self.current_time=pygame.time.get_ticks() / 1000.0    
        if self.current_time - self.hit_timer > self.hit_cooldown:
            self.hit_timer=self.current_time
            snake.reduce_body()
            game.score.trap_collision()
            if len(snake.body) <= 1 or game.score.score < 0:
                game.screen_manager.push_state('GAME_OVER') 
        
class Murcielago(Enemie):
    def __init__(self, x, y, path_right, path_down, path_left, path_up, speed, open):

        fullpath = [(path_right, 'right'), (path_down, 'down'), (path_left, 'left'), (path_up, 'up')]
        self.speed = speed
        self.velx = 0
        self.vely = 0
        self.invert = False
        self.open = open
        
        self.dead=False
        #self.rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
        

        self.fullpath = fullpath
        self.path_cont = 0
        self.path = fullpath[0]
        self.plenght = (self.path[0] - 1) * cell_size
        self.direction = self.path[1]
        self.animation_cont = 0
        
        self.bat_sound_1 = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'enemy_bat_sound.wav'))
        self.bat_sound_2 = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'enemy_bat_sound_2.wav'))
        self.bat_sound_3 = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'enemy_bat_sound_3.wav'))

        self.bat_sounds_group = [self.bat_sound_1, self.bat_sound_2, self.bat_sound_3]
        self.bat_sound_selected = self.bat_sounds_group[random.randint(0,2)]
        
        pygame.mixer.Sound.set_volume(self.bat_sound_selected, 0.6)

        self.bat_sound_selected.play(-1)

        super().__init__(x, y,'bat.png','batCoord.txt',[5])
        
    def update_path(self):
        if (self.open == False):
            self.path_cont += 1
            path_index = (self.path_cont % len(self.fullpath))
            self.path = self.fullpath[path_index]
            self.plenght = (self.path[0] - 1) * cell_size
            self.direction = self.path[1]
            
        else:
            if (self.invert==False):
                self.path_cont += 1
                path_index = (self.path_cont % len(self.fullpath))
                self.path = self.fullpath[path_index]
                self.plenght = (self.path[0] - 1) * cell_size
                self.direction = self.path[1]
                if (path_index == len(self.fullpath)-1): self.invert = True
            else:
                path_index = (self.path_cont % len(self.fullpath))
                self.path = self.fullpath[path_index]
                self.plenght = (self.path[0] - 1) * cell_size
                self.direction = self.invert_direction(self.path[1])
                self.path_cont -= 1
                if (path_index == 0): self.invert = False
                         
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
            snake.bat_kill_sound.play()
            game.score.eat_red_apple()
            self.kill()
            self.dead=True
        else:
            snake.bat_hit_sound.play()
            super().handle_collision(segment,snake,game)

    def update(self):
        if self.dead==False:
            super().update()
            self.move(self.velx, self.vely)
    
    def draw(self,screen,offset):
        if self.dead==False:
            super().draw(screen,offset)
    
class Eagle(Enemie):
    def __init__(self):
        
        super().__init__(5, 30, 'eagle.png', 'eagleCoord.txt', [10, 6, 5],3)    
        self.last_attack_time=0
        self.flying=False
        self.attacking=False
        
        self.fly_prep_time=60

        self.feather_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'feather_swoosh.mp3'))
        self.eagle_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'eagle_sound.wav'))
        self.eagle_sound.play(-1)

    def update(self,snake,current_time,enemy_group,trap_group):
        super().update()
        if self.flying==False:
            #comprueba el cooldown entre ataques
            if current_time-self.last_attack_time>random.randint(5,15):
                self.last_attack_time=current_time
                #elige entre los tres posibles ataques dependiendo de la cantidad de huevos recogidos
                attack=random.randint(0,snake.retrieved_eggs)
                if attack==0:
                    self.feather_attack(snake,enemy_group)
                elif attack==1:
                    self.trap_attack(snake,trap_group)
                elif attack==2 :
                    self.flying=True
                    self.animationNum=1
                    self.attacking=True
                #cuando tiene todos los huevos usa los tres ataques a la vez
                else:
                    self.feather_attack(snake)
                    self.trap_attack(snake,trap_group)
                    if random.randint(1,3)==3:
                        self.flying=True
                        self.animationNum=1
                        self.attacking=True
        #ataque volador
        else:
            #cambia de animacion y se pone a la altura de la serpiente
            if self.fly_prep_time>30:
                if (snake.body[0][1]-1)*cell_size<self.rect.y and (snake.body[0][1]+1)*cell_size>self.rect.y:
                    yStep=0
                else:
                    if (snake.body[0][1]-2)*cell_size>self.rect.y:
                        yStep=25
                    else: yStep=-25         
                self.fly_prep_time-=1
                self.move(0,yStep)
            #se mantiene a esa altura un momento, para dar margen
            elif self.fly_prep_time>0:
                self.fly_prep_time-=1
            #vuela en linea recta por todo el mapa y regresa a su sitio inicial
            else :
                self.animationNum=2
                self.move(20,0)
                if self.rect.x>80:
                    self.fly_prep_time=30
                    self.animationNum=0
                    self.rect.x=5*cell_size
                    self.rect.y=30*cell_size
                    self.flying=False
                    self.last_attack_time=current_time
                    self.attacking=False

    def move(self,xStep,yStep):
        self.rect.x+=xStep
        self.rect.y+=yStep
        
        

    def trap_attack(self,snake,trap_group):
        snake.wooden_trap_sound.play()
        trampa=FireTrap(snake.body[0]+snake.direction*5)
        trap_group.add(trampa)
    
    def feather_attack(self,snake,enemy_group):
        self.feather_sound.play()
        pluma=Feather(self.rect.x,self.rect.y,snake,6)
        enemy_group.add(pluma)


    def handle_collision(self,snake,game):
        if self.attacking==True:
            super().handle_collision(None,snake,game)  
        else :game.screen_manager.change_state('START')


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
        super().handle_collision(segment,snake,game)
   
                
            
        
        