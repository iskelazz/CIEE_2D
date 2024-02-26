import pygame
import sys
from assets.RedApple import RedApple
from assets.Fence import Fence
from assets.Snake import Snake
from phases.GameBoard import GameBoard
from metrics.Score import Score
from state.GameState import StartScreenState, GameOverState, PauseState

cell_size = 40
cell_number = 20

class EggQuest:
    def __init__(self):
        self.initialize_game()
        self.snake = Snake()
        self.walls = Fence.create_fences()
        self.apple = RedApple()
        self.apple.randomize(self.walls, self.snake.body)
        self.apple_group = pygame.sprite.GroupSingle(self.apple)
        self.phase = GameBoard(self.screen,self.cell_size,self.cell_number)
        self.score = Score(self.screen,self.screen_width)
        self.state = StartScreenState(self)
        self.previous_state = None

    def initialize_game(self):
        """Configura los parámetros iniciales y los objetos de Pygame."""
        pygame.init()
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.screen_width = self.cell_size * self.cell_number
        self.screen_height = self.cell_size * self.cell_number
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

    def draw_elements(self):
        """Dibuja todos los elementos del juego en la pantalla."""
        self.screen.fill((175,215,70))
        self.phase.draw_grass()
        self.score.draw_score()
        self.snake.segments.draw(self.screen)
        self.apple_group.draw(self.screen)
        self.walls.draw(self.screen)

    def change_state(self, new_state):
        """Cambio de pantalla a traves de un patron estado"""
        if not isinstance(new_state, PauseState):
            self.previous_state = self.state
        self.state = new_state

    def handle_events(self):
        """Maneja los eventos de entrada del usuario."""
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            else:
                self.state.handle_events([event])  # Delega todos los eventos al estado actual


    def check_collisions(self):
        """Verifica y maneja las colisiones."""
        head = self.snake.segments.sprites()[0]
        body = pygame.sprite.Group(self.snake.segments.sprites()[1:])
        #Colisión con manzana
        if pygame.sprite.spritecollideany(head, self.apple_group):
            self.apple.randomize(self.walls, self.snake.body)
            self.snake.add_block()
            self.score.eat_red_apple()
        #Colision de serpiente con su cuerpo    
        if pygame.sprite.spritecollideany(head, body):
            self.change_state(GameOverState(self))

        # Colisión con los muros
        if pygame.sprite.spritecollideany(head, self.walls):
            self.change_state(GameOverState(self))

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.state.handle_events(events)
            self.state.update()
            self.screen.fill((0, 0, 0))  # Considera mover esto dentro de cada estado si necesitas fondos diferentes
            self.state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(10)

if __name__ == "__main__":
    game = EggQuest()
    game.run()
