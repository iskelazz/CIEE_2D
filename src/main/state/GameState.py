from abc import ABC, abstractmethod
import pygame
import time
from pygame.math import Vector2
import sys, os
from Utils import Utils
from config import GRAPHICS_DIR, FONTS_DIR 

class GameState(ABC):
    def __init__(self, game):
        self.game = game

    @abstractmethod
    def handle_events(self, events):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass


class StartScreenState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.text = 'Press ENTER to start'
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
                    self.game.change_state(MenuState(self.game))

    def update(self):
        pass  # No hay lógica de actualización 

    def draw(self, screen):
    # Dibuja la imagen de fondo
        screen.blit(self.background_image, (0, 0))
    
    # Usa Utils para dibujar el texto con sombra
        Utils.draw_text_with_shadow(screen, self.text, (self.game.screen_width / 2, self.game.screen_height - self.game.screen_height / 6), self.font)


class PlayingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Prepara el estado para jugar

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Guardar el estado actual y cambiar a PauseState
                    self.game.previous_state = self
                    self.game.change_state(PauseState(self.game))
                else:
                    # Actualiza la dirección basada en la tecla presionada
                    self.update_direction(event.key)

    def update(self):
        current_time = time.time()
        self.game.snake.update(current_time)
        self.game.check_collisions()
        if self.game.snake.is_snake_out_of_bounds(self.game.cell_number):
            self.game.change_state(GameOverState(self.game))

    def draw(self, screen):
        self.game.draw_elements()

    def update_direction(self, key):
        """Actualiza la dirección de la serpiente basada en la entrada del usuario."""
        directions = {
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1),
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
        }
        if key in directions and directions[key] != -self.game.snake.direction:
            self.game.snake.direction = directions[key]

class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.pause_text = 'PAUSE'
        self.pause_symbol = '||'  # Símbolo de pausa

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Regresar al estado de juego guardado
                self.game.change_state(self.game.previous_state)

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

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.options = ['PLAY', 'EXIT']
        self.current_option = 0
        self.color = (255, 255, 255)
        self.color_inactive = (100, 100, 100)
        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'portada.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_option = max(0, self.current_option - 1)
                elif event.key == pygame.K_DOWN:
                    self.current_option = min(len(self.options) - 1, self.current_option + 1)
                elif event.key == pygame.K_RETURN:
                    if self.current_option == 0:  # PLAY selected
                        self.game.change_state(PlayingState(self.game))
                    elif self.current_option == 1:  # EXIT selected
                        pygame.quit()
                        sys.exit()

    def update(self):
        pass  # No hay lógica de actualización 

    def draw(self, screen):
    # Dibuja la imagen de fondo
        screen.blit(self.background_image, (0, 0))
    
    # Usa Utils para dibujar cada opción del menú con sombra
        for index, option in enumerate(self.options):
            color = self.color if index == self.current_option else self.color_inactive
            position = (self.game.screen_width / 2, self.game.screen_height - self.game.screen_height / 6 + 30 * index)
            Utils.draw_text_with_shadow(screen, option, position, self.font, color)

class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.small_font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 32)
        self.retry_text = 'Press ENTER to Retry'
        self.menu_text = 'Press ESC to Menu'
        self.score_text = f'Score: {self.game.score.score:06d}'
        self.game_over_text = 'GAME OVER'

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reinicia el juego creando una nueva instancia de SnakeGame
                    self.game.__init__()
                    self.game.change_state(PlayingState(self.game))
                elif event.key == pygame.K_ESCAPE:
                    # Cambia al estado del menú
                    self.game.__init__()
                    self.game.change_state(MenuState(self.game))

    def update(self):
        pass  # No hay necesidad de actualización lógica en la pantalla de Game Over

    def draw(self, screen):
        # Fondo
        screen.fill(pygame.Color('black'))

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