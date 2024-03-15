import pygame
from state.GameState import GameState
import sys, os
from config import FONTS_DIR, GRAPHICS_DIR

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.stop()
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.small_font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 32)

        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'game_over_background.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))

        self.retry_text = 'Presiona ENTER para reintentar'
        self.menu_text = 'Presiona ESC para Menu'
        self.score_text = f'Puntuación: {self.game.score.score:06d}'
        self.game_over_text = 'GAME OVER'

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reinicia el juego creando una nueva instancia de SnakeGame
                    self.game.screen_manager.pop_state()
                    tag = self.game.screen_manager.current_state().tag()
                    self.game.screen_manager.change_state(tag)
                elif event.key == pygame.K_ESCAPE:
                    # Cambia al estado del menú
                    self.game.__init__()
                    self.game.screen_manager.pop_state()
                    self.game.screen_manager.change_state("MENU")

    def update(self):
        pass  # No hay necesidad de actualización lógica en la pantalla de Game Over

    def draw(self, screen):
        # Fondo
        screen.blit(self.background_image, (0, 0))

        # Texto de Game Over
        game_over_surface = self.font.render(self.game_over_text, True, pygame.Color('white'))
        game_over_rect = game_over_surface.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 4))
        screen.blit(game_over_surface, game_over_rect)

        # Puntuación
        score_surface = self.small_font.render(self.score_text, True, pygame.Color('white'))
        score_rect = score_surface.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2))
        screen.blit(score_surface, score_rect)

        # Instrucciones para reintentar o volver al menú
        retry_surface = self.small_font.render(self.retry_text, True, pygame.Color('white'))
        retry_rect = retry_surface.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2 + 50))
        screen.blit(retry_surface, retry_rect)

        menu_surface = self.small_font.render(self.menu_text, True, pygame.Color('white'))
        menu_rect = menu_surface.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2 + 100))
        screen.blit(menu_surface, menu_rect)

    def tag(self):
        return "GAME_OVER"