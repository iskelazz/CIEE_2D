import pygame

from pygame.sprite import Sprite
from resources.gestorRecursos import GestorRecursos

cell_size = 40
cell_number = 20

class Enemy(Sprite):
    
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
   
                
            
        
        