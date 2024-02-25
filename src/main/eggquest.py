import pygame
from assets.snake import Snake
from phases.phase1 import Phase1

from pygame.locals import *



class eggquest:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.snake = Snake(10,10)
        self.current_phase = 1
        self.current_screen = 1
          
        self.phases = {
            1: Phase1(width, height)
        }

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.snake.direction != "DOWN":
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN and self.snake.direction != "UP":
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT and self.snake.direction != "RIGHT":
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT and self.snake.direction != "LEFT":
                    self.snake.change_direction("RIGHT")

    def update(self):
        self.phases[self.current_phase].update(self.current_screen)

    def render(self):
        self.screen.fill((0, 0, 0))  # Limpia la pantalla con color negro
        self.phases[self.current_phase].render(self.screen, self.current_screen)
        self.snake.draw(self.screen)

        pygame.display.flip()  # Actualiza la pantalla

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.render()
            self.snake.move()
            self.clock.tick(10)  # Controla la velocidad de actualización del juego

if __name__ == "__main__":
    game = eggquest(800, 600)
    game.run()