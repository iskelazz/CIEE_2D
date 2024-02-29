import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.RedApple import RedApple
from assets.staticObjects.Fence import Fence
from assets.Snake import Snake
from phases.LevelManager import LevelManager
import os
from config import LEVEL_DIR

class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Cargar nivel
        self.level_manager = LevelManager(self.game.screen, game.cell_size, game.cell_number)
        self.level_manager.load_level_from_json(os.path.join(LEVEL_DIR, 'level1.json'))
        
        self.snake = Snake()
        self.apple = RedApple(lambda: self.level_manager.precalculate_static_objects_positions())
        self.apple.randomize(self.snake.body)
        self.apple_group = pygame.sprite.GroupSingle(self.apple)
        

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
        self.check_collisions()
        if self.snake.is_snake_out_of_bounds(self.game.cell_number):
            self.game.screen_manager.change_state('GAME_OVER')

    def draw(self, screen):
        """Dibuja todos los elementos del juego en la pantalla."""
        screen.fill((175,215,70))
        self.level_manager.draw_level()
        self.level_manager.draw_objects()
        self.game.score.draw_score()
        self.snake.segments.draw(screen)
        self.apple_group.draw(screen)

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
        body = pygame.sprite.Group(self.snake.segments.sprites()[1:])
        #Colisión con manzana
        if pygame.sprite.spritecollideany(head, self.apple_group):
            self.apple.randomize(self.snake.body)
            self.snake.add_block()
            self.game.score.eat_red_apple()
        #Colision de serpiente con su cuerpo    
        if pygame.sprite.spritecollideany(head, body):
            self.game.screen_manager.change_state('GAME_OVER')
        self.level_manager.check_collisions(head, self.game.screen_manager)
        