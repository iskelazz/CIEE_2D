import pygame
from assets.snake.snakeState import SnakeState
import time
from assets.snake.normalState import NormalState

class FastState(SnakeState):
    def __init__(self, snake):
        super().__init__(snake)
        self.yello_timer = 0
        self.yellow_duration = 0.075  # Duración del parpadeo activo
        self.yellow_interval = 0.4  # Intervalo de tiempo en segundos para cambiar entre parpadeo y estado normal
        self.use_yellow_images = False
        self.start_time = time.time()
        
    def on_enter(self):
        super().on_enter()
        self.yellow_timer = pygame.time.get_ticks() / 1000.0
        self.duration = 5  # Duración de 5 segundos para este estado
        self.snake.speed = 12

    def on_exit(self):
        self.snake.speed = 7
        self.snake.mode_image = "normal"
    
    def update(self):
        super().update()  
        current_time = pygame.time.get_ticks() / 1000.0  # Obtén el tiempo actual en segundos
        if current_time - self.yellow_timer > self.yellow_interval:
            self.yellow_timer = current_time  # Reinicia el temporizador para el próximo ciclo de parpadeo
            self.use_yellow_images = not self.use_yellow_images
            # Se decide dinámicamente cuál función de dibujo usar
            if self.use_yellow_images:
                self.snake.mode_image = "yellow"
            else:
                self.snake.mode_image = "normal"
        self.check_time_limit()

    def check_time_limit(self):
        check_time = time.time()
        if check_time - self.start_time >= self.duration:
            # Tiempo transcurrido, volver al estado normal
            self.snake.set_state(NormalState(self.snake)) 