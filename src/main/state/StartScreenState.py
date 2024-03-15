import pygame
from state.GameState import GameState
import sys, os
from Utils import Utils
from config import GRAPHICS_DIR, FONTS_DIR

class StartScreenState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.text = 'Presiona ENTER para empezar'
        self.color = (255, 255, 255)
        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'portada.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.screen_manager.change_state('MENU')

    def update(self):
        pass  # No hay lógica de actualización 

    def draw(self, screen):
    # Dibuja la imagen de fondo
        screen.blit(self.background_image, (0, 0))
    
    # Usa Utils para dibujar el texto con sombra
        Utils.draw_text_with_shadow(screen, self.text, (self.game.screen_width / 2, self.game.screen_height - self.game.screen_height / 6), self.font)

    def tag(self):
        return "START"