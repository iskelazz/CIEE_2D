import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.RedApple import RedApple
from assets.RottenApple import RottenApple  
from assets.Snake import Snake
from phases.LevelManager import LevelManager
import os
from config import LEVEL_DIR, CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH

class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.load_level(os.path.join(LEVEL_DIR, 'level.json'))
        self.snake = Snake()
        self.red_apple = RedApple(lambda: self.level_manager.precalculate_static_objects_positions())
        self.apple_group = pygame.sprite.Group(self.red_apple)  
        self.rotten_apples = pygame.sprite.Group()  
        self.last_rotten_apple_time = time.time()  
        self.level_size = (self.level_manager.cell_number_x * CELL_SIZE, self.level_manager.cell_number_y * CELL_SIZE)
        self.red_apple.randomize(self.snake.body)

    def calculate_camera_offset(self):
        half_screen_width = SCREEN_WIDTH / 2
        half_screen_height = SCREEN_HEIGHT / 2

        snake_head_position = self.snake.segments.sprites()[0].rect.center
        camera_x = min(max(snake_head_position[0] - half_screen_width, 0), self.level_size[0] - SCREEN_WIDTH)
        camera_y = min(max(snake_head_position[1] - half_screen_height, 0), self.level_size[1] - SCREEN_HEIGHT)

        return Vector2(camera_x, camera_y)

    def calculate_camera_offset_block(self):
        snake_head_position = self.snake.segments.sprites()[0].rect.center
        block_x = int(snake_head_position[0] // SCREEN_WIDTH)
        block_y = int(snake_head_position[1] // SCREEN_HEIGHT)
        camera_x = block_x * SCREEN_WIDTH
        camera_y = block_y * SCREEN_HEIGHT
        camera_x = min(max(camera_x, 0), self.level_size[0] - SCREEN_WIDTH)
        camera_y = min(max(camera_y, 0), self.level_size[1] - SCREEN_HEIGHT)

        return Vector2(camera_x, camera_y)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.screen_manager.change_state('PAUSE')
                else:
                    self.update_direction(event.key)

    def update(self):
        current_time = time.time()
        self.snake.update(current_time)
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.level_manager.cell_number_x, self.level_manager.cell_number_y):
            self.game.screen_manager.change_state('GAME_OVER')
        self.camera_offset = self.calculate_camera_offset_block()
        # Añadir RottenApple cada 5 segundos hasta un máximo de 5
        if current_time - self.last_rotten_apple_time > 5 and len(self.rotten_apples) < 5:
            self.add_rotten_apple()
            self.last_rotten_apple_time = current_time

    def add_rotten_apple(self):
        rotten_apple = RottenApple(lambda: self.level_manager.precalculate_static_objects_positions())
        rotten_apple.randomize(self.snake.body)
        self.apple_group.add(rotten_apple) 
        self.rotten_apples.add(rotten_apple)  

    def draw(self, screen):
        screen.fill((175,215,70))
        self.level_manager.draw_level(screen, self.camera_offset)
        self.level_manager.draw_objects(screen, self.camera_offset)
        self.game.score.draw_score()
        for segment in self.snake.segments:
            adjusted_position = segment.rect.topleft - self.camera_offset
            screen.blit(segment.image, adjusted_position)
        self.apple_group.draw(screen)  # Dibuja todas las manzanas en el grupo

    def load_level(self, json_path):
        self.level_manager = LevelManager(self.game.screen)
        self.level_manager.load_level_from_json(os.path.join(LEVEL_DIR, json_path))

    def update_direction(self, key):
        directions = {
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1),
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
        }
        if key in directions and directions[key] != -self.snake.direction:
            self.snake.direction = directions[key]
    
    def check_collisions(self):
        head = self.snake.segments.sprites()[0]
        body = pygame.sprite.Group(self.snake.segments.sprites()[1:])
        collided_apple = pygame.sprite.spritecollideany(head, self.apple_group)
        if collided_apple:
            collided_apple.randomize(self.snake.body)
            if isinstance(collided_apple, RedApple):
                self.snake.add_block()
                self.game.score.eat_red_apple()
            elif isinstance(collided_apple, RottenApple):
                if len(self.snake.body) > 1:  # Asegurarse de que la serpiente no se reduzca por debajo de un tamaño mínimo
                    self.snake.reduce_body()
                    self.game.score.eat_rotten_apple() 
        if pygame.sprite.spritecollideany(head, body):
            self.game.screen_manager.change_state('GAME_OVER')
        self.level_manager.check_collisions(head, self.game.screen_manager)
