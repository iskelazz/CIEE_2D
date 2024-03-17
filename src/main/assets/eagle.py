import pygame, os

import random
from config import Config
from assets.floorTraps import FireTrap
from assets.enemies import Enemy

cell_size = 40
cell_number = 20

class Eagle(Enemy):
    def __init__(self):
        
        super().__init__(5, 30, 'eagle.png', 'eagleCoord.txt', [10, 6, 5],3)    
        self.last_attack_time=0
        self.flying=False
        self.attacking=False
        
        self.fly_prep_time=60

        self.feather_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'feather_swoosh.mp3'))
        self.eagle_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'eagle_sound.wav'))
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

class Feather(Enemy):
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
   