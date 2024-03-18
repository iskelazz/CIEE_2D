import pygame, os

import random
from assets.snake.pacmanState import PacmanState
from assets.enemies import Enemy

from config import Config

cell_size = 40
cell_number = 20

class Murcielago(Enemy):
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
        
        self.bat_sound_1 = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'enemy_bat_sound.wav'))
        self.bat_sound_2 = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'enemy_bat_sound_2.wav'))
        self.bat_sound_3 = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'enemy_bat_sound_3.wav'))

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
            self.bat_sound_selected.stop()
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