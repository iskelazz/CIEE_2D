from assets.snake.snakeState import SnakeState
import time
from assets.snake.normalState import NormalState

class FastState(SnakeState):
    def on_enter(self):
        super().on_enter()
        self.start_time = time.time()
        self.duration = 5  # Duración de 5 segundos para este estado
        self.snake.speed = 14

    def on_exit(self):
        self.snake.speed = 9
    
    def update(self):
        super().update()
        current_time = time.time()
        if current_time - self.start_time >= self.duration:
            # Tiempo transcurrido, volver al estado normal
            self.snake.set_estado(NormalState(self.snake))