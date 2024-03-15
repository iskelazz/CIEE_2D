from state.StateFactory import StateFactory

class StateManager:
    def __init__(self, game):
        self.game = game
        self.state_stack = []

    def push_state(self, state_id):
        """Empuja un nuevo estado a la pila."""
        # Crea y añade el nuevo estado a la pila
        new_state = StateFactory.create_state(state_id, self.game)
        self.state_stack.append(new_state)

    def pop_state(self):
        """Saca el estado actual de la pila."""
        if self.state_stack:
            self.state_stack.pop()

    def change_state(self, state_id):
        """Saca el estado actual y añade uno nuevo"""
        if self.state_stack:
            self.pop_state()
        self.push_state(state_id)

    def current_state(self):
        """Devuelve el estado actual (el último de la pila), o None si la pila está vacía."""
        if self.state_stack:
            return self.state_stack[-1]
        return None

    def handle_events(self, events):
        if self.current_state:
            self.current_state().handle_events(events)

    def update(self):
        if self.current_state:
            self.current_state().update()

    def draw(self, screen):
        if self.current_state:
            self.current_state().draw(screen)