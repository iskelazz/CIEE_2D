import pygame
import sys, os
from state.GameState import GameState
from resources.text.TextCollection import TextColection

from config import Config

class StoryTellingState(GameState):
    
    def getBackgoundImage(self, story):
        if 'STORY1' == story:
            return 'story_1_background.png'
        elif 'STORY2' == story:
            return 'story_2_background.png'
        elif 'STORY3' == story:
            return 'story_3_background.png'
        elif 'STORY4' == story:
            return 'story_4_background.jpg'
        
    def getTextMessages(self, story):
        if 'STORY1' == story:
            return TextColection.get_story_1_text()
        elif 'STORY2' == story:
            return TextColection.get_story_2_text()
        elif 'STORY3' == story:
            return TextColection.get_story_3_text()
        elif 'STORY4' == story:
            return TextColection.get_story_4_text()
    
    def getNextState(self, story):
        if 'STORY1' == story:
            return 'TUTO1'
        elif 'STORY2' == story:
            return 'TUTO2'
        elif 'STORY3' == story:
            return 'TUTO3'
        elif 'STORY4' == story:
            return 'MENU'
    
    def getTextColor(self, story):
        if 'STORY1' == story:
            return 'White'
        elif 'STORY2' == story:
            return 'White'
        elif 'STORY3' == story:
            return 'White'
        elif 'STORY4' == story:
            return 'Black'
            
    def __init__(self, game, story):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(Config.FONTS_DIR, 'Another_.ttf'), 35)
        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(Config.GRAPHICS_DIR, self.getBackgoundImage(story))).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))
        
        self.background_music = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'intro_theme.mp3'))
        self.typing_sound = pygame.mixer.Sound(os.path.join(Config.SOUNDS_DIR, 'typing_sound.wav'))
        self.messages = self.getTextMessages(story)
        self.text_color = self.getTextColor(story)
        self.next_state = self.getNextState(story)


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
                            pygame.mixer.stop()
                            self.game.screen_manager.change_state(self.next_state)
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
        
        self.snip = self.font.render(self.message[0:self.counter//self.speed], True, self.text_color)

        screen.blit(self.snip, (80, 400))
            
    def tag():
        return 'STORY'
        