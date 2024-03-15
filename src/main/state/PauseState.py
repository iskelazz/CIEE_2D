import pygame
import os
from state.GameState import GameState
from resources.text.TextCollection import TextColection
from Utils import Utils
from config import FONTS_DIR, GRAPHICS_DIR

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.pause()
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 52)
        self.pause_text = TextColection.get_pause_text()
        self.pause_symbol = '||'  # Símbolo de pausa

        # Carga la imagen de fondo    
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'pause_background.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Regresar al estado de juego guardado
                pygame.mixer.unpause()
                self.game.screen_manager.pop_state()

    def update(self):
        pass  # No es necesario actualizar nada en el estado de pausa

    def draw(self, screen):
        # Dibuja la imagen de fondo
        screen.blit(self.background_image, (0, 0))

        # Dibuja el texto y el símbolo de pausa
        Utils.draw_text_with_shadow(screen, self.pause_text, (self.game.screen_width / 2, self.game.screen_height / 2 - 30), self.font)
        Utils.draw_text_with_shadow(screen, self.pause_symbol, (self.game.screen_width / 2, self.game.screen_height / 2 + 30), self.font)

    def tag(self):
        return "PAUSE"