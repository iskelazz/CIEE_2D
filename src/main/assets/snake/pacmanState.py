from assets.snake.snakeState import SnakeState

class PacmanState(SnakeState):
    def update(self):
        return super().update()
    
    def on_enter(self):
        # Cambiar la forma de colisionar, parpadear, etc.
        pass

    def on_exit(self):
        # Restaurar comportamiento original
        pass