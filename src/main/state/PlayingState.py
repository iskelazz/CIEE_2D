import pygame
import time
from pygame.math import Vector2
from state.GameState import GameState
from assets.RedApple import RedApple
from assets.Fence import Fence
from assets.Snake import Snake
from phases.GameBoard import GameBoard
from metrics.Score import Score

class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Prepara el estado para jugar
        self.snake = Snake()
        self.walls = Fence.create_fences()
        self.apple = RedApple()
        self.apple.randomize(self.walls, self.snake.body)
        self.apple_group = pygame.sprite.GroupSingle(self.apple)
        self.phase = GameBoard(self.game.screen, game.cell_size, game.cell_number)

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
        self.phase.draw_grass()
        self.game.score.draw_score()
        self.snake.segments.draw(screen)
        self.apple_group.draw(screen)
        self.walls.draw(screen)

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
            self.apple.randomize(self.walls, self.snake.body)
            self.snake.add_block()
            self.game.score.eat_red_apple()
        #Colision de serpiente con su cuerpo    
        if pygame.sprite.spritecollideany(head, body):
            self.game.screen_manager.change_state('GAME_OVER')

        # Colisión con los muros
        if pygame.sprite.spritecollideany(head, self.walls):
            self.game.screen_manager.change_state('GAME_OVER')