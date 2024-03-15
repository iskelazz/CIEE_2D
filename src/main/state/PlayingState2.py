import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.redapple import RedApple
from assets.rottenApple import RottenApple
from assets.key import Key
from assets.snake.snake import Snake
from assets.pointsDoor import PointsDoor
from assets.door import Door
from phases.LevelManager import LevelManager
from assets.floorTraps import SpikeTrap
from assets.sawTrap import SawTrap
from assets.enemies import Murcielago
from resources.text.TextCollection import TextColection
from phases.Area import Area
from phases.AreaManager import AreaManager
from assets.gemstone import Gemstone
from assets.goldenapple import GoldenApple
from assets.pacmanFruit import PacmanFruit

import os
from config import LEVEL_DIR, CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, FONTS_DIR
"""Se definen coordenadas del mapa(En celdas de tablero) que definen un area y una clase areaManager para evaluar de forma rapida el estado de diferentes objetos en ellas"""
areas_dict = {
    "AREA1": Area("AREA1", 1, 1, 19, 19),
    "AREA2": Area("AREA2", 1, 21, 19, 18),
    "AREA3": Area("AREA3", 21, 1, 10, 23),
    "AREA4": Area("AREA4", 40, 1, 8, 19)
    #añadir mas areas si es necesario
}
class PlayingState2(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Cargar nivel
        self.load_level(os.path.join(LEVEL_DIR, 'level2_alt.json'))
        area_manager = AreaManager()
        self.game.score.init_level_score()
        reference_score = self.game.score.score
        area_manager.load_areas(areas_dict)
        self.snake = Snake(5,29)
        self.bat = Murcielago(3, 3, 8, 8, 8, 8, 2, False)
        self.bat2 = Murcielago(10, 10, 5, 2, 5, 2, 2, False)
        self.bat3 = Murcielago(8, 3, 0, 8, 0, 8, 2, False)
        self.bat4 = Murcielago(22, 18, 7, 4, 7, 4, 2, False)
        self.bat5 = Murcielago(24, 3, 0, 8, 0, 8, 2, False)
        self.sawTrap = SawTrap(45, 5, 8, 'vertical')
        self.spikeTrap = SpikeTrap(Vector2(6, 4))
        self.spikeTrap2 = SpikeTrap(Vector2(6, 2))
        self.spikeTrap3 = SpikeTrap(Vector2(7, 4))
        self.spikeTrap4 = SpikeTrap(Vector2(5, 4))
        self.spikeTrap5 = SpikeTrap(Vector2(24, 35))
        self.spikeTrap6 = SpikeTrap(Vector2(29, 35))
        self.rotten_apple_group = pygame.sprite.Group()  
        self.last_rotten_apple_time = time.time()
        self.gemstone = Gemstone(26,12)
        self.gemstone2 = Gemstone(45,18)
        self.gemstone_drop = False
        self.golden_apple = GoldenApple(37,29)
        self.pacmanFruit=PacmanFruit(37,3)
  

        self.pointsDoor1=PointsDoor(9*CELL_SIZE,20*CELL_SIZE,False,self.game.score,500+reference_score)
        self.pointsDoor2=PointsDoor(10*CELL_SIZE,20*CELL_SIZE,False,self.game.score,500+reference_score)
        self.door=Door(18*CELL_SIZE,13*CELL_SIZE,True)
        self.door2=Door(18*CELL_SIZE,14*CELL_SIZE,True)
        self.key=Key(6 * CELL_SIZE,3 * CELL_SIZE,[self.door,self.door2])

        self.pointsDoor3=PointsDoor(44*CELL_SIZE,17*CELL_SIZE,True,self.game.score,3000+reference_score)
        self.pointsDoor4=PointsDoor(44*CELL_SIZE,18*CELL_SIZE,True,self.game.score,3000+reference_score)
        self.door3=Door(57*CELL_SIZE,0*CELL_SIZE,True)
        self.door4=Door(57*CELL_SIZE,1*CELL_SIZE,True)
        self.key2=Key(58 * CELL_SIZE,18 * CELL_SIZE,[self.door3,self.door4])

        self.pointsDoor_group=pygame.sprite.Group(self.pointsDoor1,self.pointsDoor2,self.pointsDoor3,self.pointsDoor4)
        self.explosions_group = pygame.sprite.Group()    
        self.key_group=pygame.sprite.Group(self.key, self.key2)
        self.door_group=pygame.sprite.Group(self.pointsDoor1,self.pointsDoor2,self.door,self.door2,self.pointsDoor3,self.pointsDoor4,self.door3,self.door4)
        self.apple_group = pygame.sprite.Group()
        self.spike_trap_group=pygame.sprite.Group(self.spikeTrap,self.spikeTrap2,self.spikeTrap3,self.spikeTrap4,self.spikeTrap5,self.spikeTrap6)
        self.saw_trap_group=pygame.sprite.Group(self.sawTrap)
        self.gemstone_group = pygame.sprite.Group(self.gemstone2)
        self.golden_apple_group = pygame.sprite.Group(self.golden_apple)
        self.enemie_group=pygame.sprite.Group(self.bat, self.bat2, self.bat3, self.bat4, self.bat5)
        self.fruit_group=pygame.sprite.Group(self.pacmanFruit)
        self.group_list=(self.key_group,self.door_group,self.apple_group,self.rotten_apple_group,self.spike_trap_group,self.saw_trap_group, self.gemstone_group, self.golden_apple_group,self.enemie_group,self.fruit_group)

        self.level_size = (self.level_manager.cell_number_x * CELL_SIZE, self.level_manager.cell_number_y * CELL_SIZE)

        # Inicializa temporizadores de reaparición
        self.timer_respawn_pacman = None
        self.timer_respawn_gemstone = None
        
        self.init_apples(area_manager)

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
    
    def respawn_object_if_missing(self, object, group, timer, interval):
        """
        Comprueba si un objeto está en un grupo y, si no está, activa un timer.
        Si el timer supera el intervalo especificado, vuelve a añadir el objeto al grupo.

        :param object: El objeto a comprobar y potencialmente reaparecer.
        :param group: El grupo de sprites al que pertenece el objeto.
        :param timer: El temporizador actual para el objeto. None si el objeto no está en cooldown.
        :param interval: El intervalo de tiempo (en milisegundos) para reaparecer el objeto.
        :return: El estado actualizado del temporizador para el objeto.
        """
        current_time = pygame.time.get_ticks()  # Obtiene el tiempo actual
        if object not in group:
            if timer is None:
                timer = current_time
            elif current_time - timer > interval:
                group.add(object)
                timer = None
        else:
            timer = None  # Resetea el timer si el objeto ya está en el grupo
        
        return timer

    def respawn_key_items(self):
        """
        Función para gestionar el reaparecido de la fruta de Pacman y la gema.
        """
        # Intervalo para reaparecer la fruta de Pacman, en milisegundos
        interval_pacman = 35000  # 35 segundos

        # Intervalo para reaparecer la gema, en milisegundos
        interval_gemstone = 15000  # 15 segundos

        # Comprueba y gestiona el reaparecido de la fruta de Pacman
        self.timer_respawn_pacman = self.respawn_object_if_missing(
            self.pacmanFruit,
            self.fruit_group,
            self.timer_respawn_pacman,
            interval_pacman
        )
        if self.gemstone_drop:
            # Comprueba y gestiona el reaparecido de las 2 gemas
            self.timer_respawn_gemstone = self.respawn_object_if_missing(
                self.gemstone,
                self.gemstone_group,
                self.timer_respawn_gemstone,
                interval_gemstone
            )

    def update(self):
        current_time = time.time()
        self.snake.update(current_time)
        for enemie in self.enemie_group:
            enemie.update()
            enemie.handle_move()
        
        for spikeTrap in self.spike_trap_group:
            spikeTrap.animate_trap()
        for sawTrap in self.saw_trap_group:
            sawTrap.animate_saw()
            sawTrap.handle_move()
            
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.push_state('GAME_OVER')
        self.camera_offset = self.calculate_camera_offset_block()
        for pointsDoor in self.door_group:
            pointsDoor.update()
        self.explosions_group.update()
        self.drop_gemstone()
        self.respawn_key_items()
    def add_rotten_apple(self):
        #inicializacion temporal, funcion que no se usa en estos momentos
        AREA1 = AreaManager.get_instance().coords("AREA1")
        rotten_apple = RottenApple(lambda: self.level_manager.precalculate_static_objects_positions())
        rotten_apple.randomize(self.snake.body, AREA1)
        self.apple_group.add(rotten_apple) 
        self.rotten_apples.add(rotten_apple)

    def drop_gemstone(self):
        number_enemies = AreaManager.get_instance().count_objects_in_area(self.enemie_group,"AREA1")+AreaManager.get_instance().count_objects_in_area(self.enemie_group,"AREA3")
        if number_enemies == 0 and self.gemstone_drop==False:
            self.gemstone_group.add(self.gemstone)
            self.gemstone_drop=True

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
        self.game.score.save_score()
        self.game.screen_manager.change_state('PLAYING3')
        self.game.screen_manager.update()

    def tag(self):
        return "PLAYING2"