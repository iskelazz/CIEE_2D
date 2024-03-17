import pygame
import sys, os
from state.GameState import GameState
from resources.text.TextCollection import TextColection

from config import GRAPHICS_DIR, FONTS_DIR, SOUNDS_DIR

class StoryTellingState2(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 35)
        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'story_2_background.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))
        
        self.background_music = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'intro_theme.mp3'))
        self.typing_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'typing_sound.wav'))
        self.messages = TextColection.get_story_2_text()
        
        self.snip = self.font.render('',True, 'Black')
        self.counter = 0
        self.speed = 3
        self.active_message = 0
        self.message = self.messages[self.active_message]
        self.done = False

        self.typing_sound_playing = True
        self.background_music.play(-1)
        self.typing_sound.play(-1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.done:
                        if not self.typing_sound_playing:
                            self.typing_sound.play(-1)
                            self.typing_sound_playing = True
                        if self.active_message < len(self.messages)-1:
                            self.active_message +=1
                            self.done = False
                            self.message = self.messages[self.active_message]
                            self.counter = 0
                            self.speed = 3
                        else:
                            self.typing_sound.stop()
                            self.background_music.stop()
                            self.game.screen_manager.change_state('TUTO2')
                    else:
                        self.speed = 1

    def update(self):
        pass

    def draw(self, screen):
        # Dibuja la imagen de fondo
        screen.blit(self.background_image, (0, 0))     
        
        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            self.done = True
            self.typing_sound_playing = False
            self.typing_sound.stop()
        
        self.snip = self.font.render(self.message[0:self.counter//self.speed], True, 'White')
        
        screen.blit(self.snip, (60, 400))

    def tag():
        return 'STORY2'
        