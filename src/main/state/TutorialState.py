import pygame
from state.GameState import GameState
import sys, os
from config import Config

class TutorialState(GameState):
    
    def getTutorialImage(self, stage):
        if 'TUTO1' == stage:
            return 'tutorial_1.png'
        elif 'TUTO2' == stage:
            return 'tutorial_2.png'
        elif 'TUTO3' == stage:
            return 'tutorial_3.png'  
    
    def getNextState(self, stage):
        if 'TUTO1' == stage:
            return 'PLAYING1'
        elif 'TUTO2' == stage:
            return 'PLAYING2'
        elif 'TUTO3' == stage:
            return 'PLAYING3'
    
    def getMusicTheme(self, stage):
        if 'TUTO1' == stage:
            return 'level_1_theme.mp3'
        elif 'TUTO2' == stage:
            return 'level_2_theme.wav'
        elif 'TUTO3' == stage:
            return 'level_3_theme.mp3'

    def __init__(self,game, stage):
        super().__init__(game)
        self.next_state = self.getNextState(stage)
        self.tutorial_image = pygame.image.load(os.path.join(Config.GRAPHICS_DIR, self.getTutorialImage(stage))).convert()
        self.tutorial_image = pygame.transform.scale(self.tutorial_image, (game.screen_width, game.screen_height))
        self.background_music = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, self.getMusicTheme(stage)))
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
                    self.game.screen_manager.change_state(self.next_state)
    
    def draw(self, screen):
    # Dibuja la imagen de fondo
        screen.blit(self.tutorial_image, (0, 0))

    def update(self):
        pass

    def tag(self):
        return "TUTO1"