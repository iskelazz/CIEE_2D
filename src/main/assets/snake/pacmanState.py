from assets.snake.snakeState import SnakeState
from assets.snake.normalState import NormalState
import pygame
import time

class PacmanState(SnakeState):
    def __init__(self, snake):
        super().__init__(snake)
        self.blink_timer = 0
        self.blink_duration = 0.1  # Duración del parpadeo activo
        self.blink_interval = 0.5  # Intervalo de tiempo en segundos para cambiar entre parpadeo y estado normal
        self.use_blink_images = False
        self.start_time = time.time()

    def on_enter(self):
        self.duration = 25  # Duración de 25 segundos para este estado
        self.blink_timer = pygame.time.get_ticks() / 1000.0  # Iniciar temporizador para el parpadeo

    def update(self):
        super().update()  
        current_time = pygame.time.get_ticks() / 1000.0  # Obtén el tiempo actual en segundos
        if current_time - self.blink_timer > self.blink_interval:
            self.blink_timer = current_time  # Reinicia el temporizador para el próximo ciclo de parpadeo
            self.use_blink_images = not self.use_blink_images
            # Se decide dinámicamente cuál función de dibujo usar
            if self.use_blink_images:
                self.snake.draw_segments = self.draw_blink_segments
            else:
                self.snake.draw_segments = self.snake.draw_snake_segments
        self.check_time_limit()
    

    def check_time_limit(self):
        check_time = time.time()
        if check_time - self.start_time >= self.duration:
            # Tiempo transcurrido, volver al estado normal
            self.snake.set_state(NormalState(self.snake))    


    def on_exit(self):
        self.snake.draw_segments = self.snake.draw_snake_segments

    def draw_blink_segments(self):
        for index, segment in enumerate(self.snake.segments):
            position = self.snake.body[index]
            segment.update(position)
            if index == 0:
                # Convertimos self.direction a tupla antes de usarlo
                segment.image = self.snake.head_blink_images[tuple(self.snake.direction)]
            elif index == len(self.snake.body) - 1:
                direction = self.snake.body[-1] - self.snake.body[-2]
                # Convertimos la dirección a tupla antes de usarla
                segment.image = self.snake.tail_blink_images[tuple(direction)]
            else:
                # Determina la orientación y los giros para los segmentos del cuerpo
                prev_segment = self.snake.body[index - 1]
                next_segment = self.snake.body[index + 1]
                if prev_segment.x == next_segment.x:
                    segment.image = self.snake.body_vertical_blink
                elif prev_segment.y == next_segment.y:
                    segment.image = self.snake.body_horizontal_blink
                else:
                    # Aquí determinamos los giros
                    if prev_segment.x < position.x and next_segment.y < position.y or prev_segment.y < position.y and next_segment.x < position.x:
                        segment.image = self.snake.body_tl_blink
                    elif prev_segment.x > position.x and next_segment.y < position.y or prev_segment.y < position.y and next_segment.x > position.x:
                        segment.image = self.snake.body_tr_blink
                    elif prev_segment.x < position.x and next_segment.y > position.y or prev_segment.y > position.y and next_segment.x < position.x:
                        segment.image = self.snake.body_bl_blink
                    elif prev_segment.x > position.x and next_segment.y > position.y or prev_segment.y > position.y and next_segment.x > position.x:
                        segment.image = self.snake.body_br_blink