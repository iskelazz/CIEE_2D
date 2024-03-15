import pygame
import sys, os
from state.GameState import GameState
from resources.text.TextCollection import TextColection

from config import GRAPHICS_DIR, FONTS_DIR 

class IntroductionState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 30)
        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'portada.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))

        self.messages = TextColection.get_introduction_text()
        
        self.snip = self.font.render('',True, 'Black')
        self.counter = 0
        self.speed = 3
        self.active_message = 0
        self.message = self.messages[self.active_message]
        self.done = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.done:
                        if self.active_message < len(self.messages)-1:
                            self.active_message +=1
                            self.done = False
                            self.message = self.messages[self.active_message]
                            self.counter = 0
                            self.speed = 3
                        else:
                            self.game.screen_manager.change_state('TUTO1')
                    else:
                        self.speed = 1

    def update(self):
        pass  # No hay lógica de actualización 

    def draw(self, screen):
    # Dibuja la imagen de fondo
        screen.fill('Black')
        
        if self.counter < self.speed * len(self.message):
            self.counter += 1
        elif self.counter >= self.speed * len(self.message):
            self.done = True
        
        self.snip = self.font.render(self.message[0:self.counter//self.speed], True, 'White')
        screen.blit(self.snip, (100, 300))

    def tag(self):
        return "INTRO"