import pygame
import time
from pygame.math import Vector2
from state.PlayingState import PlayingState
from assets.redapple import RedApple
from phases.Area import Area
from phases.AreaManager import AreaManager
from config import Config
from assets.floorTraps import WoodTrap
from assets.sawTrap import SawTrap
from camera import Camera, MoveByBlocks
from assets.door import Door
from assets.key import Key
import os

"""Se definen coordenadas del mapa(En celdas de tablero) que definen un area y una clase areaManager para evaluar de forma rapida el estado de diferentes objetos en ellas"""
areas_dict = {
    "AREA1": Area("AREA1", 1, 1, 19, 19),
    "AREA2": Area("AREA2", 21, 1, 8, 19),
    "AREA3": Area("AREA3", 44, 1, 15, 19),
    "AREA4": Area("AREA4", 61, 6, 17, 13)
    #añadir mas areas si es necesario
}
class PlayingState1(PlayingState):
    def __init__(self, game):
        super().__init__(game)
        # Cargar nivel
        self.load_level(os.path.join(Config.LEVEL_DIR, 'level1.json'))
        
        #inicializar camara
        self.camera = Camera(MoveByBlocks())
        
        # Division de la fase en areas
        area_manager = AreaManager()
        area_manager.load_areas(areas_dict)

        self.initialize_snake((8, 10)) #Creacion de la serpiente con la posicion de su cabeza pasada por parametro  
        
        #Inicializacion de trampas y enemigos
        self.floor_trap_group = self.init_wood_traps()
        self.saw_trap_group = self.init_saw_traps()

        #Puerta de salida de la fase
        self.door=Door(75*Config.CELL_SIZE,0*Config.CELL_SIZE,False)
        self.door2=Door(76*Config.CELL_SIZE,0*Config.CELL_SIZE,False)
        self.door3=Door(77*Config.CELL_SIZE,0*Config.CELL_SIZE,False)
        self.door4=Door(78*Config.CELL_SIZE,0*Config.CELL_SIZE,False)
        self.key=Key(69 * Config.CELL_SIZE,15 * Config.CELL_SIZE,[self.door,self.door2,self.door3,self.door4])
        self.key_group=pygame.sprite.Group(self.key)
        self.door_group=pygame.sprite.Group(self.door,self.door2,self.door3,self.door4)


        #Lista con grupos de sprites
        self.group_list=(self.rotten_apple_group, self.apple_group, self.key_group, self.door_group, self.explosions_group, self.floor_trap_group, self.saw_trap_group)
        
        self.level_size = (self.level_manager.cell_number_x * Config.CELL_SIZE, self.level_manager.cell_number_y * Config.CELL_SIZE)
        
        self.init_apples(area_manager)

        #Musica del nivel
        self.background_music = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'level_1_theme.mp3'))
        self.background_music.play(-1)

    def init_wood_traps(self):
        #Trampas de la pantalla 3
        self.woodTrap = WoodTrap(Vector2(50, 5))
        self.woodTrap2 = WoodTrap(Vector2(49, 6))
        self.woodTrap3 = WoodTrap(Vector2(51, 6))
        self.woodTrap4 = WoodTrap(Vector2(50, 7))
        self.woodTrap5 = WoodTrap(Vector2(50, 10))
        self.woodTrap6 = WoodTrap(Vector2(49, 11))
        self.woodTrap7 = WoodTrap(Vector2(51, 11))
        self.woodTrap8 = WoodTrap(Vector2(50, 12))

        #Trampas de la pantalla 4
        self.woodTrap9 = WoodTrap(Vector2(66, 1))
        self.woodTrap10 = WoodTrap(Vector2(66, 2))
        self.woodTrap11 = WoodTrap(Vector2(66, 3))
        self.woodTrap12 = WoodTrap(Vector2(67, 1))
        self.woodTrap13 = WoodTrap(Vector2(67, 3))
        self.woodTrap14 = WoodTrap(Vector2(68, 2))
        self.woodTrap15 = WoodTrap(Vector2(66, 15))
        self.woodTrap16 = WoodTrap(Vector2(67, 14))
        self.woodTrap17 = WoodTrap(Vector2(68, 13))
        self.woodTrap18 = WoodTrap(Vector2(69, 12))
        self.woodTrap19 = WoodTrap(Vector2(70, 13))
        self.woodTrap20 = WoodTrap(Vector2(71, 14))
        self.woodTrap21 = WoodTrap(Vector2(72, 15))

        return pygame.sprite.Group(self.woodTrap, self.woodTrap2,self.woodTrap3, self.woodTrap4, self.woodTrap5, self.woodTrap6, self.woodTrap7, self.woodTrap8,
                                   self.woodTrap9, self.woodTrap10,self.woodTrap11, self.woodTrap12, self.woodTrap13, self.woodTrap14, self.woodTrap15, self.woodTrap16,
                                   self.woodTrap17, self.woodTrap18,self.woodTrap19, self.woodTrap20, self.woodTrap21)

    def init_saw_traps(self):
        #Trampas pantalla 3
        self.sawTrap = SawTrap(43, 11, 2, 'vertical')
        self.sawTrap2 = SawTrap(43, 4, 3, 'vertical')
        self.sawTrap3 = SawTrap(44, 9, 12, 'horizontal')

        #Trampas pantalla 4
        self.sawTrap4 = SawTrap(73, 13, 5, 'horizontal')
        self.sawTrap5 = SawTrap(65, 8, 6, 'vertical')
        self.sawTrap6 = SawTrap(63, 7, 13, 'horizontal')

        return pygame.sprite.Group(self.sawTrap, self.sawTrap2, self.sawTrap3, self.sawTrap4, self.sawTrap5,  self.sawTrap6)
    
    
    def init_apples(self, area_manager):
        "Inicializado de las manzanas según el diseño establecido para el nivel"
        #Definimos las areas donde queremos inicializar manzanas
        AREA1 = area_manager.coords("AREA1")
        AREA2 = area_manager.coords("AREA2")
        AREA3 = area_manager.coords("AREA3")
        AREA4 = area_manager.coords("AREA4")

        #Una fruta buena y una mala por area
        self.fruit_sorting(AREA1, 1, RedApple)
        self.fruit_sorting(AREA2, 1, RedApple)
        self.fruit_sorting(AREA3, 1, RedApple)
        self.fruit_sorting(AREA4, 1, RedApple)

    def update(self):
        """Actualiza el estado de los objetos"""
        current_time = time.time()
        self.snake.update(current_time)
        self.check_collisions()
        # Comprueba las Areas a las que llega la serpiente
        self.check_area_activation(current_time)
        # Generar rotten apples en todas las áreas activas
        self.generate_rotten_apple(current_time)
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.push_state('GAME_OVER')
        self.camera.update(self.snake)
        self.explosions_group.update()
        for woodTrap in self.floor_trap_group:
            woodTrap.animate_trap()

        for sawTrap in self.saw_trap_group:
            sawTrap.animate_saw()
            sawTrap.handle_move()

    def draw(self, screen):
        """Dibuja todos los elementos del juego en la pantalla."""
        screen.fill((175,215,70))
        self.level_manager.draw_level(screen, self.camera.offset)
        self.level_manager.draw_objects(screen, self.camera.offset)
        self.game.score.draw_score()
        
        for segment in self.snake.segments:
            adjusted_position = segment.rect.topleft - self.camera.offset
            screen.blit(segment.image, adjusted_position)
        
        for group in self.group_list:
            for asset in group:
                asset.draw(screen, self.camera.offset)

        for explosion in self.explosions_group:
            explosion.draw(screen, self.camera.offset)
    
    def check_collisions(self):
        """Verifica y maneja las colisiones."""
        head = self.snake.segments.sprites()[0]
        tail= self.snake.segments.sprites()[-1]
        body = pygame.sprite.Group(self.snake.segments.sprites()[1:])
        head_body = pygame.sprite.Group(head,self.snake.segments.sprites()[1:])
        
        #colisiones con assets de los grupos
        for group in self.group_list:
            collision_dict=pygame.sprite.groupcollide(head_body, group,False, False,)
            for segment,collided_asset in collision_dict.items():
                collided_asset[0].handle_collision(segment,self.snake,self.game)
         
      
        #Colision de serpiente con su cuerpo
        if pygame.sprite.spritecollideany(head, body):
            self.game.screen_manager.push_state('GAME_OVER')

        
        self.level_manager.check_collisions(self.snake, self.game.screen_manager, self.explosions_group)
    
    def next_level(self):
        """Metodo para gestionar la superacion exitosa del nivel"""
        pygame.mixer.stop()
        self.game.screen_manager.change_state('STORY2')
        self.game.screen_manager.update()

    def tag(self):
        return "PLAYING1"