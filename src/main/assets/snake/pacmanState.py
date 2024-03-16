from assets.snake.snakeState import SnakeState
from assets.snake.normalState import NormalState
import pygame
import time
import os
from config import SOUNDS_DIR

class PacmanState(SnakeState):
    def __init__(self, snake):
        super().__init__(snake)
        self.blink_timer = 0
        self.blink_duration = 0.1  # Duración del parpadeo activo
        self.blink_interval = 0.2  # Intervalo de tiempo en segundos para cambiar entre parpadeo y estado normal
        self.use_blink_images = False
        self.start_time = time.time()
        self.snake_pacman_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'pacman_state.wav'))
        #sonido
        self.snake_pacman_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, 'pacman_state.wav'))

    def on_enter(self):
        self.duration = 25  # Duración de 25 segundos para este estado
        self.blink_timer = pygame.time.get_ticks() / 1000.0  # Iniciar temporizador para el parpadeo
        self.snake_pacman_sound.play(-1)

    def update(self):
        super().update()  
        current_time = pygame.time.get_ticks() / 1000.0  # Obtén el tiempo actual en segundos
        if current_time - self.blink_timer > self.blink_interval:
            self.blink_timer = current_time  # Reinicia el temporizador para el próximo ciclo de parpadeo
            self.use_blink_images = not self.use_blink_images
            # Se decide dinámicamente cuál función de dibujo usar
            if self.use_blink_images:
                self.snake.mode_image = "white"
            else:
                self.snake.mode_image = "normal"
        self.check_time_limit()
    

    def check_time_limit(self):
        check_time = time.time()
        if check_time - self.start_time >= self.duration:
            # Tiempo transcurrido, volver al estado normal
            self.snake.set_state(NormalState(self.snake))    


    def on_exit(self):
        self.snake_pacman_sound.stop()
        self.snake.mode_image = "normal"
