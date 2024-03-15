import pygame
from state.GameState import GameState
import sys, os
from config import GRAPHICS_DIR, SOUNDS_DIR

class Tutorial1State(GameState):
    def __init__(self,game):
        super().__init__(game)
        self.tutorial_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'tutorial_1.png')).convert()
        self.tutorial_image = pygame.transform.scale(self.tutorial_image, (game.screen_width, game.screen_height))
        self.background_music = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'level_1_theme.mp3'))
        self.background_music.play(-1)
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_RETURN:
                    self.game.__init__()
                    self.background_music.stop()
                    self.game.screen_manager.change_state('PLAYING1')
    
    def draw(self, screen):
    # Dibuja la imagen de fondo
        screen.blit(self.tutorial_image, (0, 0))

    def update(self):
        pass

    def tag(self):
        return "TUTO1"