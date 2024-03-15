import pygame
from state.GameState import GameState
import sys, os
from Utils import Utils
from config import GRAPHICS_DIR, FONTS_DIR, SOUNDS_DIR

class MenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(os.path.join(FONTS_DIR, 'Another_.ttf'), 48)
        self.options = ['JUGAR', 'SALIR']
        self.current_option = 0
        self.color = (255, 255, 255)
        self.color_inactive = (100, 100, 100)
        # Carga la imagen de fondo
        self.background_image = pygame.image.load(os.path.join(GRAPHICS_DIR, 'portada.png')).convert()
        self.background_image = pygame.transform.scale(self.background_image, (game.screen_width, game.screen_height))
        self.background_music = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'menu_theme.mp3'))
        self.menu_option_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'menu_option.wav'))
        self.play_option_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'play_selected.wav'))
        self.background_music.play(-1)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.current_option = max(0, self.current_option - 1)
                    self.menu_option_sound.play()
                elif event.key == pygame.K_DOWN:
                    self.current_option = min(len(self.options) - 1, self.current_option + 1)
                    self.menu_option_sound.play()
                elif event.key == pygame.K_RETURN:
                    if self.current_option == 0:  # PLAY selected
                        self.play_option_sound.play()
                        self.game.screen_manager.change_state('INTRO')
                        self.background_music.stop()
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

    def tag(self):
        return "MENU"