import pygame
import os
from state.GameState import GameState
from Utils import Utils
from config import FONTS_DIR 

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.pause()
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.pause_text = 'PAUSE'
        self.pause_symbol = '||'  # Símbolo de pausa

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Regresar al estado de juego guardado
                pygame.mixer.unpause()
                self.game.screen_manager.pop_state()

    def update(self):
        pass  # No es necesario actualizar nada en el estado de pausa

    def draw(self, screen):
        # Dibuja la pantalla de juego actual con una capa semitransparente encima
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
        overlay.set_alpha(128)  # Ajusta la transparencia
        overlay.fill((255, 255, 255))  # Fondo blanco semitransparente
        screen.blit(overlay, (0, 0))

        # Dibuja el texto y el símbolo de pausa
        Utils.draw_text_with_shadow(screen, self.pause_text, (self.game.screen_width / 2, self.game.screen_height / 2 - 30), self.font)
        Utils.draw_text_with_shadow(screen, self.pause_symbol, (self.game.screen_width / 2, self.game.screen_height / 2 + 30), self.font)

    def tag(self):
        return "PAUSE"