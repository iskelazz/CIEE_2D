import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.redapple import RedApple
from assets.hole import Hole
from assets.key import Key
from assets.snake import Snake
from assets.pointsDoor import PointsDoor
from assets.door import Door
from phases.LevelManager import LevelManager
from assets.floorTraps import FireTrap
from assets.floorTraps import SpikeTrap
from assets.sawTrap import SawTrap

import os
from config import LEVEL_DIR, CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

class PlayingState1(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Cargar nivel
        self.load_level(os.path.join(LEVEL_DIR, 'level.json'))
        self.snake = Snake()
        self.sawTrap = SawTrap(45, 5, 8, 'vertical')
        self.fireTrap = FireTrap(Vector2(5, 5))
        self.spikeTrap = SpikeTrap(Vector2(8, 8))
        self.apple = RedApple(lambda: self.level_manager.precalculate_static_objects_positions())
        self.apple.randomize(self.snake.body)
        self.pointsDoor1=PointsDoor(700,360,True,self.game.score)
        self.pointsDoor2=PointsDoor(700,400,True,self.game.score)
        self.door=Door(300,100,True)
        self.key=Key(300,200,self.door)
        
        self.key_group=pygame.sprite.Group(self.key)
        self.door_group=pygame.sprite.Group(self.pointsDoor1,self.pointsDoor2,self.door)
        self.apple_group = pygame.sprite.GroupSingle(self.apple)
        self.level_size = (self.level_manager.cell_number_x * CELL_SIZE, self.level_manager.cell_number_y * CELL_SIZE)
        
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
                    self.game.screen_manager.change_state('PAUSE')
                else:
                    # Actualiza la dirección basada en la tecla presionada
                    self.update_direction(event.key)

    def update(self):
        current_time = time.time()
        self.snake.update(current_time)
        self.fireTrap.animate_trap()
        self.spikeTrap.animate_trap()
        self.sawTrap.animate_saw()
        self.sawTrap.handle_move()
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.change_state('GAME_OVER')
        self.camera_offset = self.calculate_camera_offset_block()
        for pointsDoor in self.door_group:
            pointsDoor.update()
        

    def draw(self, screen):
        """Dibuja todos los elementos del juego en la pantalla."""
        screen.fill((175,215,70))
        self.level_manager.draw_level(screen, self.camera_offset)
        self.level_manager.draw_objects(screen, self.camera_offset)
        self.game.score.draw_score()
        self.fireTrap.draw(screen, self.camera_offset)
        self.spikeTrap.draw(screen, self.camera_offset)
        self.sawTrap.draw(screen, self.camera_offset)
        for segment in self.snake.segments:
            adjusted_position = segment.rect.topleft - self.camera_offset
            screen.blit(segment.image, adjusted_position)
        for apple in self.apple_group:
            apple.draw(screen, self.camera_offset)
        for pointsDoor in self.door_group:
            pointsDoor.draw(screen, self.camera_offset)
        for key in self.key_group:
            key.draw(screen, self.camera_offset)
        
    def load_level(self, json_path):
        self.level_manager = LevelManager(self.game.screen)
        self.level_manager.load_level_from_json(os.path.join(LEVEL_DIR, json_path))

    def update_direction(self, key):
        """Actualiza la dirección de la serpiente basada en la entrada del usuario."""
        directions = {
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1),
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
        }
        if key in directions and directions[key] != -self.snake.direction:
            self.snake.direction = directions[key]
    
    def check_collisions(self):
        """Verifica y maneja las colisiones."""
        head = self.snake.segments.sprites()[0]
        tail= self.snake.segments.sprites()[-1]
        body = pygame.sprite.Group(self.snake.segments.sprites()[1:])
        #Colisión con manzana
        if pygame.sprite.spritecollideany(head, self.apple_group):
            self.apple.randomize(self.snake.body)
            self.snake.add_block()
            self.game.score.eat_red_apple()
        #Colision de serpiente con su cuerpo
        if pygame.sprite.spritecollideany(head, body):
            self.game.screen_manager.change_state('GAME_OVER')
        collided_door=pygame.sprite.spritecollideany(head, self.door_group)
        if collided_door!=None:
            collided_door.manage_collisions(self.game)
        collided_key=pygame.sprite.spritecollideany(head, self.key_group)
        if collided_key!=None:
            collided_key.pick_up()
        self.level_manager.check_collisions(head, tail, self.game.screen_manager)

        #Función de colisión con FloorTraps    
        def floortrap_collision(floortrap):
            if pygame.sprite.collide_mask(head, floortrap) or pygame.sprite.spritecollideany(floortrap, body):
                if floortrap.is_on():
                    self.snake.reduce_body()
                    self.game.score.trap_collision()
                if len(self.snake.body) < 1 or self.game.score.score < 0:
                    self.game.screen_manager.change_state('GAME_OVER')
       
        #Función de colisión con SawTraps            
        def sawtrap_collision(sawtrap):
            #Colision con cuchilla de cabeza
            if pygame.sprite.collide_mask(head, sawtrap):
                self.game.screen_manager.change_state('GAME_OVER')
           
            #Colision con cuchilla de cuerpo
            if pygame.sprite.spritecollideany(sawtrap, body):
                index = 0
                for i, element in enumerate(body):
                    if pygame.sprite.collide_rect(sawtrap, element):
                    # Se ha encontrado una colisión
                        index = i
                        break
       
                reduce_value = len(body) - index
                for i in range(reduce_value):
                    self.snake.reduce_body()
           
           
        #Colision con trampas de fuego
        floortrap_collision(self.fireTrap)    
   
        #Colision con trampas de pinchos
        floortrap_collision(self.spikeTrap)        
               
        #Colision con cuchilla
        sawtrap_collision(self.sawTrap)
    
    def next_level(self):
        self.game.screen_manager.change_state('PLAYING2')
        self.game.screen_manager.update()