import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.redapple import RedApple
from assets.rottenApple import RottenApple
from assets.snake.snake import Snake
from phases.LevelManager import LevelManager
from phases.Area import Area
from phases.AreaManager import AreaManager
from config import SOUNDS_DIR
from assets.enemies import Murcielago
from assets.floorTraps import WoodTrap
from assets.sawTrap import SawTrap
from assets.pacmanFruit import PacmanFruit
from assets.door import Door
from assets.key import Key


import os
from config import LEVEL_DIR, CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, FONTS_DIR
"""Se definen coordenadas del mapa(En celdas de tablero) que definen un area y una clase areaManager para evaluar de forma rapida el estado de diferentes objetos en ellas"""
areas_dict = {
    "AREA1": Area("AREA1", 1, 1, 19, 19),
    "AREA2": Area("AREA2", 21, 1, 8, 19),
    "AREA3": Area("AREA3", 44, 1, 15, 19),
    "AREA4": Area("AREA4", 61, 6, 17, 13)
    #añadir mas areas si es necesario
}
class PlayingState1(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Cargar nivel
        self.load_level(os.path.join(LEVEL_DIR, 'level1.json'))
        
        #inicializacion de score
        self.game.score.init_level_score()
        
        # Division de la fase en areas
        area_manager = AreaManager()
        area_manager.load_areas(areas_dict)
        
        self.snake = Snake(8,10)
        
        #Definimos grupos de la fruta aleatoria
        self.apple_group = pygame.sprite.Group() 
        self.rotten_apple_group = pygame.sprite.Group()  
        self.last_rotten_apple_time = time.time()
        self.explosions_group = pygame.sprite.Group()  
        
        #Inicializacion de trampas y enemigos
        self.floor_trap_group = self.init_wood_traps()
        self.saw_trap_group = self.init_saw_traps()

        #Puerta de salida de la fase
        self.door=Door(75*CELL_SIZE,0*CELL_SIZE,False)
        self.door2=Door(76*CELL_SIZE,0*CELL_SIZE,False)
        self.door3=Door(77*CELL_SIZE,0*CELL_SIZE,False)
        self.door4=Door(78*CELL_SIZE,0*CELL_SIZE,False)
        self.key=Key(69 * CELL_SIZE,15 * CELL_SIZE,[self.door,self.door2,self.door3,self.door4])
        self.key_group=pygame.sprite.Group(self.key)
        self.door_group=pygame.sprite.Group(self.door,self.door2,self.door3,self.door4)


        #Lista con grupos de sprites
        self.group_list=(self.rotten_apple_group, self.apple_group, self.key_group, self.door_group, self.explosions_group, self.floor_trap_group, self.saw_trap_group)
        
        self.level_size = (self.level_manager.cell_number_x * CELL_SIZE, self.level_manager.cell_number_y * CELL_SIZE)
        
        self.init_apples(area_manager)

        #Musica del nivel
        self.background_music = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'level_1_theme.mp3'))
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
        self.fruit_sorting(AREA1, 1, RottenApple)
        self.fruit_sorting(AREA2, 1, RedApple)
        self.fruit_sorting(AREA2, 1, RottenApple)
        self.fruit_sorting(AREA3, 1, RedApple)
        self.fruit_sorting(AREA3, 1, RottenApple)
        self.fruit_sorting(AREA4, 1, RedApple)
        self.fruit_sorting(AREA4, 1, RottenApple)
        
    def fruit_sorting(self, area, number, fruit_class):
        "Llama a la función para añadir manzanas tantas veces como este definido en inicializar_apples"
        for _ in range(number):  # Generar "number" manzanas por área
                self.add_apple_in_area(area, fruit_class)

    def add_apple_in_area(self, area, fruit_class):
        "Crea la manzana de la clase pasada por parametro y la añade al grupo de manzanas"
        apple = fruit_class(lambda: self.level_manager.precalculate_static_objects_positions())
        apple.randomize(self.snake.body, area)
        self.apple_group.add(apple)

    def calculate_camera_offset(self):
        # Para que la serpiente se encuentre en el centro de la camara
        half_screen_width = SCREEN_WIDTH / 2
        half_screen_height = SCREEN_HEIGHT / 2

        snake_head_position = self.snake.segments.sprites()[0].rect.center
        camera_x = min(max(snake_head_position[0] - half_screen_width, 0), self.level_size[0] - SCREEN_WIDTH)
        camera_y = min(max(snake_head_position[1] - half_screen_height, 0), self.level_size[1] - SCREEN_HEIGHT)

        return Vector2(camera_x, camera_y)

    def calculate_camera_offset_block(self):
        # Para que la camara se mueva por bloques

        # Obtener la posición del centro de la cabeza de la serpiente
        snake_head_position = self.snake.segments.sprites()[0].rect.center

        # Calcular en qué "bloque" de la cámara está basado en la posición de la cabeza de la serpiente
        block_x = int(snake_head_position[0] // SCREEN_WIDTH)
        block_y = int(snake_head_position[1] // SCREEN_HEIGHT)

        # Calcular el desplazamiento de la cámara para centrar ese bloque
        camera_x = block_x * SCREEN_WIDTH
        camera_y = block_y * SCREEN_HEIGHT

        # Asegurarse de que la cámara no se desplace fuera de los límites del nivel
        camera_x = min(max(camera_x, 0), self.level_size[0] - SCREEN_WIDTH)
        camera_y = min(max(camera_y, 0), self.level_size[1] - SCREEN_HEIGHT)

        return Vector2(camera_x, camera_y)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.screen_manager.push_state('PAUSE')
                else:
                    # Actualiza la dirección basada en la tecla presionada
                    self.snake.update_direction(event.key)

    def update(self):
        current_time = time.time()
        self.snake.update(current_time)
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.push_state('GAME_OVER')
        self.camera_offset = self.calculate_camera_offset_block()
        self.explosions_group.update()
        for woodTrap in self.floor_trap_group:
            woodTrap.animate_trap()

        for sawTrap in self.saw_trap_group:
            sawTrap.animate_saw()
            sawTrap.handle_move()
        # Añadir RottenApple cada 5 segundos hasta un máximo de 5
        #if current_time - self.last_rotten_apple_time > 5 and len(self.rotten_apples) < 5:
        #    self.add_rotten_apple()
        #    self.last_rotten_apple_time = current_time
    def add_rotten_apple(self):
        #inicializacion temporal, funcion que no se usa en estos momentos
        AREA1 = AreaManager.get_instance().coords("AREA1")
        rotten_apple = RottenApple(lambda: self.level_manager.precalculate_static_objects_positions())
        rotten_apple.randomize(self.snake.body, AREA1)
        self.apple_group.add(rotten_apple) 
        self.rotten_apples.add(rotten_apple)

    def draw(self, screen):
        """Dibuja todos los elementos del juego en la pantalla."""
        screen.fill((175,215,70))
        self.level_manager.draw_level(screen, self.camera_offset)
        self.level_manager.draw_objects(screen, self.camera_offset)
        self.game.score.draw_score()
        
        for segment in self.snake.segments:
            adjusted_position = segment.rect.topleft - self.camera_offset
            screen.blit(segment.image, adjusted_position)
        
        for group in self.group_list:
            for asset in group:
                asset.draw(screen, self.camera_offset)

        for explosion in self.explosions_group:
            explosion.draw(screen, self.camera_offset)
        
    def load_level(self, json_path):
        self.level_manager = LevelManager(self.game.screen)
        self.level_manager.load_level_from_json(os.path.join(LEVEL_DIR, json_path))
    
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
        self.background_music.stop()
        self.game.score.save_score()
        self.game.screen_manager.change_state('STORY2')
        self.game.screen_manager.update()

    def tag(self):
        return "PLAYING1"