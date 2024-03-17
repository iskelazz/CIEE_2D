import pygame
import time
from state.PlayingState import PlayingState
from assets.redapple import RedApple
from assets.rottenApple import RottenApple
from phases.LevelManager import LevelManager
from assets.egg import Egg
from phases.Area import Area
from phases.AreaManager import AreaManager
from assets.gemstone import Gemstone
from camera import Camera, FollowSnake

from assets.eagle import Eagle

import os
from config import Config

areas_dict = {
    "AREA1": Area("AREA1", 1, 13, 16, 5),
    "AREA2": Area("AREA2", 1, 1, 39, 12),
    "AREA3": Area("AREA3", 40, 1, 39, 12)
    #añadir mas areas si es necesario
}
class PlayingState3(PlayingState):
    def __init__(self, game):
        super().__init__(game)
        self.camera = Camera(FollowSnake())
        self.game.score.init_level_score()
        # Cargar nivel
        self.load_level(os.path.join(Config.LEVEL_DIR, 'level3.json'))

        self.initialize_snake((4, 15))

        area_manager = AreaManager()
        area_manager.load_areas(areas_dict)

        self.gemstone = Gemstone(77,2)
        #self.eagle=Eagle()
        self.egg=Egg(4,4)
        self.spike_trap_group=pygame.sprite.Group()
        self.egg_group = pygame.sprite.Group(self.egg)
        self.enemy_group=pygame.sprite.Group()
        self.rotten_apple_group = pygame.sprite.Group()
        self.apple_group = pygame.sprite.Group()
        self.gemstone_group = pygame.sprite.Group(self.gemstone)
        self.explosions_group = pygame.sprite.Group()   
        
        self.group_list=(self.apple_group,self.rotten_apple_group,self.gemstone_group,self.enemy_group,self.egg_group,self.spike_trap_group)
        self.level_size = (self.level_manager.cell_number_x * Config.CELL_SIZE, self.level_manager.cell_number_y * Config.CELL_SIZE)
        self.init_apples(area_manager)

        #sonidos
        self.background_music = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'level_3_theme.mp3'))
        self.background_music.play(-1)

    def init_apples(self, area_manager):
        "Inicializado de las manzanas según el diseño establecido para el nivel"
        #Definimos las areas donde queremos inicializar manzanas
        AREA1 = area_manager.coords("AREA1")
        AREA2 = area_manager.coords("AREA2")
        AREA3 = area_manager.coords("AREA3")

        #Una fruta buena y una mala por area
        self.fruit_sorting(AREA1, 1, RedApple)
        self.fruit_sorting(AREA1, 1, RottenApple)
        self.fruit_sorting(AREA2, 1, RedApple)
        self.fruit_sorting(AREA2, 1, RottenApple)
        self.fruit_sorting(AREA3, 1, RedApple)
        self.fruit_sorting(AREA3, 1, RottenApple)
        
    def fruit_sorting(self, area, number, fruit_class):
        "Llama a la función para añadir manzanas tantas veces como este definido en inicializar_apples"
        for _ in range(number):  # Generar "number" manzanas por área
                self.add_apple_in_area(area, fruit_class)

    def add_apple_in_area(self, area, fruit_class):
        "Crea la manzana de la clase pasada por parametro y la añade al grupo de manzanas"
        apple = fruit_class(lambda: self.level_manager.precalculate_static_objects_positions())
        apple.randomize(self.snake.body, area)
        self.apple_group.add(apple)    
    
    def update(self):
        current_time = time.time()
        self.snake.update(current_time)
        #self.eagle.update(self.snake,current_time,self.enemy_group,self.spike_trap_group)
        self.camera.update(self.snake)
        for enemie in self.enemy_group:
            enemie.update()
            enemie.handle_move()
        for spikeTrap in self.spike_trap_group:
            spikeTrap.animate_trap()
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.push_state('GAME_OVER')

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
        #self.eagle.draw(screen, self.camera.offset)
    def load_level(self, json_path):
        self.level_manager = LevelManager(self.game.screen)
        self.level_manager.load_level_from_json(os.path.join(Config.LEVEL_DIR, json_path))

    
    def check_collisions(self):
        """Verifica y maneja las colisiones."""
        head = self.snake.segments.sprites()[0]
        tail= self.snake.segments.sprites()[-1]
        body = pygame.sprite.Group(self.snake.segments.sprites()[1:])
        head_body = pygame.sprite.Group(head,self.snake.segments.sprites()[1:])
        for group in self.group_list:
            collision_dict=pygame.sprite.groupcollide(head_body, group,False, False,)
            for segment,collided_asset in collision_dict.items():
                collided_asset[0].handle_collision(segment,self.snake,self.game)
        
        #Colision de serpiente con su cuerpo
        if pygame.sprite.spritecollideany(head, body):
            self.game.screen_manager.push_state('GAME_OVER')
        #if pygame.sprite.spritecollideany(self.eagle,head_body):
        #    self.eagle.handle_collision(self.snake,self.game)   
        
        self.level_manager.check_collisions(self.snake, self.game.screen_manager, self.explosions_group)
    
    def next_level(self):
        self.game.screen_manager.change_state('MENU')
        self.game.score.save_score()
    
    def tag(self):
        return "PLAYING3"