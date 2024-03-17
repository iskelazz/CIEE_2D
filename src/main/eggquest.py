import pygame
import sys
from metrics.Score import Score
from state.StateManager import StateManager
from config import Config

class EggQuest:
    def __init__(self):
        self.initialize_game()
        # Valorar la creacion de una clase repositorio para compartir info entre estados
        self.score = Score(self.screen, self.screen_width)
        self.screen_manager = StateManager(self)
        self.screen_manager.change_state('PLAYING3')

    def initialize_game(self):
        """Configura los parámetros iniciales y los objetos de Pygame."""
        pygame.init()
        Config.initialize()
        self.screen_width = Config.SCREEN_WIDTH
        self.screen_height = Config.SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) #800x800
        pygame.display.set_caption('EggQuest')
        self.FPS = 60
        self.clock = pygame.time.Clock()

        #mixer para efectos de sonido 
        pygame.mixer.pre_init(44100,-16,2,512)
        pygame.mixer.init()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen_manager.handle_events(events)  # Manejar eventos a través del ScreenManager
            self.screen_manager.update()  # Actualizar estado a través del ScreenManager
            self.screen.fill((0, 0, 0))  # Considera mover esto dentro de cada estado si necesitas fondos diferentes
            self.screen_manager.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    game = EggQuest()
    game.run()

