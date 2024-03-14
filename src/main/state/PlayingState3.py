import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.redapple import RedApple
from assets.rottenApple import RottenApple
from assets.Hole import Hole
from assets.key import Key
from animations.explosion import Explosion
from assets.snake.snake import Snake
from assets.snake.fastState import FastState
from assets.pointsDoor import PointsDoor
from assets.door import Door
from phases.LevelManager import LevelManager
from assets.floorTraps import FireTrap
from assets.floorTraps import SpikeTrap
from assets.egg import Egg
from assets.sawTrap import SawTrap
from assets.enemies import Murcielago
from resources.text.TextCollection import TextColection
from phases.Area import Area
from phases.AreaManager import AreaManager
from assets.gemstone import Gemstone
from assets.goldenapple import GoldenApple
from assets.pacmanFruit import PacmanFruit

from assets.enemies import Eagle
from assets.enemies import Feather
import os
from config import LEVEL_DIR, CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, FONTS_DIR

areas_dict = {
    "AREA1": Area("AREA1", 1, 1, 39, 19),
    "AREA2": Area("AREA2", 1, 21, 19, 39)
    #añadir mas areas si es necesario
}
class PlayingState3(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.camera_offset = Vector2(0, 0)
        # Cargar nivel
        self.load_level(os.path.join(LEVEL_DIR, 'level3.json'))
        area_manager = AreaManager()
        area_manager.load_areas(areas_dict)
        self.snake = Snake(10,8)
        self.gemstone = Gemstone(26,12)
        self.eagle=Eagle()
        self.egg=Egg(20,10)
        self.spike_trap_group=pygame.sprite.Group()
        self.egg_group = pygame.sprite.Group(self.egg)
        self.enemy_group=pygame.sprite.Group()
        self.rotten_apple_group = pygame.sprite.Group()
        self.apple_group = pygame.sprite.Group()
        self.gemstone_group = pygame.sprite.Group(self.gemstone)
        self.explosions_group = pygame.sprite.Group()   
        
        self.group_list=(self.apple_group,self.rotten_apple_group,self.gemstone_group,self.enemy_group,self.egg_group,self.spike_trap_group)
        self.level_size = (self.level_manager.cell_number_x * CELL_SIZE, self.level_manager.cell_number_y * CELL_SIZE)
        self.init_apples(area_manager)

    def init_apples(self, area_manager):
        "Inicializado de las manzanas según el diseño establecido para el nivel"
        #Definimos las areas donde queremos inicializar manzanas
        AREA1 = area_manager.coords("AREA1")
        AREA2 = area_manager.coords("AREA2")

        #Una fruta buena y una mala por area
        self.fruit_sorting(AREA1, 2, RedApple)
        self.fruit_sorting(AREA1, 3, RottenApple)
        self.fruit_sorting(AREA2, 2, RedApple)
        self.fruit_sorting(AREA2, 4, RottenApple)
        
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
        # Coordenadas objetivo basadas en la posición de la cabeza de la serpiente
        target_x = self.snake.segments.sprites()[0].rect.centerx - SCREEN_WIDTH / 2
        target_y = self.snake.segments.sprites()[0].rect.centery - SCREEN_HEIGHT / 2

        # Asegurarse de que la cámara no se salga de los límites del nivel
        target_x = min(max(0, target_x), self.level_size[0] - SCREEN_WIDTH)
        target_y = min(max(0, target_y), self.level_size[1] - SCREEN_HEIGHT)

        # Interpolar entre la posición actual de la cámara y el objetivo
        # El factor de lerp determina qué tan "suave" o "rápido" es el movimiento de la cámara
        # Un valor más bajo resultará en un movimiento más suave
        lerp_factor = 0.1
        new_camera_x = self.camera_offset.x + (target_x - self.camera_offset.x) * lerp_factor
        new_camera_y = self.camera_offset.y + (target_y - self.camera_offset.y) * lerp_factor
        # Actualizar la posición de la cámara
        return Vector2(new_camera_x, new_camera_y)


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
                    self.game.screen_manager.change_state('PAUSE')
                else:
                    # Actualiza la dirección basada en la tecla presionada
                    self.snake.update_direction(event.key)

    def update(self):
        current_time = time.time()
        self.snake.update(current_time)
        self.eagle.update(self.snake,current_time,self.enemy_group,self.spike_trap_group)
        for enemie in self.enemy_group:
            enemie.update()
            enemie.handle_move()
        for spikeTrap in self.spike_trap_group:
            spikeTrap.animate_trap()
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.change_state('GAME_OVER')
        self.camera_offset = self.calculate_camera_offset()
        print(self.camera_offset)

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
        self.eagle.draw(screen, self.camera_offset)
    def load_level(self, json_path):
        self.level_manager = LevelManager(self.game.screen)
        self.level_manager.load_level_from_json(os.path.join(LEVEL_DIR, json_path))

    
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
            self.game.screen_manager.change_state('GAME_OVER')
        if pygame.sprite.spritecollideany(self.eagle,head_body):
            self.eagle.handle_collision(self.snake,self.game)   
        
        self.level_manager.check_collisions(head, tail, self.snake.state, self.game.screen_manager, self.explosions_group)
    
    def next_level(self):
        self.game.screen_manager.change_state('PLAYING2')